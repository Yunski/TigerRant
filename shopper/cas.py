import requests
from flask_api import status
from lxml import etree

class CASClient:
    def __init__(self, base_url):
        self.cas_url = 'https://fed.princeton.edu/cas/'
        self.service_url = base_url + 'login/validate'
        self.namespace = {'cas': 'http://www.yale.edu/tp/cas'}
    def LoginURL(self):
        login_url = self.cas_url + 'login' + '?service=' + self.service_url
        return login_url

    def LogoutURL(self):
        login_url = self.cas_url + 'logout'
        return logout_url

    def Validate(self, ticket):
        val_url = self.cas_url + "serviceValidate" + '?service=' + self.service_url+ '&ticket=' + ticket
        r = requests.post(val_url)
        if r.status_code != status.HTTP_200_OK:
            return None
        root = etree.fromstring(r.text)
        user = root.xpath('/cas:serviceResponse/cas:authenticationSuccess/cas:user', namespaces=self.namespace)
        if user is not None:
            netid = user[0].text
            return netid
        return None
