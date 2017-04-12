import datetime
import json
import logging
import sys

from flask import current_app, Flask, request, redirect, url_for, render_template, session
from flask_api import status

from . import model_cloudsql as sql
from . import cas

def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
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
        #if 'netid' in session:
        #    return redirect(url_for('browse'))
        return render_template('index.html')


    @app.route('/login')
    def login():
        c = cas.CASClient(request.url_root)
        return redirect(c.LoginURL(), code=307)


    @app.route('/login/validate')
    def validate():
        if 'ticket' not in request.args:
            content = 'cas login error'
            return content, status.HTTP_400_BAD_REQUEST
        ticket = request.args.get('ticket')
        c = cas.CASClient(request.url_root)
        netid = c.Validate(ticket)
        if netid is None:
            return redirect('/')
        response = redirect(url_for('home'), code=status.HTTP_302_FOUND)
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

    @app.route('/home')
    def home():
        if 'netid' not in session:
            return redirect(url_for('index'))
        netid = session['netid']
        return render_template('home.html', netid=netid)

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

        fields = None
        if search is not None:
            fields = search.split()
        if page is None or search is None:
            return render_template('home.html', netid=netid)
        pageInt = 0
        if page.isdigit():
            pageInt = int(page)
            start = (pageInt-1) * 12
            end = pageInt * 12
        else:
            pageInt = 1
            start = 0
            end = 12
        length = len(sql.Course.query.all())
        if length < end:
            end = length
        num_pages = length // 12 + (length % 12 > 0)
        results = []
        if fields is not None:
            baseQuery = sql.Course.query
            if order == "dept":
                baseQuery = baseQuery.order_by(sql.Course.dept)
            elif order == "rating":
                baseQuery = baseQuery.order_by(sql.Course.avg_rating.desc())
            for field in fields:
                if len(field) == 3:
                    if not field.isdigit():
                        if field == "STN" or field == "STL":
                            baseQuery = baseQuery.filter(sql.Course.distribution == field)
                        else:
                            baseQuery = baseQuery.filter(sql.Course.dept == field)
                    else:
                        baseQuery = baseQuery.filter(sql.Course.catalog_number == field)
                elif len(field) == 2 and not field.isdigit():
                    baseQuery = baseQuery.filter(sql.Course.distribution == field)
                else:
                    baseQuery = baseQuery.filter(sql.Course.title.contains(field) | sql.Course.description.contains(field))
            length = len(baseQuery.all())
            if length < end:
                end = length
            results = baseQuery.order_by(sql.Course.catalog_number)[start:end]
            num_pages = length // 12 + (length % 12 > 0)
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
        return json.dumps({'description': text}), 201

    @app.route('/api/descriptions/<int:c_id>', methods=['GET'])
    def get_descriptions(c_id):
        if 'netid' not in session:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        descriptions = course.descriptions.all()
        descriptionsJson = []
        for description in descriptions:
            dDict = {}
            dDict['text'] = description.text
            dDict['upvotes'] = description.upvotes
            descriptionsJson.append(dDict)
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
        sql.db.session.add(review)
        sql.db.session.commit()
        return json.dumps({'rant': text}), 201


    @app.route('/api/rants/<int:c_id>', methods=['GET'])
    def get_rants(c_id):
        if 'netid' not in session:
            abort(401)
        course = sql.Course.query.filter_by(c_id=c_id).first()
        if course == None:
            abort(404)
        rants = course.rants.all()
        rantsJson = []
        for rant in rants:
            rantDict = {}
            rantDict['text'] = rant.text
            rantDict['upvotes'] = rant.upvotes
            rantsJson.append(rantDict)
        return json.dumps(rantsJson)


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
        print(sem_code)
        print(rating)
        print(text)
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
        return json.dumps({'sem_code': sem_code, 'rating': rating, 'text': text}), 201


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
        for term in termSet:
            reviews = course.reviews.filter_by(sem_code=term).order_by(sql.Review.timestamp).all()
            reviewsJson[term] = {}
            reviewsJson[term]['reviews'] = []
            termCode = str(term)[1:]
            if termCode[2:3] == "2":
                termString = "Fall "
            else:
                termString = "Spring "
            termString += str(int(termCode[:2]) - 1) + "-" + termCode[:2]
            reviewsJson[term]['term_string'] = termString
            for review in reviews:
                reviewDict = {}
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
