import requests as req
from bs4 import BeautifulSoup

_1314SPR  = '1144'
_1415FALL = '1152'
_1415SPR  = '1154'
_1516FALL = '1162'
_1516SPR  = '1164'
_1617FALL = '1172'
_1617SPR  = '1174'
_1718FALL = '1182'

def fetchData(courseid):

	dummyid = _1718FALL
	url = "https://registrar.princeton.edu/course-offerings/course_details.xml?courseid={}&term={}".format(courseid, dummyid)

	response = req.get(url)
	html = response.text
	soup = BeautifulSoup(html, 'html.parser')

	data = {}
	data["distr"] = ""
	data["grade_options"] = ""

	for string in soup.stripped_strings:
		if string == "(HA)":
			data["distr"] = "HA"
		if string == "(LA)":
			data["distr"] = "LA"
		if string == "(SA)":
			data["distr"] = "SA"
		if string == "(EM)":
			data["distr"] = "EM"
		if string == "(EC)":
			data["distr"] = "EC"
		if string == "(SA)":
			data["distr"] = "SA"
		if string == "(QR)":
			data["distr"] = "QR"
		if string == "(STL)":
			data["distr"] = "STL"
		if string == "(STN)":
			data["distr"] = "STN"

	if soup.em != None:
		data["grade_options"] = soup.em.text.strip()

	return data
