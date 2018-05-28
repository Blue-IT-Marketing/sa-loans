import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.getcwd()))

from Employee import EmploymentDetails,ResidentialAddress,PostalAddress,BankingDetails,ContactDetails,EmployeeRegRequest,BranchDetails
from database import UserRights,CompanyDetails, CompanyCosts
from contact import ContactMessages
from loans import CompanyCoffers
from clientglobalhistory import SearchPartners
class EmpExistHandler(webapp2.RequestHandler):
    def get(self):
        template =template_env.get_template('templates/dynamic/admin/empexist.html')
        context ={}
        self.response.write(template.render(context))


class DeleteEmployeesHandler(webapp2.RequestHandler):
    def post(self):
        try:
            strEmployeeCode = self.request.get('vstrEmployeeCode')
            logging.info("Employees Delete Executed")
            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == strEmployeeCode)
            TempEmployees = findRequest

            strReference = ""

            for Employee in TempEmployees:
                strReference = Employee.strReference
                Employee.key.delete()

            findRequest = ResidentialAddress.query(ResidentialAddress.strEmployeeCode == strEmployeeCode)
            TempPhysical = findRequest

            for physical in TempPhysical:
                physical.key.delete()

            findRequest = PostalAddress.query(PostalAddress.strEmployeeCode == strEmployeeCode)
            TempPostal  = findRequest

            for postal in TempPostal:
                postal.key.delete()

            findRequest = BankingDetails.query(BankingDetails.strEmployeeCode == strEmployeeCode)
            TempBanking = findRequest

            for banking in TempBanking:
                banking.key.delete()

            findRequest = ContactDetails.query(ContactDetails.strEmployeeCode == strEmployeeCode)
            TempContact = findRequest

            for contact in TempContact:
                contact.key.delete()

            findRequest = UserRights.query(UserRights.strReference == strReference)
            RightsList = findRequest.fetch()

            if len(RightsList) > 0:
                Rights = RightsList[0]
                Rights.key.delete()

            logging.info("Complete")
            self.redirect('/admin')
        except:
            logging.info("Error")



class DynamicBranchEmployeesHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:
            URL = str(self.request.url)

            URLList = URL.split("/")

            strBranchCode = URLList[len(URLList) - 1]

            if "#" in strBranchCode:
                strBranchCode = strBranchCode.strip('#')


            findRequest = EmploymentDetails.query(EmploymentDetails.strBranchCode == strBranchCode)
            TempEmploymentList = findRequest.fetch()
            findRequest = BranchDetails.query(BranchDetails.strCompanyBranchCode == strBranchCode)
            BranchList  = findRequest.fetch()
            if len(BranchList) > 0:
                thisBranch = BranchList[0]
            else:
                thisBranch = BranchDetails()
            context = {'strCallingURL': URL}
            if len(TempEmploymentList) > 0:
                context = {'employees': TempEmploymentList,'thisBranch':thisBranch,
                           'strCallingURL': URL}

            template = template_env.get_template('templates/dynamic/admin/branchemployeelist.html')
            self.response.write(template.render(context))
        else:
            pass

class EmployeeRegistrationRequestHandler(webapp2.RequestHandler):
    def post(self):

        Guser = users.get_current_user()

        if Guser:

            strRegistrationEmail = self.request.get('vstrReqForEmployeeRegister')
            strReference = self.request.get('vstrReqReference')
            strIDNumber = self.request.get('vstrIDNumber')

            EmployeeRequest =  EmployeeRegRequest()

            findRequest = EmployeeRegRequest.query(EmployeeRegRequest.strEmail == Guser.email())
            RequestsLists = findRequest.fetch()

            if len(RequestsLists) > 0:
                pass
            else:
                EmployeeRequest.writeEmail(strinput=Guser.email())
                EmployeeRequest.writeReference(strinput=Guser.user_id())
                EmployeeRequest.writeIDNumber(strinput=strIDNumber)

                EmployeeRequest.put()
        else:
            pass
        self.redirect('/employees')



class UserRightsHandler(webapp2.RequestHandler):

    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = EmployeeRegRequest.query()
            usersList = findRequest.fetch()

            template = template_env.get_template('templates/dynamic/admin/userrights.html')
            context = {'users': usersList}
            self.response.write(template.render(context))


class AllUserRightsHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        logging.info(msg=" User Rights Called")

        if Guser:
            findRequest = BranchDetails.query()
            branchList = findRequest.fetch()

            URLList = str(self.request.url)

            URLList = URLList.split("/")

            strReference = URLList[len(URLList) - 1]

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == strReference)
            ThisEmployeeList = findRequest.fetch()

            ThisEmployee = EmploymentDetails()

            if len(ThisEmployeeList) > 0:
                ThisEmployee = ThisEmployeeList[0]
                strUsername = ThisEmployee.readSurname()
                strReference = ThisEmployee.readReference()
                strIDNumber = ThisEmployee.readIDNumber()
                strEmployeeBranch = ThisEmployee.readBranchWorking()
                strFirstname = ThisEmployee.readNames()
                strSurname = ThisEmployee.readSurname()
                strEmployeeCode = ThisEmployee.readEmployeeCode()

                ThisUserRights = UserRights()

                findRequest = UserRights.query(UserRights.strReference == strReference)
                ThisUserRightsList = findRequest.fetch()
                if len(ThisUserRightsList) > 0:
                    ThisUserRights = ThisUserRightsList[0]


                if ThisUserRights.bolIsEmployee:
                    vstrIsEmployee = "YES"
                else:
                    vstrIsEmployee = "NO"

                if ThisUserRights.bolAccessToEmployeesAdminForm:
                    vstrAccessEmployeeAdmin = "YES"
                else:
                    vstrAccessEmployeeAdmin = "NO"

                if ThisUserRights.bolEmployeesLoanFormReadAccess:
                    vstrSearchLoans = "YES"
                else:
                    vstrSearchLoans = "NO"

                if ThisUserRights.bolEmployeesLoanFormWriteAccess:
                    vstrEditLoanForm = "YES"
                else:
                    vstrEditLoanForm = "NO"



                if ThisUserRights.bolEmployeesLeadsFormReadAccess:
                    vstrSearchLeadsForm = "YES"
                else:
                    vstrSearchLeadsForm = "NO"
                if ThisUserRights.bolEmployeesLeadsFormWriteAccess:
                    vstrEditLeadsForm = "YES"
                else:
                    vstrEditLeadsForm = "NO"

                ThisUserRights.writeEmployeeCode(strinput=strEmployeeCode)
                ThisUserRights.writeReference(strinput=strReference)
                ThisUserRights.put()

                template = template_env.get_template('templates/dynamic/admin/thisuserights.html')
                context = {'vstrUsername':strUsername,'vstrReference': strReference, 'vstrIDNumber': strIDNumber,
                           'branches': branchList,'vstrEmployeeBranch': strEmployeeBranch,'vstrEmployeeCode':strEmployeeCode,  'vstrFirstnames': strFirstname,
                           'vstrSurname': strSurname,'vstrIsEmployee': vstrIsEmployee,'vstrAccessEmployeeAdmin':vstrAccessEmployeeAdmin,
                           'vstrSearchLoans':vstrSearchLoans,'vstrEditLoans':vstrEditLoanForm,'vstrSearchLeadsForm':vstrSearchLeadsForm,
                               'vstrEditLeadsForm':vstrEditLeadsForm}
                self.response.write(template.render(context))

            else:

                findRequest = EmployeeRegRequest.query(EmployeeRegRequest.strReference == strReference)
                EmployeeList = findRequest.fetch()

                EmployeeReq = EmployeeRegRequest()

                if len(EmployeeList) > 0:
                    EmployeeReq = EmployeeList[0]
                    strUsername = EmployeeReq.readEmail()
                    strReference = EmployeeReq.readReference()
                    strIDNumber = EmployeeReq.readIDNumber()
                    strFirstname = ""
                    strSurname = ""
                    strEmployeeBranch = ""

                    i = 0
                    done = False
                    while not(done):
                        findRequest = EmploymentDetails.query()
                        EmployeeListed = findRequest.fetch()

                        NextCode = len(EmployeeListed) + i
                        NextCode = "E" + str(NextCode)
                        strEmployeeCode = NextCode

                        findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == NextCode)
                        EmployeeList = findRequest.fetch()

                        if len(EmployeeList) > 0:
                            done = False
                            i = i + 1
                        else:
                            done = True


                    CodeList = []
                    CodeList.append(NextCode)
                    template = template_env.get_template('templates/dynamic/admin/thisuserights.html')
                    context = {'vstrUsername':strUsername,'vstrReference': strReference, 'vstrIDNumber': strIDNumber,
                               'branches': branchList,'vstrEmployeeBranch': strEmployeeBranch, 'vstrEmployeeCode':strEmployeeCode,
                               'vstrFirstnames': strFirstname,
                               'vstrSurname': strSurname}
                    self.response.write(template.render(context))

                else:
                    pass
        else:
            pass
    def post(self):
        logging.info("saving user rights and settings")
        strIsEmployee = self.request.get('vstrIsEmployee')
        strAccessEmployeeAdmin = self.request.get('vstrAccessEmployeeAdmin')
        strSearchLoans = self.request.get('vstrSearchLoans')
        strEditLoans = self.request.get('vstrEditLoans')
        strSearchLeadsForm = self.request.get('vstrSearchLeadForm')
        strEditLeadsForm  = self.request.get('vstrEditLeadsForm')

        Rights = UserRights()
        logging.info(msg=strIsEmployee)

        URL = str(self.request.url)
        URLList = URL.split("/")
        strReference = URLList[len(URLList)-1]


        findRequest = UserRights.query(UserRights.strReference == strReference)
        RightsList = findRequest.fetch()

        if len(RightsList) > 0:
            Rights = RightsList[0]

        if strIsEmployee == "YES":
            Rights.setEmployeeUserRights()
            logging.info(msg="Is employee")

        if strAccessEmployeeAdmin == "YES":
            Rights.bolEmployeesAdminFormReadAccess = True
        else:
            Rights.bolEmployeesAdminFormReadAccess = False

        if strSearchLoans == "YES":
            Rights.bolEmployeesLoanFormReadAccess = True
        else:
            Rights.bolEmployeesLoanFormReadAccess = False

        if strEditLoans == "YES":
            Rights.bolEmployeesLoanFormWriteAccess = True
        else:
            Rights.bolEmployeesLoanFormWriteAccess = False


        if strSearchLeadsForm == "YES":
            Rights.bolEmployeesLeadsFormReadAccess = True
        else:
            Rights.bolEmployeesLeadsFormReadAccess = False

        if strEditLeadsForm == "YES":
            Rights.bolEmployeesLeadsFormWriteAccess = True
        else:
            Rights.bolEmployeesLeadsFormWriteAccess = False

        URL = str(self.request.url)
        URLlist = URL.split("/")

        strReference = URLlist[len(URLlist) - 1]

        Rights.writeReference(strinput=strReference)

        Rights.put()


        template = template_env.get_template('templates/dynamic/admin/rightsresponse.html')
        context = {'vstrIsEmployee': strIsEmployee,'vstrAccessEmployeeAdmin': strAccessEmployeeAdmin,
                   'vstrSearchLoans': strSearchLoans,
                   'vstrEditLoans': strEditLoans,'vstrSearchLeadsForm': strSearchLeadsForm,
                   'vstrEditLeadsForm': strEditLeadsForm}
        self.response.write(template.render(context))


