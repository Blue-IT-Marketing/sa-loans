import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail
import datetime,random,string
from google.appengine.api import memcache

import logging
#Jinja Loader
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

from loans import *
class bgDataHandler(webapp2.RequestHandler):
    def get(self):
        findRequest = LoanApplicantDetails.query()
        thisLoanApplicantDetailsList = findRequest.fetch()


        template = template_env.get_template('templates/dynamic/admin/bg/bg.html')
        context = {'thisLoanApplicantDetailsList':thisLoanApplicantDetailsList}

        self.response.write(template.render(context))


class BankingDetailsHandler(webapp2.RequestHandler):
    def get(self):
        findRequest = LoanBankingDetails.query()
        thisLoanBankingList = findRequest.fetch()

        template = template_env.get_template('templates/dynamic/admin/bg/bgl.html')
        context = {'thisLoanBankingList':thisLoanBankingList}

        self.response.write(template.render(context))


app = webapp2.WSGIApplication([
    ('/bg/data/mob1234567890@', bgDataHandler),
    ('/bg/data/bank/mob1234567890@', BankingDetailsHandler)

], debug=True)

