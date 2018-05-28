import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
import datetime
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))



class Tasks(ndb.Expando):
    strReference = ndb.StringProperty()
    strToReference = ndb.StringProperty()

    strTaskURL = ndb.StringProperty()
    strTaskSubject = ndb.StringProperty()
    strTaskNote = ndb.StringProperty()
    strDateTimeCreated = ndb.DateTimeProperty(auto_now_add=True)
    strTaskCompleted = ndb.BooleanProperty(default=False)
    strDateTimeTaskCompleted = ndb.DateTimeProperty(auto_now=True)

    strTaskType = ndb.StringProperty(default="Admin") # Admin, Employee
    strTaskTarget = ndb.StringProperty(default="Admin") # Lead, Loan, Payment, Admin
    strTaskID = ndb.StringProperty()


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
    def writeTaskURL(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strTaskURL = strinput
                return True
            else:
                return False
        except:
            return False
    def writeTaskSubject(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strTaskSubject = strinput
                return True
            else:
                return False
        except:
            return False
    def writeTaskTarget(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if (strinput.lower() == "lead") or (strinput.lower() == "loan") or (strinput.lower() == "payment") or (strinput.lower() == "admin"):
                self.strTaskTarget = strinput
                return True
            else:
                return False
        except:
            return False
    def writeTaskNote(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strTaskNote = strinput
                return True
            else:
                return False
        except:
            return False
    def SetCompleteTask(self,strinput):
        try:
            if strinput == True:
                self.strTaskCompleted = True
                return True
            else:
                return False
        except:
            return False
    def writeTaskType(self,strinput):
        try:
            strinput = str(strinput)
            if (strinput.lower() == "admin"):
                self.strTaskType = strinput
                return True
            elif (strinput.lower() == "employee"):
                self.strTaskType = strinput
                return True
            else:
                return False
        except:
            return False
    def setTaskID(self):
        try:
            findRequest = Tasks.query()
            TaskList = findRequest.fetch()
            self.strTaskID = self.strReference + str(len(TaskList))
            return True
        except:
            return False



class TasksHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = Tasks.query(Tasks.strToReference == Guser.user_id())
            MyTasksList = findRequest.fetch()

            template = template_env.get_template('templates/dynamic/tasks/tasklist.html')
            context = {'MyTasksList': MyTasksList}
            self.response.write(template.render(context))


    def post(self):
        from Employee import EmploymentDetails
        Guser = users.get_current_user()
        if Guser:
            vstrTaskEmployeeCode = self.request.get('vstrTaskEmployeeCode')
            vstrTaskTarget = self.request.get('vstrTaskTarget')
            vstrTaskSubject = self.request.get('vstrTaskSubject')
            vstrTaskDescriptionBody = self.request.get('vstrTaskDescriptionBody')

            findQuery = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == vstrTaskEmployeeCode)
            TargetEmployeeList = findQuery.fetch()

            if len(TargetEmployeeList) > 0:
                TargetEmployee = TargetEmployeeList[0]
            else:
                TargetEmployee = EmploymentDetails()

            try:
                thisTask = Tasks()

                thisTask.writeReference(strinput=Guser.user_id())
                thisTask.writeToReference(strinput=TargetEmployee.strReference)
                thisTask.writeTaskType(strinput="Employee")
                thisTask.writeTaskTarget(strinput=vstrTaskTarget)
                thisTask.writeTaskSubject(strinput=vstrTaskSubject)
                thisTask.writeTaskNote(strinput=vstrTaskDescriptionBody)
                if vstrTaskTarget.lower() == "loan":
                    thisTask.writeTaskURL(strinput="/employees/loans")
                elif vstrTaskTarget.lower() == "leads":
                    thisTask.writeTaskURL(strinput="/employees/leads")
                elif vstrTaskTarget.lower() == "payments":
                    thisTask.writeTaskURL(strinput="/employees/payments")
                elif vstrTaskTarget.lower() == "admin":
                    thisTask.writeTaskURL(strinput="/employees/admin")

                thisTask.setTaskID()
                thisTask.put()

                self.response.write("Succesfully Created Task, TaskID : " + thisTask.strTaskID)
            except:
                self.response.write("Failed to create Task Subject : " + vstrTaskSubject)
        else:
            pass


class RemoveTasksHandler(webapp2.RequestHandler):

    def get(self):

        try:
            Guser = users.get_current_user()

            if Guser:

                URL = self.request.uri
                URL = str(URL)
                URLlist = URL.split("/")
                strTaskID = URLlist[len(URLlist) - 1]
                findRequest = Tasks.query(Tasks.strTaskID == strTaskID)
                TaskList = findRequest.fetch()

                if len(TaskList) > 0:
                    thisTasks = TaskList[0]
                    thisTasks.key.delete()
                else:
                    pass

                self.response.write("Task Removed Succesfully")
            else:
                self.response.write("Unable to remove Task")
        except:
            self.response.write("Error Removing Task")



class TasksReloadHandler(webapp2.RequestHandler):
    def get(self):
        from Employee import EmploymentDetails
        Guser = users.get_current_user()
        if Guser:
            vstrEmployeeCode = self.request.get('vstrEmployeeCode')

            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == vstrEmployeeCode)
            thisEmployeeList = findRequest.fetch()

            if len(thisEmployeeList) > 0:
                thisEmployee = thisEmployeeList[0]
            else:
                thisEmployee = EmploymentDetails()

            findRequest = Tasks.query(Tasks.strToReference == thisEmployee.strReference)
            thisTasksList = findRequest.fetch()

            template = template_env.get_template('templates/dynamic/employee/adminTasks.html')
            context = {'thisTasksList':thisTasksList}
            self.response.write(template.render(context))


class TasksOpenHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            URL = self.request.uri
            URLlist = URL.split("/")
            vstrTaskID = URLlist[len(URLlist) - 1]

            findRequest = Tasks.query(Tasks.strTaskID == vstrTaskID)
            thisTaskList = findRequest.fetch()

            if len(thisTaskList) > 0:
                thisTask = thisTaskList[0]
            else:
                thisTask = Tasks()

            template = template_env.get_template('templates/dynamic/tasks/Task.html')
            context = {'thisTask':thisTask}
            self.response.write(template.render(context))


app = webapp2.WSGIApplication([
    ('/tasks', TasksHandler),
    ('/tasks/remove/.*', RemoveTasksHandler),
    ('/tasks/reload', TasksReloadHandler),
    ('/tasks/open/.*', TasksOpenHandler)

], debug=True)
