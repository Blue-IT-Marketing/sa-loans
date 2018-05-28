
import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
import datetime
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
from Employee import EmploymentDetails
from tasks import Tasks
from database import UserRights
class Activity(ndb.Expando):
    strReference = ndb.StringProperty() # Reference of the User this Timeline Entry Refers to
    strAction = ndb.StringProperty() # Leads, Loans, Credit Checks, Payments
    strTimeActionTaken = ndb.DateTimeProperty(auto_now_add=True)
    strActionLink = ndb.StringProperty()
    strComments = ndb.StringProperty(repeated=True)

    def writeReference(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strReference = strinput
                return True
            else:
                return False
        except:
            return False
    def writeAction(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strAction = strinput
                return True
            else:
                return False

        except:
            return False
    def writeActionLink(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strActionLink = strinput
                return True
            else:
                return False
        except:
            return False


class TimeLine(ndb.Expando):
    strReference = ndb.StringProperty()
    strToReference = ndb.StringProperty()
    strEventType = ndb.StringProperty() # Message, Notification, Task
    strEventLink = ndb.StringProperty()


    def writeReference(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strReference = strinput
                return True
            else:
                return False
        except:
            return False

    def writeToReference(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strToReference = strinput
                return True
            else:
                return False
        except:
            return False

    def writeEventType(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strEventType = strinput
                return True
            else:
                return False
        except:
            return False
    def writeEventLink(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strEventLink = strinput
                return True
            else:
                return False
        except:
            return False

class EmployeeProfilesHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:

            logging.info("Employee Profiles")

            findRequest =  Activity.query(Activity.strReference == Guser.user_id())
            thisActivityList = findRequest.fetch()

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            thisEmployeeList = findRequest.fetch()

            if len(thisEmployeeList) > 0:
                thisEmployee = thisEmployeeList[0]
            else:
                thisEmployee = EmploymentDetails()

            findRequest = Tasks.query(Tasks.strToReference == Guser.user_id())
            thisTasksList = findRequest.fetch()

            TotalTasks = len(thisTasksList)

            findRequest = UserRights.query(UserRights.strReference == Guser.user_id())
            thisUserRightsList = findRequest.fetch()

            if len(thisUserRightsList) > 0:
                thisUserRights = thisUserRightsList[0]
            else:
                thisUserRights = UserRights()

            if thisUserRights.bolIsEmployee:
                template = template_env.get_template('templates/dynamic/employee/Profile.html')
                context = {'thisActivityList':thisActivityList,'thisEmployee':thisEmployee,'TotalTasks': TotalTasks}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = UserRights.query(UserRights.strReference == Guser.user_id())
            thisUserRightsList = findRequest.fetch()

            if len(thisUserRightsList) > 0:
                thisUserRights = thisUserRightsList[0]
            else:
                thisUserRights = UserRights()

            if thisUserRights.bolIsEmployee and thisUserRights.bolAccessToEmployeesAdminForm:
                findRequest = EmploymentDetails.query()
                thisEmployeeList = findRequest.fetch()
                vstrIndexControl = self.request.get('vstrIndexControl')
                if vstrIndexControl.isalpha():
                    vstrIndexControl = int(vstrIndexControl)

                if vstrIndexControl < len(thisEmployeeList):
                    thisEmployee = thisEmployeeList[vstrIndexControl]
                else:
                    thisEmployee = thisEmployeeList[len(thisEmployeeList) - 1]




                findRequest = Activity.query(Activity.strReference == thisEmployee.strReference)
                thisActivityList = findRequest.fetch()

                if len(thisActivityList) > 0:
                    thisActivity = thisActivityList[0]
                else:
                    thisActivity = Activity()
                template = template_env.get_template('templates/dynamic/employee/browseprofiles.html')
                context = {'thisEmployee':thisEmployee,'thisActivity':thisActivity}
                self.response.write(template.render(context))







app = webapp2.WSGIApplication([
    ('/employees/profiles', EmployeeProfilesHandler)


], debug=True)
