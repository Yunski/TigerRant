import requests as req
import json
import config
import html
import shopper
import shopper.model_cloudsql as sql

def fetchCourses(term, subject):
    shopper.create_app(config).app_context().push()

    courseURL = "http://etcweb.princeton.edu/webfeeds/courseofferings/?term={}&subject={}&meet=no&fmt=json".format(term, subject)
    r = req.get(courseURL)
    data = json.loads(r.text)
    print("data loaded: {}", len(data))
    subjects = data["term"][0]["subjects"]
    for subject in subjects:
        dept = subject["code"]
        print("dept: {}".format(dept))

        courses = subject["courses"]

        for course in courses:
            print("course_id: {}".format(course["course_id"]))
            course_id = course["course_id"]
            print("catalog_number: {}".format(course["catalog_number"]))
            catalog_number = course["catalog_number"]
            print("title: {}".format(course["title"]))
            title = html.unescape(course["title"])
            print("track: {}".format(course["detail"]["track"]))
            track = course["detail"]["track"]
            print("description: {}".format(course["detail"]["description"]))
            description = html.unescape(course["detail"]["description"])
            c = sql.Course(c_id=course_id, dept=dept, catalog_number=catalog_number,
                              title=title, track=track, description=description)

            for instructor in course["instructors"]:
                print("emplid: {}".format(instructor["emplid"]))
                emplid = instructor["emplid"]
                print("first_name: {}".format(instructor["first_name"]))
                first_name = instructor["first_name"]
                print("last_name: {}".format(instructor["last_name"]))
                last_name = instructor["last_name"]
                if sql.Instructor.query.filter_by(emplid=emplid).first() == None:
                    i = sql.Instructor(emplid=emplid, first_name=first_name, last_name=last_name)
                    c.instructors.append(i)
                    sql.db.session.add(i)
            crosslists = []
            if "crosslistings" in course:
                for crossl in course["crosslistings"]:
                    crosslists.append("{}{}".format(crossl["subject"], crossl["catalog_number"]))
            c.crosslisting = ",".join(crosslists)
            sql.db.session.add(c)
    sql.db.session.commit()
fetchCourses("current", "all")
