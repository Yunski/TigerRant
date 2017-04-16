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
        num = 0
        dept_code = course["dept_code"]
        dept_name = course['dept_name']
        d = sql.Department(code=dept_code, name=dept_name)
        foundDept = sql.Department.query.filter_by(code=dept_code).first()
        if foundDept == None:
            sql.db.session.add(d)
        else:
            d = foundDept
            d.code = dept_code
            d.name = dept_name
        course_id = course["c_id"]
        #print("course_id: {}".format(course_id))
        catalog_number = course["catalog_number"]
        #print("catalog_number: {}".format(catalog_number))
        title = html.unescape(course["title"])
        #print("title: {}".format(title))
        track = course["track"]
        #print("track: {}".format(track))
        description = html.unescape(course["description"])

        c = sql.Course(c_id=int(course_id), dept=dept_code, catalog_number=catalog_number,
                          title=title, track=track, description=description)
        foundCourse = sql.Course.query.filter_by(c_id=int(course_id)).first()
        if foundCourse == None:
            sql.db.session.add(c)
        else:
            c = foundCourse

        d.courses.append(c)
        c.distribution = course["distribution"]
        c.grade_options = course["grade_options"]
        for instructor in course["instructors"]:
            #print("emplid: {}".format(instructor["emplid"]))
            emplid = instructor["emplid"]
            #print("first_name: {}".format(instructor["first_name"]))
            first_name = instructor["first_name"]
            #print("last_name: {}".format(instructor["last_name"]))
            last_name = instructor["last_name"]
            if sql.Instructor.query.filter_by(emplid=emplid).first() == None:
                i = sql.Instructor(emplid=int(emplid), first_name=first_name, last_name=last_name)
                c.instructors.append(i)
                sql.db.session.add(i)
        c.crosslistings = course["crosslistings"]

        ratings = []
        for review in course['reviews']:
            text = review['student_advice']
            if len(text) < 10:
                continue
            foundReview = sql.Review.query.filter_by(c_id=int(course_id)).filter_by(num=num).first()
            if foundReview == None:
                r = sql.Review(c_id=int(course_id),
                               sem_code=int(review['semester_code']),
                               overall_rating=float(review['overall_rating']),
                               lecture_rating=float(review['lecture_rating']),
                               text=text,
                               num=num,
                               score=0,
                               scraped=True)
                c.reviews.append(r)
                sql.db.session.add(r)
            else:
                r = foundReview
                r.sem_code = int(review['semester_code'])
                r.overall_rating = float(review['overall_rating'])
                r.lecture_rating = float(review['lecture_rating'])
                r.text = review['student_advice']
            ratings.append(r.overall_rating)
            num += 1
        if len(ratings) != 0:
            c.avg_rating = sum(ratings) / len(ratings)
        else:
            c.avg_rating = 0
        print("Added {} {}".format(course["dept_code"], course["catalog_number"]))

    sql.db.session.commit()
populateDB(sys.argv[1])
