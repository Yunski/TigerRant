from selenium import webdriver
import time
import sys
from bs4 import BeautifulSoup
import requests as req
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

		#maps eid to name list. list[0] is first name. list[-1] is last name
		profs = []

		profSoup = soup.find_all("a", style="color:blue;")
		for item in profSoup:
			employee = {}
			ied = item.get('href')[19:28]
			employee["employee_id"] = ied

			name = item.text
			name = name.split()

			if len(name) == 2:
				employee["first_name"] = name[0]
				employee["last_name"]  = name[1]
			else:
				employee["first_name"]  = name[0] + " " + name[1]
				employee["last_name"]   = name[2]

			#profs[ied] = name
			profs.append(employee)

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


		term["overall_rating"] = rating
		term["lecture_rating"] = lecture
		############################################

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
	dummyid = _1718FALL #####################UPDATE ME

	url = "https://reg-captiva.princeton.edu/chart/index.php?terminfo={}&courseinfo={}".format(dummyid, courseid)
	response = req.get(url)
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
		
	url = "https://registrar.princeton.edu/course-offerings/course_details.xml?courseid={}&term={}".format(courseid, dummyid)

	response = req.get(url)
	html = response.text
	soup = BeautifulSoup(html, 'html.parser')

	for string in soup.stripped_strings:
		if string == "(HA)":
			course["distr"] = "HA"
		if string == "(LA)":
			course["distr"] = "LA"
		if string == "(SA)":
			course["distr"] = "SA"
		if string == "(EM)":
			course["distr"] = "EM"
		if string == "(EC)":
			course["distr"] = "EC"
		if string == "(SA)":
			course["distr"] = "SA"
		if string == "(QR)":
			course["distr"] = "QR"
		if string == "(STL)":
			course["distr"] = "STL"
		if string == "(STN)":
			course["distr"] = "STN"

	if soup.em != None:
		course["grade_options"] = soup.em.text.strip()	

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
  'distr': 'LA',
  'grade_options': 'na, npdf',
  'terms': {
    '1172': {
      'lecture_rating': '3.35',
      'overall_rating': '3.61',
      'instructors': [
        {
          'last_name': 'Oliver',
          'first_name': 'Demetrius D.',
          'employee_id': '960539099'
        },
        {
          'last_name': 'Whetstone',
          'first_name': 'Jeffrey',
          'employee_id': '961200463'
        }
      ]
    },
    '1152': {
      'lecture_rating': '3.83',
      'overall_rating': '3.85',
      'instructors': [
        {
          'last_name': 'Backstrom',
          'first_name': 'Sofie H.',
          'employee_id': '960700359'
        },
        {
          'last_name': 'Lawson',
          'first_name': 'Deana',
          'employee_id': '960832339'
        }
      ]
    },
    '1144': {
      'lecture_rating': '3.81',
      'overall_rating': '4.19',
      'instructors': [
        {
          'last_name': 'Abeles',
          'first_name': 'Michele H.',
          'employee_id': '961070064'
        },
        {
          'last_name': 'Lawson',
          'first_name': 'Deana',
          'employee_id': '960832339'
        }
      ]
    },
    '1154': {
      'lecture_rating': '3.72',
      'overall_rating': '3.92',
      'instructors': [
        {
          'last_name': 'Abeles',
          'first_name': 'Michele H.',
          'employee_id': '961070064'
        },
        {
          'last_name': 'Oliver',
          'first_name': 'Demetrius D.',
          'employee_id': '960539099'
        }
      ]
    },
    '1162': {
      'lecture_rating': '3.93',
      'overall_rating': '4.00',
      'instructors': [
        {
          'last_name': 'Backstrom',
          'first_name': 'Sofie H.',
          'employee_id': '960700359'
        },
        {
          'last_name': 'Oliver',
          'first_name': 'Demetrius D.',
          'employee_id': '960539099'
        }
      ]
    },
    '1164': {
      'lecture_rating': '4.41',
      'overall_rating': '4.39',
      'instructors': [
        {
          'last_name': 'Backstrom',
          'first_name': 'Sofie H.',
          'employee_id': '960700359'
        },
        {
          'last_name': 'Whetstone',
          'first_name': 'Jeffrey',
          'employee_id': '961200463'
        }
      ]
    }
  }
}
'''