import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
strValidMonths = ["JAN","FEB","MAR","APR","MAR","JUN","JUL","AUG","OCT","SEP","NOV","DEC"]

class Constants(ndb.Expando):
    undefined = None
    _generalError = "General Error"
    strReference = ndb.StringProperty()
    strAccountNumber = ndb.StringProperty()  # Calculated Value BranchCODE/EMPCODE/PolicyNUMBER  ####/#####/#####


    def readReference(self):
        try:
            strtemp = str(self.strReference)
            if not (strtemp == self.undefined):
                return strtemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeReference(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if not (strinput == self.undefined):
                self.strReference = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def readAccountNumber(self):
        try:
            strTemp = str(self.strAccountNumber)
            strTemp = strTemp.strip()
            if not(strTemp == self.undefined):
                return strTemp
            else:
                return self.undefined
        except:
            return self._generalError

    def writeAccountNumber(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if not(strinput == self.undefined):
                self.strAccountNumber = strinput
                return True
            else:
                return False
        except:
            return self._generalError

    def setGeneralError(self,strinput):
        try:
            strinput = str(strinput)
            if strinput == self.undefined:
                self._generalError = strinput
                return True
            else:
                return False
        except:
            return self._generalError
class WorkingAccount(ndb.Expando):
    strTotalCreated = ndb.IntegerProperty(default=0)
    strActivated = ndb.BooleanProperty(default=False)

    strReference = ndb.StringProperty()
    strAccountNumber = ndb.StringProperty()  # Calculated Value BranchCODE/EMPCODE/PolicyNUMBER  ####/#####/#####


    def readReference(self):
        try:
            strtemp = str(self.strReference)
            if not (strtemp == None):
                return strtemp
            else:
                return None
        except:
            return None

    def writeReference(self, strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()
            if not (strinput == None):
                self.strReference = strinput
                return True
            else:
                return False
        except:
            return None

    def readAccountNumber(self):
        try:
            strTemp = str(self.strAccountNumber)
            strTemp = strTemp.strip()

            if not(strTemp == None):
                return strTemp
            else:
                return None
        except:
            return None

    def writeAccountNumber(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == None):
                self.strAccountNumber = strinput
                return True
            else:
                return False
        except:
            return None

    def readTotalCreated(self):
        try:
            strTemp = str(self.strTotalCreated)
            strTemp = strTemp.strip()

            if strTemp.isdigit():
                return int(strTemp)
            else:
                return None
        except:
            return None

    def writeTotalCreated(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if strinput.isdigit():
                self.strTotalCreated = strinput
                return True
            else:
                return False
        except:
            return False

    def readActivated(self):
        try:
            return self.strActivated
        except:
            return False

    def writeActivated(self,strinput):
        try:
            if strinput == True:
                self.strActivated = strinput
                return True
            elif strinput == False:
                self.strActivated = strinput
                return True
            else:
                return False
        except:
            return False

    def createNewAccountNumber(self,strinput):
        from Employee import EmploymentDetails
        try:
            Guser = users.get_current_user()
            logging.info("Create Account Number Called")
            if Guser:
                logging.info("Maybe Problem is here" + str(strinput))
                strinput = str(strinput)
                logging.info(strinput)
                if strinput.isdigit():
                    self.strTotalCreated = int(strinput) + 1
                    logging.info(msg="Tested True if its Digit")
                else:
                    self.strTotalCreated = 1
                    logging.info(msg="Tested False if its digit")

                self.strActivated = False
                self.strReference = Guser.user_id()
                logging.info(msg="Create Account Number Called")

                findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
                EmployeeList = findRequest.fetch()


                if len(EmployeeList) > 0:
                    Employee = EmployeeList[0]
                else:
                    Employee = EmploymentDetails()

                self.strAccountNumber = str(Employee.strBranchCode) + str(Employee.strEmployeeCode) + str(self.strTotalCreated)

                self.put()
                return self.strAccountNumber
            else:
                logging.info("Tested False if its GUser")
                return None
        except:
            return None
class ResourceAccessRights(Constants):
    """
        If the rights relate to a client who can login into the system then the record will also contain
        the policy number

        if the rights relate to an employee then theres no use for an employment number as all employees can be
        identifiable using only their email hence reference will be enough to identify them
    """
    strEmployeeCode = ndb.StringProperty()

    bolAccessToEmployeesLoanForm = ndb.BooleanProperty(default=False)
    bolAccessToEmployeesLeadsForm = ndb.BooleanProperty(default=False)
    bolAccessToEmployeesAdminForm = ndb.BooleanProperty(default=False)


    bolAccessToStaffChatForm = ndb.BooleanProperty(default=False)
    bolAccessToClientsChatForm = ndb.BooleanProperty(default=False)

    def readEmployeeCode(self):
        try:
            strTemp = str(self.strEmployeeCode)
            return strTemp
        except:
            return ""

    def writeEmployeeCode(self,strinput):
        try:
            strinput = str(strinput)
            strinput = strinput.strip()

            if not(strinput == self.undefined):
                self.strEmployeeCode = strinput
                return True
            else:
                return False

        except:
            return False



    def setEmployeeAccessRightsDefault(self):
        try:
            if self.setClientsRightsDefault():
                self.bolAccessToEmployeesLoanForm = True
                self.bolAccessToEmployeesLeadsForm = True
                return True
            else:
                return False
        except:
            return False

    def setAdminAccessRightsDefault(self):
        try:
            if self.setEmployeeAccessRightsDefault():
                self.bolAccessToEmployeesAdminForm = True
                return True
            else:
                return False
        except:
            return False
class CompanyDetails(Constants):
    strCompanyName = ndb.StringProperty()
    strCompanyReg = ndb.StringProperty()
    strCompanyNCR = ndb.StringProperty()
    strCompanySlogan = ndb.StringProperty()
    strCompanyDirector = ndb.StringProperty()

    strStandNumber = ndb.StringProperty()
    strStreetName = ndb.StringProperty()
    strCityTown = ndb.StringProperty()
    strProvince = ndb.StringProperty()
    strCountry = ndb.StringProperty()
    strPostalCode = ndb.StringProperty()

    strCompanyTel = ndb.StringProperty()
    strCompanyCell = ndb.StringProperty()
    strCompanyFax = ndb.StringProperty()
    strCompanyEmail = ndb.StringProperty()
    strCompanyWebsite = ndb.StringProperty()


    def writeCompanyName(self,strinput):
       try:
           strinput = str(strinput)
           if not(strinput == None):
               self.strCompanyName = strinput
               return True
           else:
               return False
       except:
           return False
    def writeCompanyReg(self,strinput):
       try:
           strinput = str(strinput)
           if not(strinput == None):
               self.strCompanyReg = strinput
               return True
           else:
               return False
       except:
           return False
    def writeCompanyNCR(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCompanyNCR = strinput
                return True
            else:
                return False
        except:
            return False
    def writeCompanySlogan(self,strinput):
       try:
           strinput = str(strinput)
           if not(strinput == None):
               self.strCompanySlogan = strinput
               return True
           else:
               return False

       except:
           return False
    def writeCompanyDirector(self,strinput):
       try:
           strinput = str(strinput)
           if not(strinput == None):
               self.strCompanyDirector = strinput
               return True
           else:
               return False
       except:
           return False
    def writeStandNumber(self,strinput):
       try:
           strinput = str(strinput)
           if not(strinput == None):
               self.strStandNumber = strinput
               return True
           else:
               return False

       except:
           return False
    def writeStreetName(self,strinput):
       try:
           strinput = str(strinput)
           if not(strinput == None):
               self.strStreetName = strinput
               return True
           else:
               return False
       except:
           return False
    def writeCityTown(self,strinput):
       try:
           strinput = str(strinput)

           if not(strinput == None):
               self.strCityTown = strinput
               return True
           else:
               return False
       except:
           return False
    def writeProvince(self,strinput):
       try:
           strinput = str(strinput)
           if not(strinput == None):
               self.strProvince = strinput
               return True
           else:
               return False

       except:
           return False
    def writeCountry(self,strinput):
       try:
           strinput = str(strinput)
           if not(strinput == None):
               self.strCountry = strinput
               return True
           else:
               return False

       except:
           return False
    def writePostalCode(self,strinput):
       try:
           strinput = str(strinput)
           if not(strinput == None):
               self.strPostalCode = strinput
               return True
           else:
               return False
       except:
           return False
    def writeCompanyTel(self,strinput):
       try:
           strinput = str(strinput)
           if not(strinput == None):
               self.strCompanyTel = strinput
               return True
           else:
               return False

       except:
           return False
    def writeCompanyCell(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCompanyCell = strinput
                return True
            else:
                return False

        except:
            return False
    def writeCompanyFax(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCompanyFax = strinput
                return True
            else:
                return False
        except:
            return False
    def writeCompanyEmail(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCompanyEmail = strinput
                return True
            else:
                return False

        except:
            return False
    def writeCompanyWebsite(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCompanyWebsite = strinput
                return True
            else:
                return False
        except:
            return False
class CompanyRepaymentAccount(ndb.Expando):
    strCompanyName = ndb.StringProperty()
    strCompanyReg = ndb.StringProperty()
    strBankName = ndb.StringProperty()
    strBankAccount = ndb.StringProperty()
    strAccountType = ndb.StringProperty()
    strBranchCode = ndb.StringProperty()
    strAccountReference = ndb.StringProperty()


    def writeCompanyName(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCompanyName = strinput
                return True
            else:
                return False
        except:
            return False
    def writeCompanyReg(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCompanyReg = strinput
                return True
            else:
                return False
        except:
            return False
    def writeBankName(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBankName = strinput
                return True
            else:
                return False
        except:
            return False
    def writeBankAccount(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBankAccount = strinput
                return True
            else:
                return False
        except:
            return False
    def writeAccountType(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strAccountType = strinput
                return True
            else:
                return False
        except:
            return False
    def writeBranchCode(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBranchCode = strinput
                return True
            else:
                return False
        except:
            return False
    def writeAccountReference(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strAccountReference = strinput
                return True
            else:
                return False
        except:
            return False
class UserRights(ResourceAccessRights):
    bolIsEmployee = ndb.BooleanProperty(default=False)
    bolEmployeesLoanFormReadAccess = ndb.BooleanProperty(default=False)
    bolEmployeesLoanFormWriteAccess = ndb.BooleanProperty(default=False)
    bolEmployeesLoanFormDeleteAccess = ndb.BooleanProperty(default=False)

    bolEmployeesLoanFormReprintAccess = ndb.BooleanProperty(default=False)
    bolEmployeeLoanFormProcessPayment = ndb.BooleanProperty(default=False)
    bolEmployeeLoanFormSendPayment = ndb.BooleanProperty(default=False)

    bolEmployeesLeadsFormReadAccess = ndb.BooleanProperty(default=False)
    bolEmployeesLeadsFormWriteAccess = ndb.BooleanProperty(default=False)
    bolEmployeesLeadsFormDeleteAccess = ndb.BooleanProperty(default=False)

    bolEmployeesAdminFormReadAccess = ndb.BooleanProperty(default=False)
    bolEmployeesAdminFormWriteAccess = ndb.BooleanProperty(default=False)
    bolEmployeesAdminFormDeleteAccess = ndb.BooleanProperty(default=False)



    def setEmployeeUserRights(self):
        try:
            if self.setClientUserRights() and self.setEmployeeAccessRightsDefault():
                self.bolEmployeesLoanFormReadAccess = True
                self.bolEmployeesLoanFormWriteAccess = True
                self.bolEmployeesLeadsFormReadAccess = True
                self.bolEmployeesLeadsFormWriteAccess = True
                self.bolIsEmployee = True
                return True
            else:
                self.bolIsEmployee = False
                return False
        except:
            self.bolIsEmployee = False
            return False

    def setAdminUserRights(self):
        try:
            if self.setAdminAccessRightsDefault():
                self.bolEmployeesAdminFormReadAccess = True
                self.bolEmployeesAdminFormWriteAccess = True
                self.bolEmployeesAdminFormDeleteAccess = True
            else:
                pass
        except:
            pass
class CompanyCosts(ndb.Expando):
    strMonth = ndb.IntegerProperty()
    strBranchCode = ndb.StringProperty()
    strSalaries = ndb.IntegerProperty()
    strOfficeRent = ndb.IntegerProperty()
    strTelCell = ndb.IntegerProperty()
    strStationery = ndb.IntegerProperty()
    strElectricity = ndb.IntegerProperty()
    strTransport = ndb.IntegerProperty()
    strAdvertising = ndb.IntegerProperty()
    strInsurance = ndb.IntegerProperty()
    strOverheads = ndb.IntegerProperty()

    def writeMonth(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strMonth = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeBranchCode(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBranchCode = strinput
                return True
            else:
                return False
        except:
            return False
    def writeSalary(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strSalaries = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeOfficeRent(self,strinput):
        try:
            strinput = str(strinput)

            if strinput.isdigit():
                self.strOfficeRent = int(strinput)
                return True
            else:
                return False

        except:
            return False
    def writeTelCell(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strTelCell = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeStationery(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strStationery = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeElectricity(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strElectricity = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeTransport(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strTransport = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeAdvertising(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strAdvertising = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeInsurance(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strInsurance = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeOverhead(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strOverheads = int(strinput)
                return True
            else:
                return False
        except:
            return False












