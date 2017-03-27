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
        if 'netid' in session:
            return redirect(url_for('browse'))
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
        fields = None
        if search is not None:
            fields = search.split()
        if page is None or search is None:
            departments = sql.Department.query.order_by(sql.Department.code).all()
            display_per_row = 6
            return render_template('home.html', netid=netid, departments=departments, display_per_row=display_per_row)
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
        results = sql.Course.query[start:end]
        if fields is not None:
            baseQuery = sql.Course.query.order_by(sql.Course.dept)
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
                    baseQuery = baseQuery.filter(sql.Course.description.contains(field))
            length = len(baseQuery.all())
            if length < end:
                end = length
            results = baseQuery.order_by(sql.Course.catalog_number)[start:end]
            num_pages = length // 12 + (length % 12 > 0)
        return render_template('browse.html', netid=netid, courses=results, current=pageInt, num_results=length, pages=num_pages, search=search)


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


    @app.route('/rant')
    def rant():
        if 'netid' not in session:
            return redirect(url_for('index'))
        return render_template('rant-space.html')


    @app.route('/reviews', methods=['POST'])
    def reviews():
        if 'netid' not in session:
            return redirect(url_for('index'))
        if request.method == 'POST':
            data = json.loads(request.data.decode())
            course_id = data['cid']
            if course_id == None:
                return "", status.HTTP_400_BAD_REQUEST
            if not course_id.isdigit():
                return "", status.HTTP_400_BAD_REQUEST
            c_id = int(course_id)
            course = sql.Course.query.filter_by(c_id=c_id).first()
            if course == None:
                return "course does not exist", status.HTTP_406_NOT_ACCEPTABLE
            reviews = course.reviews.all()
            reviewsJson = {}
            termSet = set()
            for review in reviews:
                termSet.add(review.sem_code)
            for term in termSet:
                reviews = course.reviews.filter_by(sem_code=term).all()
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
                    reviewDict['student_advice'] = review.student_advice
                    reviewsJson[term]['reviews'].append(reviewDict)
            return json.dumps(reviewsJson)
        return "", status.HTTP_400_BAD_REQUEST

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
