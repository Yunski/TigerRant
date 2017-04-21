import datetime
import json
import logging
import sys

from flask import abort, current_app, Flask, request, redirect, url_for, render_template, session
from flask_api import status
from flask_cas import CAS

from . import model_cloudsql as sql
from . import cas
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
        if 'netid' in session:
            return redirect(url_for('browse'))
        return render_template('index.html')


    @app.route('/validate')
    def validate():
        netid = cas.username
        if netid is None:
            return redirect('/')
        response = redirect(url_for('browse'), code=status.HTTP_302_FOUND)
        session['netid'] = netid
        user = sql.User.query.filter_by(netid=netid).first()
        if user is None:
            newUser = sql.User(netid=netid, upvoted_reviews = "", upvoted_rants = "", downvoted_rants = "", upvoted_descriptions = "", downvoted_descriptions = "", upvoted_replys = "", downvoted_replys = "")
            sql.db.session.add(newUser)
            sql.db.session.commit()
        return response


    @app.route('/logout', methods=['POST'])
    def logout():
        session.pop('netid', None)
        return redirect(url_for('index'))


    @app.route('/browse')
    def browse():
        if 'netid' not in session:
            return redirect(url_for('index'))
        netid = session['netid']
        page = request.args.get('page')
        search = request.args.get('search')
        order = request.args.get('order')
        if order == None:
            order = "dept"
        if page is None or search is None:
            return render_template('home.html', netid=netid)

        #find list of classes that match search
        #returns a tuple of type results, pageInt, length, num_pages
        results, pageInt, length, num_pages = sc.matched_courses(search, order, page)

        #return searched classes (for specific page)
        return render_template('browse.html', netid=netid, courses=results, current=pageInt, num_results=length, pages=num_pages, search=search, order=order)


    @app.route('/course')
    def course():
        if 'netid' not in session:
            return redirect(url_for('index'))
        netid = session['netid']
        course_id = request.args.get('id')
        if course_id is None:
            return redirect(url_for('browse'))
        if not course_id.isdigit():
            return redirect(url_for('browse'))
        c_id = int(course_id)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            # course page not found
            return redirect(url_for('browse'))

        return render_template('course.html', netid=netid, course=course)


    @app.route('/cart')
    def cart():
        if 'netid' not in session:
            return redirect(url_for('index'))
        netid = session['netid']
        return render_template('cart.html', netid=netid)


    @app.route('/distributions')
    def distributions():
        if 'netid' not in session:
            return redirect(url_for('index'))
        netid = session['netid']
        return render_template('distributions.html', netid=netid)

        """
    @app.route('/rant')
    def rant():
        if 'netid' not in session:
            return redirect(url_for('index'))
        return render_template('rant.html')"""


    @app.route('/api/descriptions/<int:c_id>', methods=['POST'])
    def post_description(c_id):
        if 'netid' not in session:
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
        if 'netid' not in session:
            abort(401)
        vote = 0
        paramVote = request.form['vote']
        try:
            vote = int(paramVote)
        except ValueError:
            abort(401)
        description = sql.Description.query.get(description_id)
        user = sql.User.query.filter_by(netid=session["netid"]).first()
        if vote == 1:
            if str(description_id) not in user.upvoted_descriptions:
                user.upvoted_descriptions += " " + str(description_id)
            else:
                vote = 0
            if str(description_id) in user.downvoted_descriptions:
                user.downvoted_descriptions = user.downvoted_descriptions.replace(str(description_id), "")
                vote = 2
        elif vote == -1:
            if str(description_id) not in user.downvoted_descriptions:
                user.downvoted_descriptions += " " + str(description_id)
            else:
                vote = 0
            if str(description_id) in user.upvoted_descriptions:
                user.upvoted_descriptions = user.upvoted_descriptions.replace(str(description_id), "")
                vote = -2
        if description == None:
            abort(404)
        description.upvotes += vote
        sql.db.session.commit()
        return json.dumps({'upvotes': description.upvotes}), 201


    @app.route('/api/descriptions/<int:c_id>', methods=['GET'])
    def get_descriptions(c_id):
        if 'netid' not in session:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
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
            descriptionsJson.append(dDict)
        sql.db.session.commit()
        return json.dumps(descriptionsJson)


    @app.route('/api/rants/<int:c_id>', methods=['POST'])
    def post_rant(c_id):
        if 'netid' not in session:
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
        if 'netid' not in session:
            abort(401)
        vote = 0
        paramVote = request.form['vote']
        try:
            vote = int(paramVote)
        except ValueError:
            abort(401)
        rant = sql.Rant.query.get(rant_id)
        user = sql.User.query.filter_by(netid=session["netid"]).first()
        if vote == 1:
            if str(rant_id) not in user.upvoted_rants:
                user.upvoted_rants += " " + str(rant_id)
            else:
                vote = 0
            if str(rant_id) in user.downvoted_rants:
                user.downvoted_rants = user.downvoted_rants.replace(str(rant_id), "")
                vote = 2
        elif vote == -1:
            if str(rant_id) not in user.downvoted_rants:
                user.downvoted_rants += " " + str(rant_id)
            else:
                vote = 0
            if str(rant_id) in user.upvoted_rants:
                user.upvoted_rants = user.upvoted_rants.replace(str(rant_id), "")
                vote = -2
        if rant == None:
            abort(404)
        rant.upvotes += vote
        sql.db.session.commit()
        return json.dumps({'upvotes': rant.upvotes}), 201


    @app.route('/api/rants/<int:c_id>', methods=['GET'])
    def get_rants(c_id):
        if 'netid' not in session:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        rants = course.rants.order_by(sql.Rant.timestamp.desc()).all()
        rantsJson = []
        currentTime = datetime.datetime.utcnow()
        for rant in rants:
            rantDict = {}
            rantDict['id'] = rant.id
            rantDict['text'] = rant.text
            rantDict['upvotes'] = rant.upvotes
            rantDict['replies'] = []
            rantDict['timestamp'] = util.elapsedTime(rant.timestamp, currentTime)
            for reply in rant.replies.all():
                replyDict = {}
                replyDict['id'] = reply.id
                replyDict['text'] = reply.text
                replyDict['upvotes'] = reply.upvotes
                replyDict['timestamp'] = util.elapsedTime(reply.timestamp, currentTime)
                rantDict['replies'].append(replyDict)
            rantsJson.append(rantDict)
        return json.dumps(rantsJson)


    @app.route('/api/replies/<int:rant_id>', methods=['POST'])
    def post_reply(rant_id):
        if 'netid' not in session:
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
        if 'netid' not in session:
            abort(401)
        print(reply_id)
        vote = 0
        paramVote = request.form['vote']
        try:
            vote = int(paramVote)
        except ValueError:
            abort(401)
        reply = sql.Reply.query.get(reply_id)
        user = sql.User.query.filter_by(netid=session["netid"]).first()
        if vote == 1:
            if str(reply_id) not in user.upvoted_replys:
                user.upvoted_replys += " " + str(reply_id)
            else:
                vote = 0
            if str(reply_id) in user.downvoted_replys:
                user.downvoted_replys = user.downvoted_replys.replace(str(reply_id), "")
                vote = 2
        elif vote == -1:
            if str(reply_id) not in user.downvoted_replys:
                user.downvoted_replys += " " + str(reply_id)
            else:
                vote = 0
            if str(reply_id) in user.upvoted_replys:
                user.upvoted_replys = user.upvoted_replys.replace(str(reply_id), "")
                vote = -2
        if reply == None:
            abort(404)
        reply.upvotes += vote
        sql.db.session.commit()
        return json.dumps({'upvotes': reply.upvotes}), 201

    @app.route('/api/reviews/<int:c_id>', methods=['POST'])
    def post_review(c_id):
        if 'netid' not in session:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        sem_code = request.form['sem_code']
        rating = request.form['rating']
        text = request.form['text']
        num = len(course.reviews.all())
        review = sql.Review(sem_code=sem_code,
                       overall_rating=rating,
                       text=text,
                       num=num,
                       score=0,
                       scraped=False,
                       course=course)
        sql.db.session.add(review)
        sql.db.session.commit()
        return json.dumps({'sem_code': review.sem_code, 'text': review.text, 'score': review.score}), 201


    @app.route('/api/reviews/<int:review_id>', methods=['PUT'])
    def update_review(review_id):
        if 'netid' not in session:
            abort(401)
        score = 0
        paramScore = request.form['score']
        try:
            score = int(paramScore)
        except ValueError:
            abort(401)
        review = sql.Review.query.get(review_id)
        if review == None:
            abort(404)
        user = sql.User.query.filter_by(netid=session["netid"]).first()
        if score == 1:
            if str(review_id) not in user.upvoted_reviews:
                user.upvoted_reviews += " " + str(review_id)
            else:
                score = 0
        review.score += score
        sql.db.session.commit()
        return json.dumps({'score': review.score}), 201


    @app.route('/api/reviews/<int:c_id>', methods=['GET'])
    def get_reviews(c_id):
        if 'netid' not in session:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        reviews = course.reviews.all()
        reviewsJson = {}
        termSet = set()
        for review in reviews:
            termSet.add(review.sem_code)
        current = 1182
        termSet.add(current)

        for term in termSet:
            reviews = course.reviews.filter_by(sem_code=term).filter_by(scraped=False).order_by(sql.Review.timestamp.desc()).all()
            reviews += course.reviews.filter_by(sem_code=term).filter_by(scraped=True).order_by(sql.Review.timestamp.desc()).all()
            reviewsJson[term] = {}
            reviewsJson[term]['reviews'] = []
            termCode = str(term)[1:]
            if termCode[2:3] == "2":
                termString = "Fall " + str(int(termCode[:2]) - 1)
            else:
                termString = "Spring " + termCode[:2]
            reviewsJson[term]['term_string'] = termString
            for review in reviews:
                reviewDict = {}
                reviewDict['id'] = review.id
                reviewDict['sem_code'] = review.sem_code
                reviewDict['overall_rating'] = review.overall_rating
                reviewDict['lecture_rating'] = review.lecture_rating
                reviewDict['text'] = review.text
                reviewDict['score'] = review.score
                reviewsJson[term]['reviews'].append(reviewDict)
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
