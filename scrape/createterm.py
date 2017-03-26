#this is to check the correctess of createReview.py

from selenium import webdriver
import time
import sys
from bs4 import BeautifulSoup
import requests
import re

_1314SPR  = '1144'
_1415FALL = '1152'
_1415SPR  = '1154'
_1516FALL = '1162'
_1516SPR  = '1164'
_1617FALL = '1172'
_1617SPR  = '1174'

terms = [_1314SPR, _1415FALL, _1415SPR, _1516FALL, _1516SPR, _1617FALL, _1617SPR]

def newTerm(termid, courseid):
	driver = webdriver.PhantomJS()
	#make this
	url = "https://reg-captiva.princeton.edu/chart/index.php?terminfo={}&courseinfo={}".format(termid, courseid)
	driver.get(url)

	time.sleep(3)
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')

	term = {}
	#term["termid"] = termid

	profs = []

	profSoup = soup.find_all("a", style="color:blue;")
	for item in profSoup:
		profs.append(item.text)

	term["profs"] = profs

	for i in range(len(soup.find_all('tspan'))):
		#magic number all the wayyyyyy
		if i is 13:
			term["rating"] = soup.find_all('tspan')[i].text

	reviews = []
	reviewSoup = soup.find_all("tr", class_="two")
	for item in reviewSoup:
		reviews.append(item.text)

	#uncomment later, uncommented to make object smaller
	#term["reviews"] = reviews

	driver.close()
	return term

def newCourse(courseid):
	course = {}
	course["course-id"]  = courseid
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

	for termid in terms:
		course[termid] = newTerm(termid, courseid)

	return course

print(newCourse('002051'))
