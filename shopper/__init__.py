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
            newUser = sql.User(netid=netid, ticket=ticket)
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
                            score=0,
                            scraped=False,
                            term=term)
        sql.db.session.add(review)
        term.overall_rating = (term.overall_rating * num + review.rating) / (num + 1)
        course.avg_rating = sum(t.overall_rating for t in course.terms.all()) / len(course.terms.all())
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
            for review in term.reviews.order_by(sql.Review.timestamp.desc()).all():
                reviewDict = {}
                reviewDict['id'] = review.id
                reviewDict['sem_code'] = review.sem_code
                reviewDict['rating'] = review.rating
                reviewDict['text'] = review.text
                reviewDict['score'] = review.score
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
