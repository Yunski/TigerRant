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
        results = sql.Course.query[start:end]
        if search is not None:
            baseQuery = sql.Course.query.filter(sql.Course.dept == search)
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

        search = request.args.get('search')
        page = request.args.get('page')
        returnURL = "/browse?search={}&page={}".format(search, page)

        current = request.args.get('current')
        maxPerPage = 20
        if current is not None:
            if current.isdigit():
                currentPage = int(current)
                start = (currentPage-1) * maxPerPage
                end = currentPage * maxPerPage
        else:
            currentPage = 1
            start = 0
            end = maxPerPage
        length = len(course.reviews.all())
        if length < end:
            end = length
        num_pages = length // maxPerPage + (length % maxPerPage > 0)

        reviews = course.reviews.order_by(sql.Review.overall_rating)[start:end]
        allreviews = course.reviews.order_by(sql.Review.sem_code)
        terms = {}
        prevTermCode = -1
        recent = -1
        for review in allreviews:
            currentTerm = int(review.sem_code)
            if prevTermCode != currentTerm:
                period = ""
                term = str(currentTerm)[1:]
                if term[2:3] == "2": period = "Fall "
                else: period = "Spring "
                prevYear = str(int(term[:2]) - 1)
                period += prevYear + "-" + term[:2]
                prevTermCode = currentTerm
                recent = prevTermCode
                terms[prevTermCode] = {
                    "rating": review.overall_rating,
                    "num_reviews": "1",
                    "prof_rating": review.lecture_rating,
                    "period": period
                }
            else:
                curNum = int(terms[currentTerm]["num_reviews"])
                terms[currentTerm]["num_reviews"] = str(curNum + 1)
                for key in terms:
                    sys.stdout.write(str(terms[key]) + '\n')
                    sys.stdout.flush()
        if recent != -1:
            return render_template('course.html', netid=netid, course=course, current=currentPage, pages=num_pages, recent=recent, reviews=reviews, returnURL=returnURL, terms=terms, total=length)
        else: #this means no reviews
            return render_template('course.html', netid=netid, course=course, current=currentPage, pages=num_pages, reviews=reviews, returnURL=returnURL, terms=terms, total=length)

    @app.route('/cart')
    def cart():
        if 'netid' not in session:
            return redirect(url_for('index'))
        netid = session['netid']
        return render_template('cart.html', netid=netid)

    @app.route('/rant')
    def rant():
        if 'netid' not in session:
            return redirect(url_for('index'))
        return render_template('rant-space.html')

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
