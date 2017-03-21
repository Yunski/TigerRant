import requests as req
import json
import config
import html
import shopper
import shopper.model_cloudsql as sql
from scrape.createReview import newCourse

def populateDB():
    shopper.create_app(config).app_context().push()

    with open('courses.json') as data_file:
        data = json.load(data_file)
    print("data loaded from courses.json")
    courses = data['courses']
    for course in courses:
        num = 0
        dept = course["dept"]
        #print("dept: {}".format(dept))
        course_id = course["c_id"]
        #print("course_id: {}".format(course_id))
        catalog_number = course["catalog_number"]
        #print("catalog_number: {}".format(catalog_number))
        title = html.unescape(course["title"])
        #print("title: {}".format(title))
        track = course["track"]
        #print("track: {}".format(track))
        description = html.unescape(course["description"])

        url = "/course?id={}".format(course_id)
        c = sql.Course(c_id=int(course_id), dept=dept, catalog_number=catalog_number,
                          title=title, track=track, description=description, url=url)
        foundCourse = sql.Course.query.filter_by(c_id=int(course_id)).first()
        if foundCourse == None:
            sql.db.session.add(c)
        else:
            c = foundCourse

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
        c.crosslisting = course["crosslistings"]

        for review in course['reviews']:
            foundReview = sql.Review.query.filter_by(course_id=int(course_id)).filter_by(num=num).first()
            if foundReview == None:
                r = sql.Review(course_id=int(course_id),
                               sem_code=int(review['semester_code']),
                               overall_rating=float(review['overall_rating']),
                               lecture_rating=float(review['lecture_rating']),
                               student_advice=review['student_advice'],
                               num=num)
                c.reviews.append(r)
                sql.db.session.add(r)
            else:
                r = foundReview
                r.sem_code = int(review['semester_code'])
                r.overall_rating = float(review['overall_rating'])
                r.lecture_rating = float(review['lecture_rating'])
                r.student_advice = review['student_advice']
            num += 1
        print("Added {} {}".format(course["dept"], course["catalog_number"]))

    sql.db.session.commit()
populateDB()
