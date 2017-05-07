import datetime
import json
import logging
import sys

from flask import abort, current_app, Flask, make_response, request, redirect, url_for, render_template, session
from flask_api import status
from flask_cas import CAS

from . import model_cloudsql as sql
from . import search_courses as sc
from . import util

def create_app(config, debug=False, testing=False, config_overrides=None):
    cas = CAS()
    app = Flask(__name__)
    cas.init_app(app)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    with app.app_context():
        model = sql
        model.init_app(app)


    @app.route('/')
    def index():
        if cas.username is not None:
            return redirect(url_for('browse'))
        return render_template('index.html')

    @app.route('/validate')
    def validate():
        netid = cas.username
        if netid is None:
            return redirect('/')
        response = redirect(url_for('browse'), code=status.HTTP_302_FOUND)
        user = sql.User.query.filter_by(netid=netid).first()
        if user is None:
            newUser = sql.User(netid=netid, upvoted_reviews = "", upvoted_rants = "", downvoted_rants = "", upvoted_descriptions = "", downvoted_descriptions = "", upvoted_replies = "", downvoted_replies = "")
            sql.db.session.add(newUser)
            sql.db.session.commit()
        return response

    @app.route('/browse')
    def browse():
        netid = cas.username
        if netid is None:
            return redirect(url_for('index'))
        page = request.args.get('page')
        search = request.args.get('search')
        order = request.args.get('order')
        if order == None:
            order = "dept"
        courses = request.cookies.get('courses')
        if (courses == None) or (courses == ""):
            num = '0'
        else:
            num = str(len(courses.split(' ')))
        if page is None or search is None:
            return render_template('home.html', netid=netid, incart=num)

        #find list of classes that match search
        #returns a tuple of type results, pageInt, length, num_pages
        results, pageInt, length, num_pages = sc.matched_courses(search, order, page)

        descriptions = []

        for course in results:
            urban = course.descriptions.order_by(sql.Description.upvotes.desc()).first()
            if urban == None:
                desc = course.description
            elif urban.upvotes < 10:
                desc = course.description
            else:
                desc = urban.text

            desc = desc.split()
            count = 40
            if len(desc) > count:
                desc = desc[0:count]
                desc.append("...")
            desc = " ".join(desc)
            descriptions.append(desc)

        #return searched classes (for specific page)
        return render_template('browse.html', netid=netid, courses=results,
        current=pageInt, num_results=length, pages=num_pages, search=search, order=order, incart=num, desc=descriptions)

    @app.route('/course')
    def course():
        netid = cas.username
        if netid is None:
            return redirect(url_for('index'))
        course_id = request.args.get('id')
        search = request.args.get('search')
        page = request.args.get('page')
        order = request.args.get('order')
        if course_id is None:
            return redirect(url_for('browse'))
        if not course_id.isdigit():
            return redirect(url_for('browse'))
        c_id = int(course_id)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            # course page not found
            return redirect(url_for('browse'))
        courses_cookie = request.cookies.get('courses')
        if (courses_cookie == None) or (courses_cookie == ""):
            num = '0'
        else:
            num = str(len(courses_cookie.split(' ')))
        return render_template('course.html', netid=netid, course=course, search=search, page=page, order=order, incart=num)

    @app.route('/addtocart')
    def add_to_cart():
        netid = cas.username
        if netid is None:
            return redirect(url_for('index'))
        course_id = request.args.get('id')
        search = request.args.get('search')
        page = request.args.get('page')
        order = request.args.get('order')
        if course_id is None:
            return redirect(url_for('browse'))
        if not course_id.isdigit():
            return redirect(url_for('browse'))
        c_id = int(course_id)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            # course page not found
            return redirect(url_for('browse'))
        courses_cookie = request.cookies.get('courses')
        if (courses_cookie == None) or (courses_cookie == ""):
            response = make_response(render_template('course.html', netid=netid, search=search, page=page, order=order, course=course, incart='1'))
            response.set_cookie('courses', course_id)
            return response
        else:
            if course_id not in courses_cookie:
                num = str(len(courses_cookie.split(' ')) + 1)
                response = make_response(render_template('course.html', netid=netid, search=search, page=page, order=order, course=course, incart=num))
                response.set_cookie('courses', (courses_cookie + ' ' + course_id))
                return response
            else:
                num = str(len(courses_cookie.split(' ')))
                return make_response(render_template('course.html', netid=netid, search=search, page=page, order=order, course=course, incart=num))

    @app.route('/about')
    def about():
        netid = cas.username
        loggedIn = netid is not None
        courses = request.cookies.get('courses')
        if (courses == None) or (courses == ""):
            num = '0'
        else:
            num = str(len(courses.split(' ')))
        return render_template('about.html', netid=netid, loggedIn=loggedIn, incart=num)

    def delete(course, string):
        if len(string) < 4: return ""
        courses = string.split(' ')
        result = ""
        for i in range(0, len(courses)):
            if (courses[i] != ' ') and (courses[i] != course):
                result += courses[i] + " "
        return result.strip()

    @app.route('/cart')
    def cart():
        netid = cas.username
        if netid is None:
            return redirect(url_for('index'))
        course_cookie = request.cookies.get('courses')
        courses = []
        if course_cookie == None:
            return render_template('cart.html', netid=netid, courses=courses, incart='0')
        course_id = request.args.get('id')
        removeAll = request.args.get('remall')
        if removeAll != None:
            response = make_response(render_template('cart.html', netid=netid, incart='0'))
            response.set_cookie('courses', '')
            return response
        if course_id != None:
            if not course_id.isdigit():
                '''going to want to redirect back to course page not browse'''
                return redirect(url_for('cart'))
            if course_id in course_cookie:
                course_cookie = delete(course_id, course_cookie)
                course_ids = course_cookie.split(' ')
                if (course_cookie == None) or (course_cookie == ""):
                    num = '0'
                else:
                    num = str(len(course_ids))
                for course_id in course_ids:
                    if course_id != '':
                        c_id = int(course_id)
                        course = sql.Course.query.filter_by(c_id=c_id).first()
                        if course != None: courses.append(course)
                response = make_response(render_template('cart.html', netid=netid, courses=courses, incart=num))
                response.set_cookie('courses', course_cookie)
                return response
        course_ids = course_cookie.split(' ')
        for course_id in course_ids:
            if course_id != '':
                c_id = int(course_id)
                course = sql.Course.query.filter_by(c_id=c_id).first()
                if course != None: courses.append(course)
        if (course_cookie == None) or (course_cookie == ""):
            num = '0'
        else:
            num = str(len(course_ids))
        return render_template('cart.html', netid=netid, courses=courses, incart=num)

    @app.route('/api/descriptions/<int:c_id>', methods=['POST'])
    def post_description(c_id):
        if cas.username is None:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        text = request.form['text']
        description = sql.Description(text=text, upvotes=0, course=course)
        sql.db.session.add(description)
        sql.db.session.commit()
        return json.dumps({'text': description.text, 'upvotes': description.upvotes}), 201

    @app.route('/api/descriptions/<int:description_id>', methods=['PUT'])
    def update_description(description_id):
        netid = cas.username
        if netid is None:
            abort(401)
        vote = 0
        paramVote = request.form['vote']
        try:
            vote = int(paramVote)
        except ValueError:
            abort(401)
        description = sql.Description.query.get(description_id)
        user = sql.User.query.filter_by(netid=netid).first()
        if vote == 1:
            if str(description_id) not in user.upvoted_descriptions:
                user.upvoted_descriptions += " " + str(description_id) + " "
            else:
                vote = -1
                user.upvoted_descriptions = user.upvoted_descriptions.replace(" " + str(description_id) + " ", "")
            if str(description_id) in user.downvoted_descriptions:
                user.downvoted_descriptions = user.downvoted_descriptions.replace(" " + str(description_id) + " ", "")
                vote = 2
        elif vote == -1:
            if str(description_id) not in user.downvoted_descriptions:
                user.downvoted_descriptions += " " + str(description_id) + " "
            else:
                vote = 1
                user.downvoted_descriptions = user.downvoted_descriptions.replace(" " + str(description_id) + " ", "")
            if str(description_id) in user.upvoted_descriptions:
                user.upvoted_descriptions = user.upvoted_descriptions.replace(" " + str(description_id) + " ", "")
                vote = -2
        if description == None:
            abort(404)
        description.upvotes += vote
        sql.db.session.commit()
        return json.dumps({'upvotes': description.upvotes}), 201

    @app.route('/api/descriptions/<int:c_id>', methods=['GET'])
    def get_descriptions(c_id):
        netid = cas.username
        if netid is None:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        user = sql.User.query.filter_by(netid=netid).first()
        descriptions = course.descriptions.order_by(sql.Description.upvotes.desc()).all()
        descriptionsJson = []
        for description in descriptions:
            if description.upvotes <= -10:
                sql.db.session.delete(description)
                continue
            dDict = {}
            dDict['id'] = description.id
            dDict['text'] = description.text
            dDict['upvotes'] = description.upvotes
            dDict['action'] = 0
            if str(description.id) in user.upvoted_descriptions:
                dDict['action'] = 1
            elif str(description.id) in user.downvoted_descriptions:
                dDict['action'] = -1
            descriptionsJson.append(dDict)
        sql.db.session.commit()
        return json.dumps(descriptionsJson)

    @app.route('/api/rants/<int:c_id>', methods=['POST'])
    def post_rant(c_id):
        if cas.username is None:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        text = request.form['text']
        rant = sql.Rant(text=text, upvotes=0, course=course)
        sql.db.session.add(rant)
        sql.db.session.commit()
        return json.dumps({'id': rant.id, 'text': rant.text, 'upvotes': rant.upvotes}), 201

    @app.route('/api/rants/<int:rant_id>', methods=['PUT'])
    def update_rant(rant_id):
        netid = cas.username
        if netid is None:
            abort(401)
        vote = 0
        paramVote = request.form['vote']
        try:
            vote = int(paramVote)
        except ValueError:
            abort(401)
        rant = sql.Rant.query.get(rant_id)
        user = sql.User.query.filter_by(netid=netid).first()
        if vote == 1:
            if str(rant_id) not in user.upvoted_rants:
                user.upvoted_rants += " " + str(rant_id) + " "
            else:
                vote = -1
                user.upvoted_rants = user.upvoted_rants.replace(" " + str(rant_id) + " ", "")
            if str(rant_id) in user.downvoted_rants:
                user.downvoted_rants = user.downvoted_rants.replace(" " + str(rant_id) + " ", "")
                vote = 2
        elif vote == -1:
            if str(rant_id) not in user.downvoted_rants:
                user.downvoted_rants += " " + str(rant_id) + " "
            else:
                vote = 1
                user.downvoted_rants = user.downvoted_rants.replace(" " + str(rant_id) + " ", "")
            if str(rant_id) in user.upvoted_rants:
                user.upvoted_rants = user.upvoted_rants.replace(" " + str(rant_id) + " ", "")
                vote = -2
        if rant == None:
            abort(404)
        rant.upvotes += vote
        sql.db.session.commit()
        return json.dumps({'upvotes': rant.upvotes}), 201

    @app.route('/api/rants/<int:c_id>', methods=['GET'])
    def get_rants(c_id):
        netid = cas.username
        if netid is None:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        try:
            isHot = request.args.get('sort-by') == 'true'
        except ValueError:
            isHot = False
        rants = course.rants.order_by(sql.Rant.timestamp.desc()).all()
        if isHot:
            rants.sort(key=lambda k: k.upvotes, reverse=True)
        user = sql.User.query.filter_by(netid=netid).first()
        rantsJson = []
        currentTime = datetime.datetime.utcnow()
        for rant in rants:
            rantDict = {}
            rantDict['id'] = rant.id
            rantDict['text'] = rant.text
            rantDict['upvotes'] = rant.upvotes
            rantDict['replies'] = []
            rantDict['action'] = 0
            if str(rant.id) in user.upvoted_rants:
                rantDict['action'] = 1
            elif str(rant.id) in user.downvoted_rants:
                rantDict['action'] = -1
            rantDict['timestamp'] = util.elapsedTime(rant.timestamp, currentTime)
            for reply in rant.replies.all():
                replyDict = {}
                replyDict['id'] = reply.id
                replyDict['text'] = reply.text
                replyDict['upvotes'] = reply.upvotes
                replyDict['action'] = 0
                if str(reply.id) in user.upvoted_replies:
                    replyDict['action'] = 1
                elif str(reply.id) in user.downvoted_replies:
                    replyDict['action'] = -1
                replyDict['timestamp'] = util.elapsedTime(reply.timestamp, currentTime)
                rantDict['replies'].append(replyDict)
            rantsJson.append(rantDict)
        return json.dumps(rantsJson)

    @app.route('/api/replies/<int:rant_id>', methods=['POST'])
    def post_reply(rant_id):
        if cas.username is None:
            abort(401)
        rant = sql.Rant.query.get(rant_id)
        if rant == None:
            abort(404)
        text = request.form['text']
        reply = sql.Reply(text=text, upvotes=0, parent=rant)
        sql.db.session.add(reply)
        sql.db.session.commit()
        time = util.elapsedTime(reply.timestamp, datetime.datetime.utcnow())
        return json.dumps({'id': reply.id, 'text': reply.text, 'upvotes': reply.upvotes, 'timestamp': time}), 201

    @app.route('/api/replies/<int:reply_id>', methods=['PUT'])
    def update_reply(reply_id):
        netid = cas.username
        if netid is None:
            abort(401)
        vote = 0
        paramVote = request.form['vote']
        try:
            vote = int(paramVote)
        except ValueError:
            abort(401)
        reply = sql.Reply.query.get(reply_id)
        user = sql.User.query.filter_by(netid=netid).first()
        if vote == 1:
            if str(reply_id) not in user.upvoted_replies:
                user.upvoted_replies += " " + str(reply_id) + " "
            else:
                vote = -1
                user.upvoted_replies = user.upvoted_replies.replace(" " + str(reply_id) + " ", "")
            if str(reply_id) in user.downvoted_replies:
                user.downvoted_replies = user.downvoted_replies.replace(" " + str(reply_id) +  " ", "")
                vote = 2
        elif vote == -1:
            if str(reply_id) not in user.downvoted_replies:
                user.downvoted_replies += " " + str(reply_id) + " "
            else:
                vote = 1
                user.downvoted_replies = user.downvoted_replies.replace(" " + str(reply_id) +  " ", "")
            if str(reply_id) in user.upvoted_replies:
                user.upvoted_replies = user.upvoted_replies.replace(" " + str(reply_id) + " ", "")
                vote = -2
        if reply == None:
            abort(404)
        reply.upvotes += vote
        sql.db.session.commit()
        return json.dumps({'upvotes': reply.upvotes}), 201

    @app.route('/api/reviews/<int:c_id>', methods=['POST'])
    def post_review(c_id):
        if cas.username is None:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        sem_code = 0
        rating = 0.0
        try:
            sem_code =int(request.form['sem_code'])
        except ValueError:
            abort(400)
        try:
            rating = float(request.form['rating'])
        except ValueError:
            abort(400)
        text = request.form['text']
        term = sql.Term.query.filter_by(c_id=c_id, code=sem_code).first()
        num = len(term.reviews.all())
        review = sql.Review(rating=rating,
                            text=text,
                            num=num,
                            upvotes=0,
                            scraped=False,
                            term=term)
        sql.db.session.add(review)
        term.overall_rating = (term.overall_rating * num + review.rating) / (num + 1)
        course.avg_rating = sum(t.overall_rating for t in course.terms.all()) / len(course.terms.all())
        sql.db.session.commit()
        return json.dumps({'sem_code': review.sem_code, 'text': review.text, 'upvotes': review.upvotes}), 201

    @app.route('/api/reviews/<int:review_id>', methods=['PUT'])
    def update_review(review_id):
        netid = cas.username
        if netid is None:
            abort(401)
        upvotes = 0
        paramVotes = request.form['upvotes']
        try:
            upvotes = int(paramVotes)
        except ValueError:
            abort(401)
        review = sql.Review.query.get(review_id)
        if review == None:
            abort(404)
        user = sql.User.query.filter_by(netid=netid).first()
        if upvotes == 1:
            if " " + str(review_id) + " " not in user.upvoted_reviews:
                user.upvoted_reviews += " " + str(review_id) + " "
            else:
                upvotes = -1
                user.upvoted_reviews = user.upvoted_reviews.replace(" " + str(review_id) + " ", "")
        review.upvotes += upvotes
        sql.db.session.commit()
        return json.dumps({'upvotes': review.upvotes}), 201

    @app.route('/api/reviews/<int:c_id>', methods=['GET'])
    def get_reviews(c_id):
        netid = cas.username
        if netid is None:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        try:
            byUpvotes = request.args.get('sort-by') == 'true'
        except ValueError:
            byUpvotes = False
        user = sql.User.query.filter_by(netid=netid).first()
        terms = course.terms.all()
        reviewsJson = {}
        for term in terms:
            code = term.code
            reviewsJson[code] = {}
            termCode = str(term.code)[1:]
            if termCode[2:3] == "2":
                termString = "Fall " + str(int(termCode[:2]) - 1)
            else:
                termString = "Spring " + termCode[:2]
            reviewsJson[code]['term_string'] = termString
            reviewsJson[code]['average_rating'] = term.overall_rating
            reviewsJson[code]['instructors'] = []
            for instructor in term.instructors:
                instrucDict = {}
                instrucDict['emplid'] = instructor.emplid
                instrucDict['first_name'] = instructor.first_name
                instrucDict['last_name'] = instructor.last_name
                reviewsJson[code]['instructors'].append(instrucDict)
            reviewsJson[code]['reviews'] = []
            reviewsForTerm = term.reviews.order_by(sql.Review.timestamp.desc()).all()
            if byUpvotes:
                reviewsForTerm.sort(key=lambda k: k.upvotes, reverse=True)
            for review in reviewsForTerm:
                reviewDict = {}
                reviewDict['id'] = review.id
                reviewDict['sem_code'] = review.sem_code
                reviewDict['rating'] = review.rating
                reviewDict['text'] = review.text
                reviewDict['action'] = 0
                if str(review.id) in user.upvoted_reviews:
                    reviewDict['action'] = 1
                reviewDict['upvotes'] = review.upvotes
                reviewsJson[code]['reviews'].append(reviewDict)
        return json.dumps(reviewsJson)

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500

    return app
