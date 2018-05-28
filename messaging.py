import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

from Employee import *
from profiles import  TimeLine
import re

def verifyEmail(addressToVerify):
    try:
        match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
        if match == None:
            return False
        else:
            return True
    except:
        return False


def sendEmail():
    pass

class Messages(ndb.Expando):
    strMessageIndex = ndb.IntegerProperty()
    strEmployeeCode = ndb.StringProperty()
    strMessageHeading = ndb.StringProperty()
    strMessageBody =ndb.StringProperty()
    strIsDraft = ndb.BooleanProperty(default=False)
    strMessageDelete = ndb.BooleanProperty(default=False)
    strDateTimeDeleted = ndb.DateTimeProperty()

    strMessageFromReference = ndb.StringProperty()
    strDateTimeSent = ndb.DateTimeProperty(auto_now_add=True)
    strMessageSent = ndb.BooleanProperty(default=False)

    def writeMessageHeading(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strMessageHeading = strinput
                return True
            else:
                return False
        except:
            return False
    def writeMessageBody(self,strinput):
        try:
            strinput = str(strinput)

            if not (strinput == None):
                self.strMessageBody = strinput
                return True
            else:
                return False
        except:
            return False
    def writeMessageFromReference(self,strinput):
        try:
            strinput = str(strinput)

            if not (strinput == None):
                self.strMessageFromReference = strinput
                return True
            else:
                return False
        except:
            return False
    def writeEmployeeCode(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not (strinput == None):
                self.strEmployeeCode = strinput
                return True
            else:
                return False
        except:
            return False
    def setIndex(self):
        try:

            findRequest = Messages.query()
            thisMessagesList = findRequest.fetch()
            self.strMessageIndex = len(thisMessagesList)
            return True
        except:
            return False
    def setDraft(self):
        try:
            self.strIsDraft = True
            return True
        except:
            return False
    def setMessageSent(self):
        try:
            self.strMessageSent = True
            return True
        except:
            return False


class SendMessagingHandler(webapp2.RequestHandler):

    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrEmployeeCode = self.request.get('vstrEmployeeCode')

            findRequest = Messages.query(Messages.strEmployeeCode == vstrEmployeeCode)
            thisMessagesList = findRequest.fetch()

            template = template_env.get_template('templates/dynamic/employee/adminMessages.html')
            context = {'thisMessagesList':thisMessagesList}
            self.response.write(template.render(context))


    def post(self):
        try:
            Guser = users.get_current_user()

            strEmployeeCode = self.request.get('vstrEmployeeCode')
            strMessageHeading = self.request.get('vstrSubject')
            strMessageBody = self.request.get('vstrMessageBody')

            Employee = EmploymentDetails()
            Message = Messages()

            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            TempEmployeeList = findRequest.fetch()

            if len(TempEmployeeList) > 0:
                Employee = TempEmployeeList[0]
            else:
                self.redirect('/admin')

            Employee.strTotalMessages = Employee.strTotalMessages + 1
            Employee.put()
            Message.writeEmployeeCode(strinput=strEmployeeCode)
            Message.writeMessageBody(strinput=strMessageBody)
            Message.writeMessageHeading(strinput=strMessageHeading)
            Message.writeMessageFromReference(strinput=Guser.user_id())

            findRequest = Messages.query()
            thisMessagesList = findRequest.fetch()
            Message.strMessageIndex = len(thisMessagesList)
            Message.setMessageSent()
            Message.put()

            thisTimeLine = TimeLine()
            thisTimeLine.writeReference(strinput=Guser.user_id())
            thisTimeLine.writeToReference(strinput=Employee.strReference)
            thisTimeLine.writeEventType(strinput="Message")
            thisEventLink =  ""
            thisTimeLine.writeEventLink(strinput=thisEventLink)
            thisTimeLine.put()


            thisURL = "/admin/employees/" + strEmployeeCode
            self.redirect(thisURL)

        except:
            self.redirect('/')






class SMSMessageTemplatesHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:

            template = template_env.get_template('templates/dynamic/contact/MessageTemplates.html')
            context = {}
            self.response.write(template.render(context))


class InboxHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest =  EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            thisEmployeeList = findRequest.fetch()

            if len(thisEmployeeList) > 0:
                thisEmployee = thisEmployeeList[0]
            else:
                thisEmployee = EmploymentDetails()

            findRequest = Messages.query(Messages.strEmployeeCode == thisEmployee.strEmployeeCode)
            MessageList = findRequest.fetch()

            template = template_env.get_template('templates/inbox.html')
            context = {'MessageList': MessageList,'thisEmployee':thisEmployee}
            self.response.write(template.render(context))

class InboxMessagesReadHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            URL = self.request.uri
            URL = str(URL)
            URLlist = URL.split("/")
            vstrMessageIndex = URLlist[len(URLlist) - 1]

            if vstrMessageIndex.isdigit():
                vstrMessageIndex = int(vstrMessageIndex)
            else:
                vstrMessageIndex = 0

            findRequest = Messages.query(Messages.strMessageIndex == vstrMessageIndex)
            thisMessageList = findRequest.fetch()

            if len(thisMessageList) > 0:
                thisMessage = thisMessageList[0]
            else:
                thisMessage = Messages()


            template = template_env.get_template('templates/dynamic/messaging/read-mail.html')
            context = {'thisMessage':thisMessage}
            self.response.write(template.render(context))




class ComposeMessageHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:

            findRequests = UserRights.query(UserRights.strReference == Guser.user_id())
            thisUserRightsList = findRequests.fetch()

            if len(thisUserRightsList) > 0:
                thisUserRights = thisUserRightsList[0]
            else:
                thisUserRights = UserRights()


            if thisUserRights.bolIsEmployee:

                template = template_env.get_template('templates/dynamic/messaging/compose.html')
                context = {}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()
        if Guser:
            vstrComposeText = self.request.get('vstrComposeText')
            vstrSubject = self.request.get('vstrSubject')
            vstrToAddress = self.request.get('vstrToAddress')
            vstrIsDraft = self.request.get('vstrIsDraft')



            if verifyEmail(addressToVerify=vstrToAddress):
                sendEmail()
            else:

                findrequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
                thisEmployeeList  = findrequest.fetch()
                if len(thisEmployeeList) > 0:
                    thisEmployee = thisEmployeeList[0]
                else:
                    thisEmployee = EmploymentDetails()

                try:
                    if vstrIsDraft == True:
                        thisMessage = Messages()

                        thisMessage.writeEmployeeCode(strinput=vstrToAddress)
                        thisMessage.writeMessageFromReference(strinput=Guser.user_id())
                        thisMessage.writeMessageHeading(strinput=vstrSubject)
                        thisMessage.writeMessageBody(strinput=vstrComposeText)
                        findRequest = Messages.query()
                        MessageList = findRequest.fetch()

                        thisMessage.strMessageIndex = len(MessageList)
                        thisMessage.setDraft()
                        thisMessage.put()
                        thisEmployee.strTotalDrafts = thisEmployee.strTotalDrafts + 1
                        thisEmployee.put()

                        findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == vstrToAddress)
                        RecEmployeeList = findRequest.fetch()

                        RecEmployee = RecEmployeeList[0]

                        thisTimeLine = TimeLine()
                        thisTimeLine.writeReference(strinput=Guser.user_id())
                        thisTimeLine.writeToReference(strinput=RecEmployee.strReference)
                        thisTimeLine.writeEventType(strinput="Message")
                        thisEventLink = ""
                        thisTimeLine.writeEventLink(strinput=thisEventLink)
                        thisTimeLine.put()
                    else:
                        thisMessage = Messages()

                        thisMessage.writeEmployeeCode(strinput=vstrToAddress)
                        thisMessage.writeMessageFromReference(strinput=Guser.user_id())
                        thisMessage.writeMessageHeading(strinput=vstrSubject)
                        thisMessage.writeMessageBody(strinput=vstrComposeText)
                        findRequest = Messages.query()
                        MessageList = findRequest.fetch()

                        thisMessage.strMessageIndex = len(MessageList)
                        thisMessage.setMessageSent()
                        thisMessage.put()

                        thisEmployee.strTotalSent = thisEmployee.strTotalSent + 1
                        thisEmployee.put()

                        findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == vstrToAddress)
                        RecEmployeeList = findRequest.fetch()

                        RecEmployee = RecEmployeeList[0]

                        thisTimeLine = TimeLine()
                        thisTimeLine.writeReference(strinput=Guser.user_id())
                        thisTimeLine.writeToReference(strinput=RecEmployee.strReference)
                        thisTimeLine.writeEventType(strinput="Message")
                        thisEventLink = ""
                        thisTimeLine.writeEventLink(strinput=thisEventLink)
                        thisTimeLine.put()

                        self.response.write("Message Successfully Sent To Recipient : " + vstrToAddress)
                except:
                    self.response.write("Error Sending Message to Recipient : " + vstrToAddress)


class DeleteMessageHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrMessageIndex = self.request.get('vstrMessageIndex')
            vstrMessageIndex = int(vstrMessageIndex)

            findRequest = Messages.query(Messages.strMessageIndex == vstrMessageIndex)
            thisMessagesList = findRequest.fetch()

            for thisMessage in thisMessagesList:
                thisMessage.strMessageDelete = True
                thisNow = datetime.datetime.now()
                thisMessage.strDateTimeDeleted = thisNow
                thisMessage.put()



            self.response.write("Message Succesfully Sent to Trash")

app = webapp2.WSGIApplication([
    ('/admin/employees/messaging', SendMessagingHandler ),
    ('/admin/sms/templates', SMSMessageTemplatesHandler),
    ('/inbox', InboxHandler),
    ('/inbox/messages/read/.*', InboxMessagesReadHandler),
    ('/inbox/compose', ComposeMessageHandler),
    ('/inbox/messages/delete', DeleteMessageHandler)




], debug=True)


