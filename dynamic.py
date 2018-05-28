

import os
import webapp2
import jinja2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
from database import  WorkingAccount

from Employee import BranchDetails,EmploymentDetails, PostalAddress, ResidentialAddress,BankingDetails,ContactDetails

from database import UserRights


class AmountPayableDynamicHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/dynamic/funeralpolicy/AmountPayableSummary.html')
        context = {}
        self.response.write(template.render(context))
class PaymentDetailsDynamicHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/funeral/paymentdetails/payroll')
        logging.info(upload_url)
        template = template_env.get_template('templates/dynamic/funeralpolicy/PaymentDetails.html')
        context = {'payroll_upload': upload_url}
        self.response.write(template.render(context))
class EditBranchHandler(webapp2.RequestHandler):
    def get(self):
        logging.info(msg="Edit Branch Handler Was Called")
        Guser = users.get_current_user()
        if Guser:
            findQuery = BranchDetails.query()
            results = findQuery.fetch()

            if len(results) > 0:
                branchdet = results
            else:
                branchdet = []

            template = template_env.get_template('templates/dynamic/admin/editbranch.html')
            context = {'branches': branchdet }
            self.response.write(template.render(context))
        else:
            pass

    def post(self):
        logging.info(msg="Branch Saving Data")
        Guser = users.get_current_user()
        if Guser:
            strBranchName = self.request.get('vstrBranchName')
            strBranchCode = self.request.get('vstrBranchCode')
            strBranchAddress = self.request.get('vstrBranchAddress')
            strBranchContact = self.request.get('vstrBranchContact')
            strBranchEmail = self.request.get('vstrBranchEmail')
            strBranchManager = self.request.get('vstrBranchManager')
            strBranchManagerContact = self.request.get('vstrBranchManagerContact')
            strBranchManagerEmail = self.request.get('vstrBranchManagerEmail')

            newBranch = BranchDetails()

            findRequest = BranchDetails.query(BranchDetails.strCompanyBranchCode == strBranchCode)
            TempBranchList = findRequest.fetch()

            if len(TempBranchList) > 0:
                newBranch = TempBranchList[0]

            if newBranch.writeCompanyBranchName(strBranchName) and newBranch.writeCompanyBranchCode(strBranchCode):
                newBranch.writeReference(strinput=Guser.user_id())
                newBranch.writeCompanyBranchTel(strinput=strBranchContact)
                newBranch.writeCompanyBranchAddress(strinput=strBranchAddress)
                newBranch.writeCompanyBranchEmail(strinput=strBranchEmail)
                newBranch.writeBranchManagerName(strinput=strBranchManager)
                newBranch.writeBranchManagerTel(strinput=strBranchManagerContact)
                newBranch.writeBranchManagerEmail(strinput=strBranchManagerEmail)
                newBranch.put()
                self.redirect("/admin")
            else:
                self.redirect("/admin")
        else:
            self.redirect("/admin")
