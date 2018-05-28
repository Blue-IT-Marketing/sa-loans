import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

from profiles import Activity
from loans import LoanApplicantDetails, AdvancedAmount
from database import UserRights
class Ratings(ndb.Expando):
    strIDNumber = ndb.StringProperty()
    strIncomePredictor = ndb.IntegerProperty(default=100)
    strCreditConfidence =  ndb.IntegerProperty(default=100)
    strEmploymentConfidenceIndex = ndb.IntegerProperty(default=100)


    def writeIDNumber(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strIDNumber = strinput
                return True
            else:
                return False

        except:
            return False

class ClientHistory(ndb.Expando):
    strIDNumber = ndb.StringProperty()

class CreditRatingHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = UserRights.query(UserRights.strReference == Guser.user_id())
            thisUserRightsList = findRequest.fetch()

            if len(thisUserRightsList) > 0:
                thisUserRights = thisUserRightsList[0]
            else:
                thisUserRights = UserRights()

            if thisUserRights.bolIsEmployee:
                template = template_env.get_template('templates/dynamic/ratings/credit.html')
                context = {}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()
        if Guser:
            vstrIDNumber = self.request.get('vstrIDNumber')

            findRequest = Ratings.query(Ratings.strIDNumber == vstrIDNumber)
            RatingList = findRequest.fetch()

            if len(RatingList) > 0:
                thisRating = RatingList[0]
            else:
                thisRating = Ratings()
                thisRating.writeIDNumber(strinput=vstrIDNumber)
                thisRating.put()

            thisActivity = Activity()
            thisActivity.writeReference(strinput=Guser.user_id())
            thisActivity.writeAction(strinput="Credit Rating")
            thisLeadLink = "/employees/rating/" + str(thisRating.strIDNumber)
            thisActivity.writeActionLink(strinput=thisLeadLink)
            thisActivity.put()

            template = template_env.get_template('templates/dynamic/ratings/clientRating.html')
            context = {'thisRating':thisRating}
            self.response.write(template.render(context))


class ClientHistoryHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrIDNumber = self.request.get('vstrIDNumber')

            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strIDNumber == vstrIDNumber)
            thisLoanApplicantList = findRequest.fetch()

            if len(thisLoanApplicantList) > 0:
                thisLoanApplicant = thisLoanApplicantList[0]
            else:
                thisLoanApplicant = LoanApplicantDetails()

            findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == thisLoanApplicant.strAccountNumber)
            thisAdvanceList = findRequest.fetch()


            findRequest = UserRights.query(UserRights.strReference == Guser.user_id())
            thisUserRightsList = findRequest.fetch()

            if len(thisUserRightsList) > 0:
                thisUserRights = thisUserRightsList[0]
            else:
                thisUserRights = UserRights()


            if thisUserRights.bolIsEmployee:
                if len(thisAdvanceList) > 0:
                    template = template_env.get_template('templates/dynamic/ratings/History.html')
                    context = {'thisAdvanceList': thisAdvanceList,'thisLoanApplicant':thisLoanApplicant }
                    self.response.write(template.render(context))
                else:
                    template = template_env.get_template('templates/dynamic/ratings/History.html')
                    context = {'Message':"Client has no history"}
                    self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))
        else:
            template = template_env.get_template('templates/500.html')
            context = {}
            self.response.write(template.render(context))


class HistoryRatingHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            URL = self.request.uri
            URLlist = URL.split("/")
            vstrIDNumber = URLlist[len(URLlist) -1]



            findRequest = Ratings.query(Ratings.strIDNumber == vstrIDNumber)
            RatingList = findRequest.fetch()

            if len(RatingList) > 0:
                thisRating = RatingList[0]
            else:
                thisRating = Ratings()
                thisRating.writeIDNumber(strinput=vstrIDNumber)
                thisRating.put()


            template = template_env.get_template('templates/dynamic/ratings/CreditRatingHistory.html')
            context = {'thisRating': thisRating}
            self.response.write(template.render(context))

app = webapp2.WSGIApplication([
    ('/employees/rating', CreditRatingHandler),
    ('/loans/history', ClientHistoryHandler),
    ('/employees/rating/.*', HistoryRatingHandler)

], debug=True)