

import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
import datetime
from Employee import *
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))




class Chats(ndb.Expando):
    strOwnerReference = ndb.StringProperty()
    strOwnerNick = ndb.StringProperty()
    strRecipientReference = ndb.StringProperty()
    strRecipientNick = ndb.StringProperty()
    strChatID = ndb.StringProperty()


    def writeOwnerReference(self, strinput):
        try:

            strinput = str(strinput)
            if not(strinput == None):
                self.strOwnerReference = strinput
                return True
            else:
                return False
        except:
            return False
    def writeRecipientReference(self, strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strRecipientReference = strinput
                return True
            else:
                return False

        except:
            return False
    def writeChatID(self,thisUser,remoteUser):
        try:

            thisUserArray = str(thisUser)
            remoteUserArray = str(remoteUser)
            b = ""
            b = str(b)

            for i in range(len(thisUserArray)):
                c = int(thisUserArray[i]) + int(remoteUserArray[i])
                b = b + str(c)

            self.strChatID =b
            return True
        except:
            return False
    def writeOwnerNick(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strOwnerNick = strinput
                return True
            else:
                return False
        except:
            return False
    def writeRecipientNick(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strRecipientNick = strinput
                return True
            else:
                return False
        except:
            return False
class Messages(ndb.Expando):
    strChatID = ndb.StringProperty()
    strIsOwner = ndb.BooleanProperty()
    strMessage = ndb.StringProperty()
    strTimeStamp = ndb.DateTimeProperty(auto_now_add=True)
    strMessageIndex = ndb.IntegerProperty(default=0)

    def writeChatID(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strChatID = strinput
                return True
            else:
                return False

        except:
            return False
    def writeMessage(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strMessage = strinput
                return True
            else:
                return False
        except:
            return False
    def writeIsOwner(self,strinput):
        try:
            if strinput == True:
                self.strIsOwner = True
                return True
            elif strinput == False:
                self.strIsOwner = False
                return True
            else:
                return False
        except:
            return False
class ChatsHandler(webapp2.RequestHandler):

    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = EmploymentDetails.query()
            MyContacts = findRequest.fetch()


            template = template_env.get_template('templates/chats.html')
            context = {'MyContacts':MyContacts}
            self.response.write(template.render(context))

class UserChatsHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            strEmployeeCode = self.request.get('vstrEmployeeCode')


            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            EmployeeList = findRequest.fetch()
            if len(EmployeeList) > 0:
                Employee = EmployeeList[0]
            else:
                Employee = EmploymentDetails()

            findRequest = Chats.query(Chats.strOwnerReference == Guser.user_id(), Chats.strRecipientReference == Employee.strReference)
            ChatList = findRequest.fetch()

            if len(ChatList) > 0:
                MyChats = ChatList[0]

            else:
                MyChats = Chats()
                MyChats.writeOwnerNick(strinput=Guser.nickname())
                MyChats.writeOwnerReference(strinput=Guser.user_id())
                MyChats.writeChatID(thisUser=Guser.user_id(),remoteUser=Employee.strReference)
                MyChats.writeRecipientNick(strinput=Employee.strFullNames)
                MyChats.writeRecipientReference(strinput=Employee.strReference)
                MyChats.put()

            MyMessages = Messages()
            MyMessages.writeChatID(MyChats.strChatID)
            MyMessages.writeIsOwner(strinput=True)
            findRequest = Messages.query(Messages.strChatID == MyChats.strChatID)
            MessagesList = findRequest.fetch()
            MyMessages.strMessageIndex = len(MessagesList)
            MyMessages.put()


            findRequest = Messages.query(Messages.strChatID == MyChats.strChatID)
            MessagesList = findRequest.fetch()
            vstrMessagesCount = len(MessagesList)
            sorted(MessagesList,key=lambda Messages: Messages.strMessageIndex)

            template = template_env.get_template('templates/dynamic/chats/chatmessages.html')
            context = {'MessagesList': MessagesList,'MyChats':MyChats,'vstrMessagesCount':vstrMessagesCount}
            self.response.write(template.render(context))

class SendMessageHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrChatID = self.request.get('vstrChatID')
            vstrChatMessage = self.request.get('vstrChatMessage')

            SendMessage = Messages()
            SendMessage.writeChatID(strinput=vstrChatID)
            SendMessage.writeMessage(strinput=vstrChatMessage)

            findRequest = Chats.query(Chats.strChatID == vstrChatID)
            ChatsList = findRequest.fetch()
            if len(ChatsList) > 0:
                thisChats = ChatsList[0]
            else:
                thisChats = Chats()

            if thisChats.strOwnerReference == Guser.user_id():

                SendMessage.writeIsOwner(strinput=True)
            else:
                SendMessage.writeIsOwner(strinput=False)

            findRequest = Messages.query(Messages.strChatID == vstrChatID)
            MessagesList = findRequest.fetch()
            SendMessage.strMessageIndex = len(MessagesList)
            SendMessage.put()

            findRequest = Messages.query(Messages.strChatID == vstrChatID)
            MessagesList = findRequest.fetch()
            vstrMessagesCount = len(MessagesList)

            findRequest = Chats.query(Chats.strChatID == vstrChatID)
            MyChatsList = findRequest.fetch()

            if len(MyChatsList) > 0:
                MyChats = MyChatsList[0]
            else:
                MyChats = Chats()


            template = template_env.get_template('templates/dynamic/chats/chatmessages.html')
            context = {'MessagesList':MessagesList,'MyChats':MyChats,'vstrMessagesCount':vstrMessagesCount}
            self.response.write(template.render(context))


app = webapp2.WSGIApplication([
    ('/chats', ChatsHandler),
    ('/chats/employees/.*', UserChatsHandler),
    ('/chats/sendmessage', SendMessageHandler)

], debug=True)