class EditEmployeesHandler(webapp2.RequestHandler):

    def get(self):
        logging.info(msg="Edit Employees Handler was called")
        Guser = users.get_current_user()

        if Guser:
            findQuery = EmploymentDetails.query()
            results = findQuery.fetch()

            if len(results) > 0:
                employeesdet = results
            else:
                employeesdet = []

            findQuery = BranchDetails.query()
            results = findQuery.fetch()

            if len(results) > 0:
                branchdet = results
            else:
                branchdet = []

            template = template_env.get_template('templates/dynamic/admin/editemployees.html')
            context = {'employees': employeesdet,
                       'branches': branchdet}
            self.response.write(template.render(context))
        else:
            pass

    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strBranchCode = self.request.get('vstrBranchCode')
            strEmployeeCode = self.request.get('vstrEmployeeCode')
            strContractType = self.request.get('vstrContractType')
            strBasicSalary = self.request.get('vstrBasicSalary')
            strDateOfEmployment = self.request.get('vstrDateOfEmployment')
            strTitle = self.request.get('vstrTitle')
            strFullnames = self.request.get('vstrFullnames')
            strSurname = self.request.get('vstrSurname')
            strIDNumber = self.request.get('vstrIDNumber')
            strDateOfBirth = self.request.get('vstrDateOfBirth')
            strNationality = self.request.get('vstrNationality')
            strPhysicalAddressL1 = self.request.get('vstrPhysicalAddressL1')
            strPhysicalAddressL2 = self.request.get('vstrPhysicalAddressL2')
            strCityTown = self.request.get('vstrCityTown')
            strProvince  = self.request.get('vstrProvince')
            strPhysicalPostalCode = self.request.get('vstrPhysicalPostalCode')
            strPostalAddressL1 = self.request.get('vstrPostalAddressL1')
            strPostalAddressL2 = self.request.get('vstrPostalAddressL2')
            strPostalCityTown = self.request.get('vstrPostalCityTown')
            strPostalProvince = self.request.get('vstrPostalProvince')
            strPostalCode = self.request.get('vstrPostalCode')

            strAccountHolder = self.request.get('vstrAccountHolder')
            strBankName = self.request.get('vstrBankName')
            strAccountType = self.request.get('vstrAccountType')
            strAccountNumber = self.request.get('vstrAccountNumber')
            strBankBranchCode = self.request.get('vstrBankBranchCode')

            strCell = self.request.get('vstrCell')
            strTel = self.request.get('vstrTel')
            strEmail = self.request.get('vstrEmail')

            vstrIsEmployee = self.request.get('vstrIsEmployee')
            vstrAccessEmployeeAdmin = self.request.get('vstrAccessEmployeeAdmin')
            vstrSearchLoans = self.request.get('vstrSearchLoans')
            vstrEditLoans = self.request.get('vstrEditLoans')
            vstrSearchLeadsForm =  self.request.get('vstrSearchLeadsForm')
            vstrEditLeadsForm = self.request.get('vstrEditLeadsForm')
            vstrDeleteLoans = self.request.get('vstrDeleteLoans')
            vstrLoanReprint = self.request.get('vstrReprintLoans')
            vstrProcessPayment = self.request.get('vstrProcessPayment')
            vstrSendPayment = self.request.get('vstrSendPayment')


            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            EmpResult = findRequest.fetch()

            if len(EmpResult) > 0:
                Employee = EmpResult[0]
            else:
                Employee = EmploymentDetails()


            try:
                Employee.writeEmployeeCode(strinput=strEmployeeCode)
                Employee.writeBranchWorking(strinput=strBranchCode)
                Employee.writeContractType(strinput=strContractType)
                Employee.writeBasicSalary(strinput=strBasicSalary)
                Employee.writeDateOfEmployment(strinput=strDateOfEmployment)
                Employee.writeTitle(strinput=strTitle)
                Employee.writeNames(strinput=strFullnames)
                Employee.writeSurname(strinput=strSurname)
                Employee.writeIDNumber(strinput=strIDNumber)
                Employee.writeDateOfBirth(strinput=strDateOfBirth)
                Employee.writeNationality(strinput=strNationality)

                Employee.put()
            except:
                pass

            findRequest = ResidentialAddress.query(ResidentialAddress.strEmployeeCode == strEmployeeCode)
            PhysicalResult = findRequest.fetch()


            if len(PhysicalResult) > 0:
                PhysicalAddress = PhysicalResult[0]
            else:
                PhysicalAddress = ResidentialAddress()

            try:
                PhysicalAddress.writeEmployeeCode(strinput=strEmployeeCode)
                PhysicalAddress.writeResAddressL1(strinput=strPhysicalAddressL1)
                PhysicalAddress.writeResAddressL2(strinput=strPhysicalAddressL2)
                PhysicalAddress.writeCityTown(strinput=strCityTown)
                PhysicalAddress.writeProvince(strinput=strProvince)
                PhysicalAddress.writePostalCode(strinput=strPhysicalPostalCode)

                PhysicalAddress.put()
            except:
                pass

            findRequest = PostalAddress.query(PostalAddress.strEmployeeCode == strEmployeeCode)
            PostalList = findRequest.fetch()


            if len(PostalList) > 0:
                PostalAddy = PostalList[0]
            else:
                PostalAddy = PostalAddress()

            try:
                PostalAddy.writeEmployeeCode(strinput=strEmployeeCode)
                PostalAddy.writePostalAddressL1(strinput=strPostalAddressL1)
                PostalAddy.writePostalAddressL2(strinput=strPostalAddressL2)
                PostalAddy.writeTownCity(strinput=strPostalCityTown)
                PostalAddy.writeProvince(strinput=strPostalProvince)
                PostalAddy.writePostalCode(strinput=strPostalCode)

                PostalAddy.put()
            except:
                pass

            findRequest = ContactDetails.query(ContactDetails.strEmployeeCode == strEmployeeCode)
            ContactList = findRequest.fetch()

            if len(ContactList) > 0:
                Contacts = ContactList[0]
            else:
                Contacts = ContactDetails()
            try:
                Contacts.writeEmployeeCode(strinput=strEmployeeCode)
                Contacts.writeCell(strinput=strCell)
                Contacts.writeTel(strinput=strTel)
                Contacts.writeEmail(strinput=strEmail)


                Contacts.put()
            except:
                pass


            findRequester = BankingDetails.query(BankingDetails.strEmployeeCode == strEmployeeCode)
            BankingList = findRequester.fetch()

            if len(BankingList) > 0:
                Banking = BankingList[0]
            else:
                Banking = BankingDetails()


            try:
                Banking.writeEmployeeCode(strinput=strEmployeeCode)
                Banking.writeAccountHolder(strinput=strAccountHolder)
                Banking.writeAccountNumber(strinput=strAccountNumber)
                Banking.writeAccountType(strinput=strAccountType)
                Banking.writeBankName(strinput=strBankName)
                Banking.writeBranchCode(strinput=strBankBranchCode)

                Banking.put()
            except:
                pass

            findRequest = WorkingAccount.query(WorkingAccount.strReference == Employee.strReference)
            AllOpenPolicies = findRequest.fetch()
            try:
                for OpenPols in AllOpenPolicies:
                    OpenPols.strActivated = True
                    OpenPols.put()
            except:
                pass

            findRequest = UserRights.query(UserRights.strReference == Employee.strReference)
            UserRightsList = findRequest.fetch()

            if len(UserRightsList) > 0:
                EmployeeRights = UserRightsList[0]

                EmployeeRights.writeEmployeeCode(strinput=strEmployeeCode)
                if vstrIsEmployee == "YES":
                    EmployeeRights.bolIsEmployee = True
                else:
                    EmployeeRights.bolIsEmployee = False

                if vstrAccessEmployeeAdmin == "YES":
                    EmployeeRights.bolAccessToEmployeesAdminForm = True
                else:
                    EmployeeRights.bolAccessToEmployeesAdminForm = False

                if vstrSearchLoans == "YES":
                    EmployeeRights.bolEmployeesLoanFormReadAccess = True
                else:
                    EmployeeRights.bolEmployeesLoanFormReadAccess = False

                if vstrEditLoans == "YES":
                    EmployeeRights.bolEmployeesLoanFormWriteAccess = True
                else:
                    EmployeeRights.bolEmployeesLoanFormWriteAccess = False

                if vstrSearchLeadsForm == "YES":
                    EmployeeRights.bolEmployeesLeadsFormReadAccess = True
                else:
                    EmployeeRights.bolEmployeesLeadsFormReadAccess = False

                if vstrEditLeadsForm == "YES":
                    EmployeeRights.bolEmployeesLeadsFormWriteAccess = True
                else:
                    EmployeeRights.bolEmployeesLeadsFormWriteAccess = False

                if vstrDeleteLoans == "YES":
                    EmployeeRights.bolEmployeesLoanFormDeleteAccess = True
                else:
                    EmployeeRights.bolEmployeesLoanFormDeleteAccess = False

                if vstrLoanReprint == "YES":
                    EmployeeRights.bolEmployeesLoanFormReprintAccess = True
                else:
                    EmployeeRights.bolEmployeesLoanFormReprintAccess = False

                if vstrProcessPayment == "YES":
                    EmployeeRights.bolEmployeeLoanFormProcessPayment = True
                else:
                    EmployeeRights.bolEmployeeLoanFormProcessPayment = False

                if vstrSendPayment == "YES":
                    EmployeeRights.bolEmployeeLoanFormSendPayment = True
                else:
                    EmployeeRights.bolEmployeeLoanFormSendPayment = False

                EmployeeRights.put()
            selfURL = "/admin/employees/" + strEmployeeCode
            self.redirect(selfURL)

        else:
            self.redirect("/")


app = webapp2.WSGIApplication([

    ('/dynamic/funeralpolicy/AmountPayableSummary.html', AmountPayableDynamicHandler),
    ('/dynamic/funeralpolicy/PaymentDetails.html', PaymentDetailsDynamicHandler),
    ('/dynamic/admin/editbranch.html', EditBranchHandler),
    ('/dynamic/admin/editemployees.html', EditEmployeesHandler)
], debug=True)
