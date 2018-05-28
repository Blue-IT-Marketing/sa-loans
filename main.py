 #!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

import datetime
from leads import Leads
from Employee import EmploymentDetails,EmployeeRegRequest
from database import UserRights
from profiles import Activity
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/index.html')
        context = {}
        self.response.write(template.render(context))
class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        """
            try creating a burn list and run the user against the burn list
        :return:
        """
        Guser = users.get_current_user()
        if Guser:
            findRequest = EmployeeRegRequest.query(EmployeeRegRequest.strReference == Guser.user_id())
            RequestList = findRequest.fetch()
            if len(RequestList) > 0:
                thisRequest = RequestList[0]
                template = template_env.get_template('templates/employees.html')
                context = {'thisRequest':thisRequest}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/employees.html')
                context = {}
                self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strReference = Guser.user_id()
            strIDNumber = self.request.get('vstrIDNumber')
            strSurname = self.request.get('vstrSurname')
            strFirstname = self.request.get('vstrFirstName')
            strEmail = Guser.email()

            findRequest = EmployeeRegRequest.query(EmployeeRegRequest.strReference == Guser.user_id())
            RequestList = findRequest.fetch()

            if len(RequestList) > 0:
                EmployeeReq = RequestList[0]
            else:
                EmployeeReq = EmployeeRegRequest()

            EmployeeReq.writeReference(strinput=strReference)
            EmployeeReq.writeIDNumber(strinput=strIDNumber)
            EmployeeReq.writeEmail(strinput=strEmail)
            EmployeeReq.writeFirstName(strinput=strFirstname)
            EmployeeReq.writeSurname(strinput=strSurname)
            EmployeeReq.put()
            self.response.write("Succesfully Sent our Employee Request")
        else:
            self.response.write("you are not logged in please login to create a request")
class LeadsHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:
            findRequests = Leads.query(Leads.strConverted == False)
            LeadsList = findRequests.fetch()

            findRequest = Leads.query(Leads.strConverted == True)
            CLeadsList = findRequest.fetch()

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            EmployList = findRequest.fetch()
            if len(EmployList) > 0:
                Employ = EmployList[0]
            else:
                Employ = EmploymentDetails()

            findRequest = UserRights.query(UserRights.strEmployeeCode == Employ.strEmployeeCode)
            RightsList = findRequest.fetch()

            if len(RightsList) > 0:
                Rights = RightsList[0]
            else:
                Rights = UserRights()

            if Rights.bolIsEmployee:
                template = template_env.get_template('templates/leads.html')
                context = {'LeadsList':LeadsList,'CLeadsList':CLeadsList,'Rights':Rights}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))



    def post(self):
        Guser = users.get_current_user()
        if Guser:
            vstrTitle = self.request.get('vstrTitle')
            logging.info(vstrTitle)
            vstrSurname = self.request.get('vstrSurname')
            vstrFullnames = self.request.get('vstrFullnames')
            vstrIDNumber = self.request.get('vstrIDNumber')
            vstrDateofBirth = self.request.get('vstrDateofBirth')
            vstrResidential = self.request.get('vstrResidential')
            vstrTownCity = self.request.get('vstrTownCity')
            logging.info(vstrTownCity)
            vstrCountry = self.request.get('vstrCountry')
            vstrProvince = self.request.get('vstrProvince')
            vstrPostalCode = self.request.get('vstrPostalCode')
            vstrTel = self.request.get('vstrTel')
            vstrCell = self.request.get('vstrCell')
            logging.info(vstrCell)
            vstrEmail = self.request.get('vstrEmail')
            vstrLeadNotes = self.request.get('vstrLeadNotes')
            vstrInterest = self.request.get('vstrInterest')

            findRequests = Leads.query(Leads.strIDNumber == vstrIDNumber)
            DuplicateLists = findRequests.fetch()

            if len(DuplicateLists) > 0:
                self.response.write("Lead has already been Captured")
            else:
                try:
                    thisLead = Leads()
                    logging.info("We have SUCCESFULLY CREATED LEAD CAPTURE CLASS")
                    thisLead.writeTitle(strinput=vstrTitle)
                    logging.info("Title Written")
                    thisLead.writeSurname(strinput=vstrSurname)
                    thisLead.writeNames(strinput=vstrFullnames)
                    thisLead.writeIDNumber(strinput=vstrIDNumber)
                    thisLead.writeDateOfBirth(strinput=vstrDateofBirth)
                    thisLead.writeResAddress(strinput=vstrResidential)
                    thisLead.writeCityTown(strinput=vstrTownCity)
                    thisLead.writeCountry(strinput=vstrCountry)
                    logging.info("Till Country")
                    thisLead.writeProvince(strinput=vstrProvince)
                    thisLead.writePostalCode(strinput=vstrPostalCode)
                    thisLead.writeTel(strinput=vstrTel)
                    thisLead.writeCell(strinput=vstrCell)
                    thisLead.writeEmail(strinput=vstrEmail)
                    logging.info("Till Email")

                    thisLead.writeLeadNotes(strinput=vstrLeadNotes)
                    thisLead.writeLeadInterests(strinput=vstrInterest)

                    findRequests = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
                    EmployeeList = findRequests.fetch()

                    if len(EmployeeList) > 0:
                        Employee = EmployeeList[0]
                        thisLead.writeEmployeeCode(strinput=Employee.strEmployeeCode)
                        thisLead.put()

                        thisActivity = Activity()
                        thisActivity.writeReference(strinput=Guser.user_id())
                        thisActivity.writeAction(strinput="Lead")
                        thisLeadLink = "/leads/sublead/" + str(thisLead.strIDNumber)
                        thisActivity.writeActionLink(strinput=thisLeadLink)
                        thisActivity.put()
                        self.response.write("Lead Capture Succesfully")
                    else:
                        self.response.write("Not Authorised to Capture Lead")
                except:
                    self.response.write("An Error Occured Capturing Lead")
        else:
            self.response.write("You are presently not logged in")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/register', RegisterHandler),
    ('/employees', RegisterHandler),
    ('/employees/leads', LeadsHandler),

], debug=True)
