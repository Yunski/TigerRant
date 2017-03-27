import requests
from bs4 import BeautifulSoup

_1314SPR  = '1144'
_1415FALL = '1152'
_1415SPR  = '1154'
_1516FALL = '1162'
_1516SPR  = '1164'
_1617FALL = '1172'
_1617SPR  = '1174'

def fetchDistribution(courseid):

	dummyid = _1617SPR
	url = "https://registrar.princeton.edu/course-offerings/course_details.xml?courseid={}&term={}".format(courseid, dummyid)

	response = requests.get(url)
	html = response.text
	soup = BeautifulSoup(html, 'html.parser')

	for string in soup.stripped_strings:
		if string == "(HA)":
			return "HA"
		if string == "(LA)":
			return "LA"
		if string == "(SA)":
			return "SA"
		if string == "(EM)":
			return "EM"
		if string == "(EC)":
			return "EC"
		if string == "(SA)":
			return "SA"
		if string == "(QR)":
			return "QR"
		if string == "(STL)":
			return "STL"
		if string == "(STN)":
			return "STN"

	return ""
