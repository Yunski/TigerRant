import datetime
import requests as req
import json
import config
import html
import sys
import shopper
import shopper.model_cloudsql as sql

def populateDB(filename):
    shopper.create_app(config).app_context().push()

    with open(filename) as data_file:
        data = json.load(data_file)
    print("data loaded from file")
    current_time = datetime.datetime.utcnow()
    courses = data['courses']
    for course in courses:
        dept_code = course["dept_code"]
        dept_name = course['dept_name']
        d = sql.Department.query.filter_by(code=dept_code).first()
        if d == None:
            d = sql.Department(code=dept_code, name=dept_name)
            sql.db.session.add(d)
        else:
            d.code = dept_code
            d.name = dept_name
        c_id = int(course["c_id"])
        #print("c_id: {}".format(c_id))
        catalog_number = course["catalog_number"]
        #print("catalog_number: {}".format(catalog_number))
        title = html.unescape(course["title"])
        #print("title: {}".format(title))
        track = course["track"]
        #print("track: {}".format(track))
        description = html.unescape(course["description"])

        c = sql.Course.query.filter_by(c_id=c_id).first()
        if c == None:
            c = sql.Course(c_id=c_id, dept=dept_code, catalog_number=catalog_number,
                              title=title, track=track, description=description)
            sql.db.session.add(c)

        d.courses.append(c)
        c.distribution = course["distribution"]
        c.grade_options = course["grade_options"]
        c.crosslistings = course["crosslistings"]

        current = 1182
        t = sql.Term(code=current, overall_rating=0.0, course=c)
        sql.db.session.add(t)
        for instructor in course['instructors']:
            emplid = int(instructor["emplid"])
            first_name = instructor["first_name"]
            last_name = instructor["last_name"]
            i = sql.Instructor.query.filter_by(emplid=emplid).first()
            if i == None:
                i = sql.Instructor(emplid=emplid, first_name=first_name, last_name=last_name)
                sql.db.session.add(i)
            t.instructors.append(i)

        ratings = []
        for (termCode, term) in course['terms'].items():
            num = 0
            code = int(termCode)
            t = sql.Term.query.filter_by(c_id=c_id, code=code).first()
            if t == None:
                overall_rating = 0.0
                try:
                    overall_rating = float(term['overall_rating'])
                except ValueError:
                    pass
                t = sql.Term(code=code, overall_rating=overall_rating, course=c)
                sql.db.session.add(t)
            ratings.append(t.overall_rating)
            for instructor in term['instructors']:
                emplid = instructor['emplid']
                first_name = instructor['first_name']
                last_name = instructor['last_name']
                i = sql.Instructor.query.filter_by(emplid=emplid).first()
                if i == None:
                    i = sql.Instructor(emplid=emplid, first_name=first_name, last_name=last_name)
                    sql.db.session.add(i)
                t.instructors.append(i)
            for review in term['reviews']:
                if len(review) < 10:
                    continue
                r = sql.Review.query.filter_by(c_id=c_id, sem_code=t.code, num=num).first()
                if r == None:
                    r = sql.Review(c_id=c_id,
                                   rating=t.overall_rating,
                                   text=review,
                                   num=num,
                                   upvotes=0,
                                   scraped=True,
                                   term=t)
                    sql.db.session.add(r)
                num += 1

        if len(ratings) != 0:
            c.avg_rating = sum(ratings) / len(ratings)
        else:
            c.avg_rating = 0
        print("Added {} {}".format(course["dept_code"], course["catalog_number"]))

    sql.db.session.commit()
populateDB(sys.argv[1])