class UserPersonalsHandler(webapp2.RequestHandler):
    def post(self):
        Guser = users.get_current_user()

        if Guser:
            strFirstnames = self.request.get('vstrFirstnames')
            strSurname = self.request.get('vstrSurname')
            strIDNumber = self.request.get('vstrIDNumber')
            strEmployeeCode = self.request.get('vstrEmployeeCode')
            strBranchCode = self.request.get('vstrBranchCode')

            URL = str(self.request.url)

            URLList = URL.split("/")
            strReference = URLList[len(URLList) - 1]

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == strReference)
            EmployeeList = findRequest.fetch()

            Employee = EmploymentDetails()

            if len(EmployeeList) > 0:
                Employee = EmployeeList[0]
            else:
                pass

            Employee.writeReference(strinput=strReference)
            Employee.writeEmployeeCode(strinput=strEmployeeCode)
            Employee.writeBranchWorking(strinput=strBranchCode)
            Employee.writeIDNumber(strinput=strIDNumber)
            Employee.writeSurname(strinput=strSurname)
            Employee.writeNames(strinput=strFirstnames)

            Employee.put()

            FindRequest = EmployeeRegRequest.query(EmployeeRegRequest.strReference == strReference)
            EmployeeReqList = FindRequest.fetch()

            findRequest = UserRights.query(UserRights.strReference == strReference)
            UserRightsList =findRequest.fetch()
            UserRight = UserRights()

            if len(UserRightsList) > 0:
                UserRight = UserRightsList[0]

            UserRight.writeReference(strinput=strReference)
            UserRight.writeEmployeeCode(strinput=strEmployeeCode)
            UserRight.put()


            if len(EmployeeReqList) > 0:
                EmployeeReq = EmployeeReqList[0]
                try:
                    EmployeeReq.key.delete()
                except:
                    pass
            else:
                pass


            template = template_env.get_template('templates/dynamic/admin/personalsresponse.html')
            context = {'vstrFirstnames': strFirstnames, 'vstrSurname': strSurname,'vstrIDNumber':strIDNumber,
                       'vstrEmployeeCode': strEmployeeCode,'vstrReference': strReference,'vstrBranchCode':strBranchCode}

            self.response.write(template.render(context))


class ContactFormMessagesHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = ContactMessages.query(ContactMessages.strResponseSent == False)
            ContactMessagesList = findRequest.fetch()
            TotalMessages = len(ContactMessagesList)
            Context = {'ContactMessagesList': ContactMessagesList, 'TotalMessages': TotalMessages}
            template = template_env.get_template('templates/dynamic/contact/inbox.html')
            self.response.write(template.render(Context))
        else:
            pass

class ContactFormReadMessageHandler(webapp2.RequestHandler):

    def get(self):
        try:
            URL = self.request.url
            URLlist = URL.split("/")
            MessageReference = URLlist[len(URLlist) - 1]
            MessageReference = str(MessageReference)
            MessageReference = MessageReference.strip()

            findRequest = ContactMessages.query(ContactMessages.strMessageReference == MessageReference)
            ContactMessageList = findRequest.fetch()

            findRequest = ContactMessages.query()
            TotalMessagesList = findRequest.fetch()
            TotalMessages = len(TotalMessagesList)

            ContactMessage = ContactMessageList[0]
            template = template_env.get_template('templates/dynamic/contact/readinbox.html')
            Context = {'ContactMessage': ContactMessage,'TotalMessages': TotalMessages}
            self.response.write(template.render(Context))

        except:
            pass






class AdminHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = CompanyDetails.query()
            CompanyList = findRequest.fetch()

            if len(CompanyList) > 0:
                thisCompany = CompanyList[0]
                template = template_env.get_template('templates/admin.html')
                context = {'thisCompany':thisCompany}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/admin.html')
                context = {}
                self.response.write(template.render(context))


class CompanyManagementHandler(webapp2.RequestHandler):
    def get(self):
        template = template_env.get_template('templates/management/company.html')
        context = {}
        self.response.write(template.render(context))
class CompanyDetailsHandler(webapp2.RequestHandler):

    def post(self):
        Guser = users.get_current_user()
        if Guser:
            self.response.write(""" .....Updating Company Database<br> """)
            vstrCompanyName = self.request.get('vstrCompanyName')
            vstrCompanyReg = self.request.get('vstrCompanyReg')
            vstrCompanySlogan = self.request.get('vstrCompanySlogan')
            vstrCompanyDirector = self.request.get('vstrCompanyDirectors')
            vstrStandNumber = self.request.get('vstrStandNumber')
            vstrStreetName = self.request.get('vstrStreetName')
            vstrCityTown = self.request.get('vstrCityTown')
            vstrProvince = self.request.get('vstrProvince')
            vstrCountry = self.request.get('vstrCountry')
            vstrPostalCode = self.request.get('vstrPostalCode')
            vstrCompanyTel = self.request.get('vstrCompanyTel')
            vstrCompanyCell = self.request.get('vstrCompanyCell')
            vstrCompanyFax = self.request.get('vstrCompanyFax')
            vstrCompanyEmail = self.request.get('vstrCompanyEmail')
            vstrCompanyWebsite = self.request.get('vstrCompanyWebsite')

            findRequest = CompanyDetails.query()
            CompanyList = findRequest.fetch()

            if len(CompanyList) > 0:
                Company = CompanyList[0]
            else:
                Company = CompanyDetails()


            try:

                Company.writeReference(strinput= Guser.user_id())
                Company.writeCompanyName(strinput=vstrCompanyName)
                Company.writeCompanyReg(strinput=vstrCompanyReg)
                Company.writeCompanySlogan(strinput=vstrCompanySlogan)
                Company.writeCompanyDirector(strinput=vstrCompanyDirector)
                Company.writeStandNumber(strinput=vstrStandNumber)
                Company.writeStreetName(strinput=vstrStreetName)
                Company.writeCityTown(strinput=vstrCityTown)
                Company.writeProvince(strinput=vstrProvince)
                Company.writeCountry(strinput=vstrCountry)
                Company.writePostalCode(strinput=vstrPostalCode)
                Company.writeCompanyTel(strinput=vstrCompanyTel)
                Company.writeCompanyCell(strinput=vstrCompanyCell)
                Company.writeCompanyFax(strinput=vstrCompanyFax)
                Company.writeCompanyEmail(strinput=vstrCompanyEmail)
                Company.writeCompanyWebsite(strinput=vstrCompanyWebsite)
                Company.put()
                self.response.write("Successfully updated company details")
            except:
                self.response.write("Error Updating Company Details")
        else:
            self.response.write("Error updating Company Details")

class BranchIncomeHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrBranchCode = self.request.get('vstrBranchCode')

            findRequest = BranchDetails.query(BranchDetails.strCompanyBranchCode == vstrBranchCode)
            thisBranchList = findRequest.fetch()

            if len(thisBranchList) > 0:
                thisBranch = thisBranchList[0]
            else:
                thisBranch = BranchDetails()

            findRequest = CompanyCoffers.query(CompanyCoffers.strBranchCode == vstrBranchCode)
            thisCompanyCoffersList = findRequest.fetch()

            if len(thisCompanyCoffersList) > 0:
                thisCompanyCoffers = thisCompanyCoffersList[0]
            else:
                thisCompanyCoffers = CompanyCoffers()

            template = template_env.get_template('templates/dynamic/admin/branchincome.html')
            context = {'thisBranch':thisBranch, 'thisCompanyCoffers':thisCompanyCoffers}
            self.response.write(template.render(context))

    def post(self):
        """
            Make sure to insert the Banking Fields below
            or maybe we can use a different button to add the banking section
        :return:
        """
        Guser = users.get_current_user()
        if Guser:
            vstrOption = self.request.get('vstrOption')
            vstrOption = int(vstrOption)
            vstrBranchCode = self.request.get('vstrBranchCode')
            if vstrOption == 0:
                vstrTotalCashAvailable = self.request.get('vstrTotalCashAvailable')



                findRequest = CompanyCoffers.query(CompanyCoffers.strBranchCode == vstrBranchCode)
                thisCompanyCoffersList = findRequest.fetch()

                if len(thisCompanyCoffersList) > 0:
                    thisCompanyCoffers = thisCompanyCoffersList[0]
                else:
                    thisCompanyCoffers = CompanyCoffers()

                thisCompanyCoffers.writeBranchCode(strinput=vstrBranchCode)
                thisCompanyCoffers.writeReference(strinput=Guser.user_id())
                thisCompanyCoffers.writeCashAvailable(strinput=vstrTotalCashAvailable)
                thisCompanyCoffers.put()
            elif vstrOption == 1:
                vstrTotalCashInBank = self.request.get('vstrTotalCashInBank')
                findRequest = CompanyCoffers.query(CompanyCoffers.strBranchCode == vstrBranchCode)
                thisCompanyCoffersList = findRequest.fetch()

                if len(thisCompanyCoffersList) > 0:
                    thisCompanyCoffers = thisCompanyCoffersList[0]
                else:
                    thisCompanyCoffers = CompanyCoffers()

                thisCompanyCoffers.writeBranchCode(strinput=vstrBranchCode)
                thisCompanyCoffers.writeReference(strinput=Guser.user_id())
                thisCompanyCoffers.writeCashInBank(strinput=vstrTotalCashInBank)
                thisCompanyCoffers.put()

            self.response.write("Company Income Successfully Adjusted")

class BranchCostsHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrBranchCode = self.request.get('vstrBranchCode')

            findRequest = BranchDetails.query(BranchDetails.strCompanyBranchCode == vstrBranchCode)
            thisBranchList = findRequest.fetch()

            if len(thisBranchList) > 0:
                thisBranch = thisBranchList[0]
            else:
                thisBranch = BranchDetails()

            template = template_env.get_template('templates/dynamic/admin/branchcosts.html')
            context = {'thisBranch':thisBranch}
            self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()
        if Guser:
            vstrBranchCode = self.request.get('vstrBranchCode')
            vstrTotalEstimatedSalaries = self.request.get('vstrTotalEstimatedSalaries')
            vstrTotalActualSalaries = self.request.get('vstrTotalActualSalaries')
            vstrAdvertising = self.request.get('vstrAdvertising')
            vstrInsurance = self.request.get('vstrInsurance')
            vstrOverHeads = self.request.get('vstrOverHeads')
            vstrOfficeRent = self.request.get('vstrOfficeRent')
            vstrTelCosts = self.request.get('vstrTelCosts')
            vstrStationery = self.request.get('vstrStationery')
            vstrElectricity = self.request.get('vstrElectricity')
            vstrTransport = self.request.get('strTransport')


            findRequest = CompanyCosts.query(CompanyCosts.strBranchCode == vstrBranchCode)
            CompanyCostList = findRequest.fetch()
            if len(CompanyCostList) > 0:
                thisCompanyCosts = CompanyCostList[0]
            else:
                thisCompanyCosts = CompanyCosts()


            thisCompanyCosts.writeBranchCode(strinput=vstrBranchCode)
            thisCompanyCosts.writeAdvertising(strinput=vstrAdvertising)
            thisCompanyCosts.writeSalary(strinput=vstrTotalActualSalaries)
            thisCompanyCosts.writeInsurance(strinput=vstrInsurance)
            thisCompanyCosts.writeOverhead(strinput=vstrOverHeads)
            thisCompanyCosts.writeOfficeRent(strinput=vstrOfficeRent)
            thisCompanyCosts.writeTelCell(strinput=vstrTelCosts)
            thisCompanyCosts.writeStationery(strinput=vstrStationery)
            thisCompanyCosts.writeElectricity(strinput=vstrElectricity)
            thisCompanyCosts.writeTransport(strinput=vstrTransport)
            thisCompanyCosts.put()


class LockStatusHandler(webapp2.RequestHandler):
    def get(self):
        """
            Design The Lock Mechanism
        :return:
        """
        Guser = users.get_current_user()
        if Guser:
            vstrEmployeeCode = self.request.get('vstrEmployeeCode')

            findRequest = EmploymentDetails.query(EmploymentDetails.strEmployeeCode == vstrEmployeeCode)
            thisEmployeeList = findRequest.fetch()

            if len(thisEmployeeList) > 0:
                thisEmployee = thisEmployeeList[0]
            else:
                thisEmployee = EmploymentDetails()

            template = template_env.get_template('templates/dynamic/employee/LockStatus.html')
            context = {'thisEmployee':thisEmployee}
            self.response.write(template.render(context))


class GlobalHistoryCheckHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:


            findRequests = SearchPartners.query()
            thisSearchPartnersList = findRequests.fetch()

            template = template_env.get_template('templates/dynamic/ratings/globalsources.html')
            context = {'thisSearchPartnersList':thisSearchPartnersList}
            self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()
        if Guser:
            vstrURL = self.request.get('vstrURL')


            findRequest = SearchPartners.query(SearchPartners.strPartnerURL == vstrURL)
            thisSearchPartnersList = findRequest.fetch()

            if len(thisSearchPartnersList) > 0:
                self.response.write("Search Partner Already Added")
            else:
                findRequest = SearchPartners.query()
                thisSearchPartnersList = findRequest.fetch()

                thisSearchPartner = SearchPartners()
                thisSearchPartner.strPartnerURL = vstrURL
                thisSearchPartner.strIndex = len(thisSearchPartnersList)
                thisSearchPartner.put()


                findRequest = SearchPartners.query()
                thisSearchPartnersList = findRequest.fetch()


                template = template_env.get_template('templates/dynamic/ratings/globalsources.html')
                context = {'thisSearchPartnersList': thisSearchPartnersList}
                self.response.write(template.render(context))

app = webapp2.WSGIApplication([
    ('/admin', AdminHandler),
    ('/admin/empexist',EmpExistHandler),
    ('/admin/employees/delete',DeleteEmployeesHandler),
    ('/dynamic/admin/branch/employees/.*', DynamicBranchEmployeesHandler),
    ('/admin/registration/request', EmployeeRegistrationRequestHandler),
    ('/dynamic/admin/userrights', UserRightsHandler),
    ('/admin/contactform', ContactFormMessagesHandler),
    ('/admin/contact/.*', ContactFormReadMessageHandler),
    ('/admin/userrights/employees/.*', AllUserRightsHandler),
    ('/admin/userpersonals/employees/.*', UserPersonalsHandler),
    ('/dynamic/management/companymanagement', CompanyManagementHandler),
    ('/admin/companydetails', CompanyDetailsHandler),
    ('/admin/branchincome', BranchIncomeHandler),
    ('/admin/branchcosts', BranchCostsHandler),
    ('/admin/lockstatus', LockStatusHandler),
    ('/admin/globalhistorycheck', GlobalHistoryCheckHandler)

], debug=True)

