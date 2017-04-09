import requests as req
import json
import html
import re
from createReview import newCourse
from distribution import fetchData

def fetchCourses(term, subject):
    courseURL = "http://etcweb.princeton.edu/webfeeds/courseofferings/?term={}&subject={}&fmt=json".format(term, subject)
    r = req.get(courseURL)
    data = r.json()
    courseList = {}
    courseList['courses'] = []
    sections = re.compile('^[L|C|S|U]' , re.IGNORECASE)
    print("fetched data from course offerings web feed")
    subjects = data['term'][0]['subjects']
    for subject in subjects:
        dept_code = subject['code']
        dept_name = html.unescape(subject['name'])
        #print("dept: {}".format(dept))
        courses = subject['courses']

        for course in courses:
            print("Start course_id: {}, {} {}".format(course['course_id'], dept_code, course['catalog_number']))
            #print("course_id: {}".format(course['course_id']))
            course_id = course['course_id']
            #print("catalog_number: {}".format(course['catalog_number']))
            catalog_number = course['catalog_number']
            #print("title: {}".format(course['title']))
            title = html.unescape(course['title'])
            #print("track: {}".format(course['detail']['track']))
            track = course['detail']['track']
            #print("description: {}".format(course['detail']['description']))
            description = html.unescape(course['detail']['description'])
            courseObj = {}
            courseObj['c_id'] = course_id
            courseObj['dept_code'] = dept_code
            courseObj['dept_name'] = dept_name
            courseObj['catalog_number'] = catalog_number
            courseObj['title'] = title
            courseObj['track'] = track
            courseObj['description'] = description
            courseData = fetchData(course_id)
            courseObj['distribution'] = courseData['distr']
            courseObj['grade_options'] = courseData['grade_options']
            courseObj['instructors'] = []
            for instructor in course['instructors']:
                #print("emplid: {}".format(instructor['emplid']))
                emplid = instructor['emplid']
                #print("first_name: {}".format(instructor['first_name']))
                first_name = instructor['first_name']
                #print("last_name: {}".format(instructor['last_name']))
                last_name = instructor['last_name']
                instructorObj = {}
                instructorObj['emplid'] = emplid
                instructorObj['first_name'] = first_name
                instructorObj['last_name'] = last_name
                courseObj['instructors'].append(instructorObj)

            crosslists = []
            if 'crosslistings' in course:
                for crossl in course['crosslistings']:
                    crosslists.append("{} {}".format(crossl['subject'], crossl['catalog_number']))
            courseObj['crosslistings'] = ",".join(crosslists)
            courseObj['sections'] = []
            if 'classes' in course:
                for section in course['classes']:
                    #if sections.search(section['section']) != None:
                    sectionObj = {}
                    sectionObj['class_number'] = section['class_number']
                    sectionObj['section'] = section['section']
                    sectionObj['status'] = section['status']
                    sectionObj['capacity'] = section['capacity']
                    sectionObj['enrollment'] = section['enrollment']
                    if 'schedule' in section:
                        if 'meetings' in section['schedule']:
                            meeting = section['schedule']['meetings'][0]
                            sectionObj['start_time'] = meeting['start_time']
                            sectionObj['end_time'] = meeting['end_time']
                            if 'days' in meeting:
                                sectionObj['days'] = meeting['days']
                            if 'building' in meeting:
                                sectionObj['building'] = meeting['building']['name']
                            if 'room' in meeting:
                                sectionObj['room'] = meeting['room']
                    courseObj['sections'].append(sectionObj)

            courseObj['reviews'] = newCourse(course_id)['reviews']
            courseList['courses'].append(courseObj)
            print("Finished course_id: {}, {} {}".format(course['course_id'], dept_code, course['catalog_number']))

        with open('courses.json', 'w') as courseFile:
            json.dump(courseList, courseFile, indent=4, separators=(',', ': '))
fetchCourses("current", "all")
