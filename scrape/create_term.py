from selenium import webdriver
import time
import sys
from bs4 import BeautifulSoup
import requests
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_1314SPR  = '1144'
_1415FALL = '1152'
_1415SPR  = '1154'
_1516FALL = '1162'
_1516SPR  = '1164'
_1617FALL = '1172'
_1617SPR  = '1174'
_1718FALL = '1182'

def newTerm(driver, termid, courseid):

    url = "https://reg-captiva.princeton.edu/chart/index.php?terminfo={}&courseinfo={}".format(termid, courseid)
    driver.get(url)

    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "svg")))
    finally:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        term = {}
        #term["termid"] = termid

        profs = []

        profSoup = soup.find_all("a", style="color:blue;")
        for item in profSoup:
            foo = item.text
            foo = " ".join(foo.split()) #remove double spaces between words
            profs.append(foo)

        term["instructors"] = profs

        #find ratings!
        ########################################
        tspan = soup.find_all('tspan')

        r = 6
        while tspan[r].text != '':
            r += 1

        graphRows = (r - 6)/2

        rating = 0
        lecture = 0

        for i in range(len(tspan)):
            #magic number all the wayyyyyy
            if i == 6 + graphRows + 2 - 1:
                rating = tspan[i].text
            if i == 6 + graphRows + graphRows - 1:
                lecture = tspan[i].text
        ############################################

        term["overall_rating"] = rating
        term["lecture_rating"] = lecture

        reviews = []
        reviewSoup = soup.find_all("tr", class_="two")
        for item in reviewSoup:
            reviews.append(item.text)

        #uncomment later, uncommented to make object smaller
        term["reviews"] = reviews


        return term

#return new course dictionary of course with id courseid
def newCourse(courseid):

    course = {}
    course["course-id"] = courseid
    dummyid = _1617SPR #####################UPDATE ME

    url = "https://reg-captiva.princeton.edu/chart/index.php?terminfo={}&courseinfo={}".format(dummyid, courseid)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    terms = []

    for item in soup.table.find_all("td"):
        if item.text == "2013-2014 Spring":
            terms.append(_1314SPR)
        if item.text == "2014-2015 Fall":
            terms.append(_1415FALL)
        if item.text == "2014-2015 Spring":
            terms.append(_1415SPR)
        if item.text == "2015-2016 Fall":
            terms.append(_1516FALL)
        if item.text == "2015-2016 Spring":
            terms.append(_1516SPR)
        if item.text == "2016-2017 Fall":
            terms.append(_1617FALL)

    #course["reviews"] = []
    #tempList = course["reviews"]
    driver = webdriver.PhantomJS()
    course["terms"] = {}

    for termid in terms:
        course["terms"][termid] = newTerm(driver, termid, courseid)
        #url = "https://reg-captiva.princeton.edu/chart/index.php?terminfo={}&courseinfo={}".format(termid, courseid)
        #response = urllib2.urlopen(url)
        #html = response.read()
        #soup = BeautifulSoup(html, 'html.parser')
        #if not soup.find_all(string=re.compile("not available")):

        # populateReviews(driver, tempList, courseid, termid)

    driver.close()
    return course

if __name__ == '__main__':
    print(newCourse('008907'))
    """
    for review in eval_info["reviews"]:
        print(review['semester-code'])
        print(review['overall-rating'])
        print(review['lecture-rating'])
        print(review['student-advice'])
        for prof in review['professors']:
            print(prof)"""

#Example return value (reviews redacted)

'''
{
  'course-id': '008907',
  'terms': {
    '1164': {
      'overall_rating': '4.39',
      'instructors': [
        'Sofie H. Backstrom',
        'Jeffrey Whetstone'
      ],
      'lecture_rating': '4.41',
      'reviews': [

      ]
    },
    '1172': {
      'overall_rating': '3.61',
      'instructors': [
        'Demetrius D. Oliver',
        'Jeffrey Whetstone'
      ],
      'lecture_rating': '3.35',
      'reviews': [

      ]
    },
    '1144': {
      'overall_rating': '4.19',
      'instructors': [
        'Michele H. Abeles',
        'Deana Lawson'
      ],
      'lecture_rating': '3.81',
      'reviews': [

      ]
    },
    '1154': {
      'overall_rating': '3.92',
      'instructors': [
        'Michele H. Abeles',
        'Demetrius D. Oliver'
      ],
      'lecture_rating': '3.72',
      'reviews': [

      ]
    },
    '1162': {
      'overall_rating': '4.00',
      'instructors': [
        'Sofie H. Backstrom',
        'Demetrius D. Oliver'
      ],
      'lecture_rating': '3.93',
      'reviews': [

      ]
    },
    '1152': {
      'overall_rating': '3.85',
      'instructors': [
        'Sofie H. Backstrom',
        'Deana Lawson'
      ],
      'lecture_rating': '3.83',
      'reviews': [

      ]
    }
  }
}
'''
