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

#terms = [_1314SPR, _1415FALL, _1415SPR, _1516FALL, _1516SPR, _1617FALL]

#create a newReview dictionary and populate its fields
def newReview(termid, rating, review, profs, lecture):
	newReview = {}
	newReview["semester_code"] = termid
	newReview["overall_rating"] = rating
	newReview["student_advice"] = review
	newReview["instructors"] = profs
	newReview["lecture_rating"] = lecture
	return newReview

#populate the review list of some course
def populateReviews(driver, tempList, courseid, termid):
	#make this
	url = "https://reg-captiva.princeton.edu/chart/index.php?terminfo={}&courseinfo={}".format(termid, courseid)
	driver.get(url)

	try:
		element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.TAG_NAME, "svg")))
	finally:
		#print(driver.find_element_by_id("content").text)
		#driver.close()

		#time.sleep(3)
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
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

		profs = []

		profSoup = soup.find_all("a", style="color:blue;")
		for item in profSoup:
			profs.append(item.text)

		reviews = []
		reviewSoup = soup.find_all("tr", class_="two")
		for item in reviewSoup:
			reviews.append(item.text)


		for review in reviews:
			tempList.append(newReview(termid, rating, review, profs, lecture))

#return new course dictionary of course with id courseid
def newCourse(courseid):
	driver = webdriver.PhantomJS()
	course = {}
	course["course-id"] = courseid
	dummyid = _1617SPR

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

	course["reviews"] = []
	tempList = course["reviews"]

	for termid in terms:
		#url = "https://reg-captiva.princeton.edu/chart/index.php?terminfo={}&courseinfo={}".format(termid, courseid)
		#response = urllib2.urlopen(url)
		#html = response.read()
		#soup = BeautifulSoup(html, 'html.parser')
		#if not soup.find_all(string=re.compile("not available")):
		populateReviews(driver, tempList, courseid, termid)
	driver.close()
	return course

if __name__ == '__main__':
	eval_info = newCourse('009380')
	"""
	for review in eval_info["reviews"]:
		print(review['semester-code'])
		print(review['overall-rating'])
		print(review['lecture-rating'])
		print(review['student-advice'])
		for prof in review['professors']:
			print(prof)"""
