
import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
import datetime
from Employee import *
from google.appengine.api import urlfetch
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

from loans import AdvancedAmount,LoanApplicantDetails

class ClientReport(ndb.Expando):
    strIDNumber = ndb.StringProperty()
    strReport = ndb.StringProperty()
    strReference = ndb.StringProperty()


    def writeIDNumber(self,strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.strIDNumber = strinput
                return True
            else:
                return False
        except:
            return True


    def writeReport(self,strinput):
        try:
            strinput = str(strinput)
            self.strReport = strinput
            return True
        except:
            return False

    def writeReference(self,strinput):
        try:
            strinput = str(strinput)
            if strinput != None:
                self.strReference = strinput
                return True
            else:
                return False
        except:
            return False

class SearchPartners(ndb.Expando):
    strIndex = ndb.IntegerProperty(default=0)
    strPartnerURL = ndb.StringProperty()

class ClientCheckWithIDHandler(webapp2.RequestHandler):
    def get(self):
        try:
            URL = str(self.request.uri)
            URLlist = URL.split("/")
            vstrIDNumber = URLlist[len(URLlist)-1]
            if "?" in vstrIDNumber:
                cleanID = vstrIDNumber.split("?")
                vstrIDNumber = cleanID[0]
            logging.info('ID Number : ' + vstrIDNumber)


            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strIDNumber == vstrIDNumber)
            thisLoanApplicantList = findRequest.fetch()

            if len(thisLoanApplicantList) > 0:
                thisLoanApplicant = thisLoanApplicantList[0]
                findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == thisLoanApplicant.strAccountNumber)
                thisAdvancedList = findRequest.fetch()

                template = template_env.get_template('templates/dynamic/ratings/global.html')
                context = {'thisLoanApplicant':thisLoanApplicant,'thisAdvancedList':thisAdvancedList}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/dynamic/ratings/global.html')
                context = {'Message':'Client has no history here'}
                self.response.write(template.render(context))
        except:
            template = template_env.get_template('templates/dynamic/ratings/global.html')
            context = {'Message':'There was an error looking for client history'}
            self.response.write(template.render(context))

class SendRequestForClientCheckHandler(webapp2.RequestHandler):
    def get(self):
        try:
            Guser = users.get_current_user()
            if Guser:
                URL = str(self.request.uri)
                URLlist = URL.split("/")
                vstrIDNumber = URLlist[len(URLlist)-1]
                if "?" in vstrIDNumber:
                    cleanID = vstrIDNumber.split("?")
                    vstrIDNumber = cleanID[0]
                logging.info('ID Number : ' + vstrIDNumber)
                self.response.write('ID Number : ' + vstrIDNumber)


                findRequest = SearchPartners.query()
                thisSearchPartnersList = findRequest.fetch()
                thisContent = ""
                ishistory = False
                for thisSearchPartner in thisSearchPartnersList:
                    try:

                        result = urlfetch.fetch(thisSearchPartner.strPartnerURL + "/clientcheck/withid/" + vstrIDNumber)
                        if result.status_code == 200:
                            thisContent = thisContent + result.content
                            ishistory = True
                        else:
                            pass
                    except urlfetch.Error:
                        logging.exception('Caught exception fetching url')
                if ishistory:

                    findRequest = ClientReport.query(ClientReport.strIDNumber == vstrIDNumber)
                    thisClientReportList = findRequest.fetch()

                    if len(thisClientReportList) > 0:
                        thisClientReport = thisClientReportList[0]
                    else:
                        thisClientReport = ClientReport()

                    thisClientReport.writeIDNumber(strinput=vstrIDNumber)
                    thisClientReport.writeReference(strinput=Guser.user_id())
                    thisClientReport.writeReport(strinput=thisContent)
                    thisClientReport.put()
                    thisContent = thisContent + """  <a href="/employees/rating/print/""" +vstrIDNumber + """ " """ + """ class="btn btn-primary btn-block"><i class="fa fa-print"> </i> <strong>Print Record</strong></a> """

                    self.response.write(thisContent)
                else:
                    self.response.write("""
                    <p>Client has no History</p>
                    <a href="/employees/loans" class="btn btn-success btn-block"><i class="fa fa-users"> </i> <strong>Create Loan</strong> </a>
                    """)
        except:
            self.response.write("Error Fetching Data")
class PrintGlobalRatingHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            URL = str(self.request.uri)
            URLlist = URL.split("/")
            vstrIDNumber = URLlist[len(URLlist) - 1]

            findRequest = ClientReport.query(ClientReport.strIDNumber == vstrIDNumber)
            thisClientReportList = findRequest.fetch()
            if len(thisClientReportList) > 0:
                thisClientReport = thisClientReportList[0]
            else:
                thisClientReport = ClientReport()

            template = template_env.get_template("templates/dynamic/ratings/printglobal.html")
            context = {'thisClientReport':thisClientReport}
            self.response.write(template.render(context))



app = webapp2.WSGIApplication([
    ('/clientcheck/withid/.*', ClientCheckWithIDHandler),
    ('/sendreq/clientidcheck/.*', SendRequestForClientCheckHandler),
    ('/employees/rating/print/.*', PrintGlobalRatingHandler)


], debug=True)