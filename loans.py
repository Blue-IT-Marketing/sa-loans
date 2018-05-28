import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
import datetime
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))

from database import *
from Employee import BranchDetails,EmploymentDetails
from tasks import Tasks
from profiles import Activity
class LoanConstant(ndb.Expando):
    strAccountNumber = ndb.StringProperty()
    strReference = ndb.StringProperty()
    strEmployeeCode = ndb.StringProperty()


    def writeAccountNumber(self, strinput):
        try:

            strinput = str(strinput)

            if not (strinput == None):
                self.strAccountNumber = strinput
                return True
            else:
                return False
        except:
            return False

    def writeReference(self, strinput):
        try:
            strinput = str(strinput)
            if not (strinput == None):
                self.strReference = strinput
                return True
            else:
                return False
        except:
            return False
    def writeEmployeeCode(self, strinput):
        try:
            strinput = str(strinput)
            if not (strinput == None):
                self.strEmployeeCode = strinput
                return True
            else:
                return False
        except:
            return False
class ActiveLoan(LoanConstant):
    strLoanActive = ndb.BooleanProperty(default=False)
    def setActiveLoan(self,strReference,strAccountNumber):
        try:

            findRequest = ActiveLoan.query(ActiveLoan.strReference == strReference,ActiveLoan.strLoanActive == True)
            ActiveLoansList = findRequest.fetch()

            for Active in ActiveLoansList:
                Active.key.delete()

            self.strAccountNumber = strAccountNumber
            self.strReference = strReference
            self.strLoanActive = True
            self.put()
            return True
        except:
            return False
class Loan(LoanConstant):
    strLoanedAmount = ndb.StringProperty()
    strDateLoaned = ndb.DateProperty()
    strPaymentAmount = ndb.IntegerProperty()
    strBalance = ndb.IntegerProperty()
    strPaymentDate = ndb.StringProperty()
    strLoanActive = ndb.BooleanProperty(default=False)

    def writeLoanedAmount(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strLoanedAmount = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeDateLoaned(self,strinput):
        try:

            if not(strinput == None):
                self.strDateLoaned = strinput
                return True
            else:
                return False
        except:
            return False
    def writePaymentAmount(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strPaymentAmount = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeBalance(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strBalance = strinput
                return True
            else:
                return False
        except:
            return False
    def writePaymentDate(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strPaymentDate = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def ActivateLoan(self):
        try:
            Guser = users.get_current_user()
            if Guser:
                self.strLoanActive = True
                findRequest = UserRights.query(UserRights.bolEmployeeLoanFormSendPayment == True)
                AdminUSersList = findRequest.fetch()

                for AdminUser in AdminUSersList:
                    Task = Tasks()
                    Task.writeReference(strinput=Guser.user_id())
                    Task.writeTaskNote(strinput="Payment for loan")
                    PaymentURL = "/loans/list/" + self.strAccountNumber
                    Task.writeTaskURL(strinput=PaymentURL)
                    Task.writeTaskType(strinput="Admin")
                    Task.writeToReference(strinput=AdminUser.strReference)
                    Task.writeReference(strinput=Guser.user_id())
                    if Task.setTaskID():
                        Task.put()
                        return True
                    else:
                        return False
                return True
        except:
            return False
class LoanApplicantDetails(LoanConstant):

    strTitle = ndb.StringProperty()
    strFullNames = ndb.StringProperty()
    strSurname = ndb.StringProperty()
    strIDNumber = ndb.StringProperty()
    strDateOfBirth = ndb.DateProperty()
    strNationality = ndb.StringProperty()

    strHouseNumber = ndb.StringProperty()
    strStreetName = ndb.StringProperty()
    strCityTown = ndb.StringProperty()
    strProvince = ndb.StringProperty()
    strCountry = ndb.StringProperty()
    strPostalCode = ndb.StringProperty()

    strBoxNumber = ndb.StringProperty()
    strPostalCityTown = ndb.StringProperty()
    strPostalProvince = ndb.StringProperty()
    strPostalCountry = ndb.StringProperty()
    strPostalPostalCode = ndb.StringProperty()


    strTel = ndb.StringProperty()
    strCell = ndb.StringProperty()
    strEmail = ndb.StringProperty()

    strNextOfKinNames = ndb.StringProperty()
    strNextOfKinAddress = ndb.StringProperty()
    strNextOfKinCell = ndb.StringProperty()

    strALLPS = ndb.StringProperty()


    def writeTitle(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strTitle = strinput
                return True
            else:
                return False
        except:
            return False
    def writeBoxNumber(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strBoxNumber = strinput
                return True
            else:
                return False
        except:
            return False
    def writePostalCityTown(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strPostalCityTown = strinput
                return True
            else:
                return False
        except:
            return False
    def writePostalProvince(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strPostalProvince = strinput
                return True
            else:
                return False

        except:
            return False
    def writePostalCountry(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strPostalCountry = strinput
                return True
            else:
                return False

        except:
            return False
    def writePostalPostalCode(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strPostalPostalCode = strinput
                return True
            else:
                return False
        except:
            return False
    def writeFullNames(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strFullNames = strinput
                return True
            else:
                return False
        except:
            return False
    def writeSurname(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strSurname = strinput
                return True
            else:
                return False
        except:
            return False
    def writeIDNumber(self,strinput):
        try:
            strinput  = str(strinput)

            if not(strinput == None):
                self.strIDNumber = strinput
                return True
            else:
                return False
        except:
            return False
    def writeDateOfBirth(self,strinput):
        try:
            if not(strinput == None):
                self.strDateOfBirth = strinput
                return True
            else:
                return False
        except:
            return False
    def writeNationality(self,strinput):
        try:
            strinput = str(strinput)


            if not(strinput == None):
                self.strNationality = strinput
                return True
            else:
                return False
        except:
            return False
    def writeHouseNumber(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strHouseNumber = strinput
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
    def writeTel(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strTel = strinput
                return True
            else:
                return False
        except:
            return False
    def writeCell(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCell = strinput
                return True
            else:
                return False
        except:
            return False
    def writeEmail(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strEmail = strinput
                return True
            else:
                return False
        except:
            return False
    def writeNextOfKinNames(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strNextOfKinNames = strinput
                return True
            else:
                return False
        except:
            return False
    def writeNextOfKinAddress(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strNextOfKinAddress = strinput
                return True
            else:
                return False
        except:
            return False
    def writeNextOfKinCell(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strNextOfKinCell = strinput
                return True
            else:
                return False
        except:
            return False
    def writeALLPS(self, strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strALLPS = strinput
                return True
            else:
                return False
        except:
            return False
class LoanEmploymentDetails(LoanConstant):

    strNameOfEmployer = ndb.StringProperty()
    strEmployeeNumber = ndb.StringProperty()
    strEmployeeKind =ndb.StringProperty()
    strDepartment = ndb.StringProperty()
    strContract = ndb.StringProperty()
    strDateJoined = ndb.DateProperty()
    strStandNumber = ndb.StringProperty()
    strStreetName = ndb.StringProperty()
    strTownCity = ndb.StringProperty()
    strProvince = ndb.StringProperty()
    strCountry = ndb.StringProperty()
    strPostalCode = ndb.StringProperty()
    strTel = ndb.StringProperty()

    def writeEmployeeKind(self,strinput):
        try:
            strinput = str(strinput)
            if strinput == "government" or strinput == "private" or strinput== "pension" or strinput == "grant":
                self.strEmployeeKind = strinput
                return True
            else:
                return False
        except:
            return False

    def writeNameOfEmployer(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strNameOfEmployer = strinput
                return True
            else:
                return False
        except:
            return False

    def writeEmployeeNumber(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strEmployeeNumber = strinput
                return True
            else:
                return False
        except:
            return False

    def writeDepartment(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strDepartment = strinput
                return True
            else:
                return False
        except:
            return False

    def writeContract(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strContract = strinput
                return True
            else:
                return False
        except:
            return False

    def writeDateJoined(self,strinput):
        try:
            if not(strinput == None):
                self.strDateJoined = strinput
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

    def writeTownCity(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strTownCity = strinput
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

class CreditProvider(LoanConstant):
    strNameCreditProvider = ndb.StringProperty(default="Midey Financial Solutions")
    strProviderAddress = ndb.StringProperty(default=""" Mashapa Complex, 1st Floor, Office No. B12 &amp; 14 , Thohoyandou, 0950,
    Tel : 015 962 0976""")
    strNCRRegistration = ndb.StringProperty(default="NCRCP5905")
    strBranchName = ndb.StringProperty()
    strLoanOfficer = ndb.StringProperty() # Reference Number of the Employee Who created the Loan
    strDateSigned = ndb.DateProperty(auto_now_add=True)

    def writeBranchName(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBranchName = strinput
                return True
            else:
                return False
        except:
            return False

    def writeLoanOfficer(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strLoanOfficer = strinput
                return True
            else:
                return False
        except:
            return False
class IncomeExpense(LoanConstant):


    strIncomeAfterDeduction = ndb.IntegerProperty()
    strOverTime = ndb.IntegerProperty()
    strCommission = ndb.IntegerProperty()
    strOtherIncome = ndb.IntegerProperty()
    strTotalIncome = ndb.IntegerProperty()

    strBondRepayments = ndb.IntegerProperty()
    strLoanInstallments = ndb.IntegerProperty()
    strWaterElectricityTel = ndb.IntegerProperty()
    strInsurance = ndb.IntegerProperty()
    strChildrenMaintenance = ndb.IntegerProperty()
    strVehicleMaintenance = ndb.IntegerProperty()
    strBasicNecessities = ndb.IntegerProperty()
    strDomesticWages = ndb.IntegerProperty()
    strEducation = ndb.IntegerProperty()
    strOtherExpenses = ndb.IntegerProperty()
    strTotalExpenses = ndb.IntegerProperty()
    strAffordability = ndb.IntegerProperty()


    def writeIncomeAfterDeduction(self,strinput):
        try:
            strinput = str(strinput)

            if strinput.isdigit():
                self.strIncomeAfterDeduction = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeOverTime(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strOverTime = int(strinput)
                return True
            else:
                return False

        except:
            return False
    def writeCommission(self,strinput):
        try:
            strinput = str(strinput)

            if strinput.isdigit():
                self.strCommission = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeOtherIncome(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strOtherIncome = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeTotalIncome(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strTotalIncome = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeChildrenMaintanance(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strChildrenMaintenance = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeBondRepayments(self,strinput):
        try:
            strinput = str(strinput)

            if strinput.isdigit():
                self.strBondRepayments = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeLoanInstallements(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strLoanInstallments = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeWaterElectricity(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strWaterElectricityTel = int(strinput)
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
    def writeVehicleMaintenance(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strVehicleMaintenance = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeBasicNecessity(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strBasicNecessities = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeDomesticWages(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strDomesticWages = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeEducation(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strEducation = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeOtherExpenses(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strOtherExpenses = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeTotalExpenses(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strTotalExpenses = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeAffordability(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strAffordability = int(strinput)
                return True
            else:
                return False
        except:
            return False
class PayTO(LoanConstant):
    strBankName = ndb.StringProperty()
    strAccountHolder = ndb.StringProperty()
    strBankAccountNumber = ndb.StringProperty()
    strAccountType = ndb.StringProperty()
    strBranchCode = ndb.StringProperty()
    strBranchName = ndb.StringProperty()
    strNotes = ndb.StringProperty()

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

    def writeAccountHolder(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strAccountHolder = strinput
                return True
            else:
                return False
        except:
            return False

    def writeBankAccountNumber(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBankAccountNumber = strinput
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

    def writeBranchName(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBranchName = strinput
                return True
            else:
                return False
        except:
            return False

    def writeNotes(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strNotes = strinput
                return True
            else:
                return False

        except:
            return False

class CompanyCoffers(ndb.Expando):
    strReference = ndb.StringProperty()
    strBranchCode = ndb.StringProperty()
    strCashAvailable = ndb.IntegerProperty()
    strCashInBank = ndb.IntegerProperty()

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

    def writeCashAvailable(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCashAvailable = int(strinput)
                return True
            else:
                return False
        except:
            return False

    def writeCashInBank(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCashInBank = int(strinput)
                return True
            else:
                return False
        except:
            return False

    def depositCashInBank(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strCashInBank = self.strCashInBank + int(strinput)
                return True
            else:
                return False
        except:
            return False

    def withdrawCashFromBank(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strCashInBank = self.strCashInBank - int(strinput)
                return True
            else:
                return False
        except:
            return False

    def depositCashAvailable(self,strinput):
        try:
            strinput = str(strinput)

            if strinput.isdigit():
                self.strCashAvailable = self.strCashAvailable + int(strinput)
                return True
            else:
                return False
        except:
            return False

    def withDrawCashAvailable(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strCashAvailable = self.strCashAvailable - int(strinput)
                return True
            else:
                return False
        except:
            return False





class PaymentTOClient(LoanConstant):
    strAmountRequested = ndb.IntegerProperty()
    strAmountPaid = ndb.IntegerProperty()
    strBalance = ndb.IntegerProperty()
    strDateTimePaid = ndb.DateTimeProperty(auto_now_add=True)

    def writeAmountRequested(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strAmountRequested = int(strinput)
                return True
            else:
                return False
        except:
            return False

    def writeAmountPaid(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strAmountPaid = int(strinput)
                return True
            else:
                return False
        except:
            return False

    def writeBalance(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBalance = int(strinput)
                return True
            else:
                return False
        except:
            return False

class PaymentFromClient(LoanConstant):
    strAmountOwed = ndb.IntegerProperty()
    strAmountPaid = ndb.IntegerProperty()
    strBalance = ndb.IntegerProperty()

    def writeAmountOwed(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strAmountOwed = int(strinput)
                return True
            else:
                return False
        except:
            return False

    def writeAmountPaid(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strAmountPaid = int(strinput)
                return True
            else:
                return False
        except:
            return False

    def writeBalance(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBalance = int(strinput)
                return True
            else:
                return False
        except:
            return False

class AdvancedAmount(LoanConstant):
    strCreditAdvancedCapital = ndb.IntegerProperty()
    strInitiationFee = ndb.IntegerProperty()
    strMonthlyServiceFee = ndb.IntegerProperty()
    strMonthlyInterest = ndb.IntegerProperty()
    strFreequency = ndb.StringProperty()
    strNumberInstallments = ndb.IntegerProperty()
    strLoanTerm = ndb.StringProperty()
    strAmountAdvancedToClient = ndb.IntegerProperty()
    strMonthlyInstallments = ndb.IntegerProperty()
    strTotalInstallments = ndb.IntegerProperty()
    strDateTaken = ndb.DateTimeProperty(auto_now_add=True)
    strAdvanceReference = ndb.IntegerProperty()
    strLoanPaidStatus = ndb.BooleanProperty(default=False) # If True it means the loan amount has been paid to client

    strPaymentDate = ndb.IntegerProperty(default=30)

    strTotalAmountRePaid = ndb.IntegerProperty()
    strAdvancedIndex = ndb.IntegerProperty()

    strInstallmentsPaid = ndb.BooleanProperty(default=False)
    strOutStanding = ndb.BooleanProperty(default=False)
    strAccountChange = ndb.BooleanProperty(default=False)






    def setToPaid(self):
        try:
            self.strLoanPaidStatus = True
            return True
        except:
            return False

    def setReference(self):
        try:
            findRequest = AdvancedAmount.query()
            AdvList = findRequest.fetch()

            self.strAdvanceReference = len(AdvList)
            return True
        except:
            return False

    def writeCreditAdvancedCapital (self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strCreditAdvancedCapital = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeInitiationFee(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strInitiationFee = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeMonthlyServiceFee(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strMonthlyServiceFee = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeMonthlyInterest(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strMonthlyInterest = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeFrequency(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strFreequency = strinput
                return True
            else:
                return False
        except:
            return False
    def writeNumberInstallments(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strNumberInstallments = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeLoanTerm(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strLoanTerm = strinput
                return True
            else:
                return False
        except:
            return False
    def writeAmountAdvancedToClient(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strAmountAdvancedToClient = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeMonthlyInstallments(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strMonthlyInstallments = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeTotalInstallments(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strTotalInstallments = int(strinput)
                return True
            else:
                return False
        except:
            return False
class LoanBankingDetails(LoanConstant):
    strAccountHolder = ndb.StringProperty()
    strBankAccountNumber = ndb.StringProperty()
    strBankingInstitution = ndb.StringProperty()
    strBranchCode = ndb.StringProperty()
    strAccountType = ndb.StringProperty()
    strDateCommencement = ndb.DateProperty()

    def writeAccountHolder(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strAccountHolder = strinput
                return True
            else:
                return False
        except:
            return False

    def writeBankAccountNumber(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strBankAccountNumber = strinput
                return True
            else:
                return False
        except:
            return False

    def writeBankingInstitution(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBankingInstitution = strinput
                return True
            else:
                return False
        except:
            return False

    def writeBranchCode(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strBranchCode = strinput
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

    def writeCommencementDate(self,strinput):
        try:
            if not(strinput == None):
                self.strDateCommencement = strinput
                return True
            else:
                return False
        except:
            return False
class LoanReceiver(LoanConstant):
    strNameCreditReceiver = ndb.StringProperty()
    strStandNumber = ndb.StringProperty()
    strStreetName = ndb.StringProperty()
    strCityTown = ndb.StringProperty()
    strProvince = ndb.StringProperty()
    strCountry = ndb.StringProperty()
    strPostalCode = ndb.StringProperty()

    strWorkTel = ndb.StringProperty()
    strHomeTel = ndb.StringProperty()
    strCell = ndb.StringProperty()

    strIDNumber = ndb.StringProperty()
    strEmployer = ndb.StringProperty()
    strDateReceived = ndb.DateProperty(auto_now_add=True)

    def writeNameCreditProvider(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strNameCreditReceiver = strinput
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
    def writeWorkTel(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strWorkTel = strinput
                return True
            else:
                return False
        except:
            return False
    def writeHomeTel(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strHomeTel = strinput
                return True
            else:
                return False
        except:
            return False
    def writeCell(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strCell = strinput
                return True
            else:
                return False
        except:
            return False
    def writeIDNumber(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strIDNumber = strinput
                return True
            else:
                return False
        except:
            return False
    def writeEmployer(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strEmployer = strinput
                return True
            else:
                return False

        except:
            return False
class LoanNotes(LoanConstant):
    strNotes = ndb.StringProperty()
    strSubject = ndb.StringProperty()
    strFullNames = ndb.StringProperty()
    strSurname = ndb.StringProperty()

    strDateTimeTaken = ndb.DateTimeProperty(auto_now_add=True)

    def writeNotes(self,strinput):
        try:
            strinput = str(strinput)

            if not(strinput == None):
                self.strNotes = strinput
                return True
            else:
                return False
        except:
            return False

    def writeSubject(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strSubject = strinput
                return True
            else:
                return False
        except:
            return False

    def writeFullNames(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strFullNames = strinput
                return True
            else:
                return False
        except:
            return False

    def writeSurname(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strSurname = strinput
                return True
            else:
                return False
        except:
            return False
########################################################################################################################
############ Handlers
########################################################################################################################
class LoansHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = WorkingAccount.query(WorkingAccount.strReference == Guser.user_id(), WorkingAccount.strActivated == False)
            WorkingAccountList = findRequest.fetch()

            Working = WorkingAccount()
            if len(WorkingAccountList) > 0:
                Working = WorkingAccountList[0]

                strAccountNumber = Working.strAccountNumber
            else:
                findRequest = WorkingAccount.query(WorkingAccount.strReference == Guser.user_id())
                WorkingAccountList = findRequest.fetch()
                strAccountNumber = Working.createNewAccountNumber(strinput=(len(WorkingAccountList) + 1))
                Working.writeReference(strinput=Guser.user_id())
                Working.writeAccountNumber(strinput=strAccountNumber)
                Working.writeActivated(strinput=False)
                Working.put()

            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == strAccountNumber)
            LoanApplicantList = findRequest.fetch()

            if len(LoanApplicantList) > 0:
                LoanApplicant = LoanApplicantList[0]
            else:
                LoanApplicant = LoanApplicantDetails()


            findRequest = LoanApplicantDetails.query()
            LoansList = findRequest.fetch()

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
            if (Rights.bolIsEmployee) and (Rights.bolEmployeesLoanFormReadAccess):
                template = template_env.get_template('templates/loans.html')
                context = {'vstrAccountNumber':strAccountNumber,'LoanApplicant': LoanApplicant,'ActiveLoansList': LoansList,
                           'UserRights': Rights}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))


    def post(self):
        Guser = users.get_current_user()

        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            vstrTitle = self.request.get('vstrTitle')
            vstrSurname = self.request.get('vstrSurname')
            vstrFullnames = self.request.get('vstrFullnames')
            vstrIDNumber = self.request.get('vstrIDNumber')
            vstrDateofBirth = self.request.get('vstrDateofBirth')
            vstrDateofBirth = str(vstrDateofBirth)
            vstrNationality = self.request.get('vstrNationality')
            vstrCityTown = self.request.get('vstrCityTown')
            vstrHouseNumber = self.request.get('vstrHouseNumber')
            vstrStreetName = self.request.get('vstrStreetName')
            vstrResidentialProvince = self.request.get('vstrResidentialProvince')
            vstrResidentialCountry = self.request.get('vstrResidentialCountry')
            vstrResidentialPostalCode = self.request.get('vstrResidentialPostalCode')

            vstrBoxNumber = self.request.get('vstrBoxNumber')
            vstrPostalAddressCityTown = self.request.get('vstrPostalCityTown')
            vstrPostalProvince = self.request.get('vstrPostalProvince')
            vstrPostalCountry = self.request.get('vstrPostalCountry')
            vstrPostalCode = self.request.get('vstrPostalCode')

            vstrDayTimeNumber = self.request.get('vstrDayTimeNumber')
            vstrCellNumber = self.request.get('vstrCellNumber')
            vstrEmail = self.request.get('vstrEmail')

            vstrNextOfKinNames = self.request.get('vstrNextOfKinNames')
            vstrNextOfKinAddress  = self.request.get('vstrNextOfKinAddress')
            vstrNextOfKinCell = self.request.get('vstrNextOfKinCell')

            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == vstrAccountNumber)
            LoanApplicantList = findRequest.fetch()

            LoanApplicant = LoanApplicantDetails()

            if len(LoanApplicantList) > 0:
                LoanApplicant = LoanApplicantList[0]
            else:
                pass
            try:
                findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
                EmployList = findRequest.fetch()
                if len(EmployList) > 0:
                    Employ = EmployList[0]
                else:
                    Employ = EmploymentDetails()

                findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strIDNumber == vstrIDNumber)
                LoanDuplicateList = findRequest.fetch()

                if len(LoanDuplicateList) == 0:
                    LoanApplicant.writeReference(strinput=Guser.user_id())
                    LoanApplicant.writeAccountNumber(strinput=vstrAccountNumber)
                    LoanApplicant.writeEmployeeCode(strinput=Employ.strEmployeeCode)
                    LoanApplicant.writeSurname(strinput=vstrSurname)
                    LoanApplicant.writeFullNames(strinput=vstrFullnames)
                    LoanApplicant.writeTitle(strinput=vstrTitle)
                    LoanApplicant.writeIDNumber(strinput=vstrIDNumber)

                    DateList = vstrDateofBirth.split("-")
                    year = DateList[0]
                    month = DateList[1]
                    day = DateList[2]

                    tempDate = datetime.date(year=int(year),month=int(month),day=int(day))


                    LoanApplicant.writeDateOfBirth(strinput=tempDate)
                    LoanApplicant.writeNationality(strinput=vstrNationality)
                    LoanApplicant.writeHouseNumber(strinput=vstrHouseNumber)
                    LoanApplicant.writeStreetName(strinput=vstrStreetName)
                    LoanApplicant.writeCityTown(strinput=vstrCityTown)
                    LoanApplicant.writeProvince(strinput=vstrResidentialProvince)
                    LoanApplicant.writeCountry(strinput=vstrResidentialCountry)
                    LoanApplicant.writePostalCode(strinput=vstrResidentialPostalCode)

                    LoanApplicant.writeBoxNumber(strinput=vstrBoxNumber)
                    LoanApplicant.writePostalCityTown(strinput=vstrPostalAddressCityTown)
                    LoanApplicant.writePostalProvince(strinput=vstrPostalProvince)
                    LoanApplicant.writePostalCountry(strinput=vstrPostalCountry)
                    LoanApplicant.writePostalPostalCode(strinput=vstrPostalCode)

                    LoanApplicant.writeTel(strinput=vstrDayTimeNumber)
                    LoanApplicant.writeCell(strinput=vstrCellNumber)
                    LoanApplicant.writeEmail(strinput=vstrEmail)

                    LoanApplicant.writeNextOfKinNames(strinput=vstrNextOfKinNames)
                    LoanApplicant.writeNextOfKinAddress(strinput=vstrNextOfKinAddress)
                    LoanApplicant.writeNextOfKinCell(strinput=vstrNextOfKinCell)

                    LoanApplicant.put()
                    self.response.write("Succesfully Updated the Loan Application Database")
                else:
                    self.response.write("Duplicate Error - Your Client already have an account- or you made an error with the ID Number")

            except:
                self.response.write("Error Occured while updating your Loan Applicant Database")

            #TODO- Finish this up and make sure the data actually get saved and also attached to the employee code
class LoansApplicationsHandler(webapp2.RequestHandler):
    def get(self):
        pass
class LoansEmploymentDetailsHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            findRequest = LoanEmploymentDetails.query(LoanEmploymentDetails.strAccountNumber == vstrAccountNumber)
            LoanEmploymentDetailsList = findRequest.fetch()

            if len(LoanEmploymentDetailsList) > 0:
                LoanEmployment = LoanEmploymentDetailsList[0]
            else:
                LoanEmployment = LoanEmploymentDetails()

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
                template = template_env.get_template('templates/dynamic/loans/EmployementDetails.html')
                context = {'Employment': LoanEmployment,'UserRights': Rights}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))

    def post(self):
        try:
            Guser = users.get_current_user()
            if Guser:
                vstrAccountNumber = self.request.get('vstrAccountNumber')
                vstrNameOfEmployer = self.request.get('vstrNameOfEmployer')
                vstrEmployeeNumber = self.request.get('vstrEmployeeNumber')
                vstrDepartment = self.request.get('vstrDepartment')
                vstrEmployeeKind = self.request.get('vstrEmployeeKind')
                vstrContract = self.request.get('vstrContracts')
                vstrDateJoined = str(self.request.get('vstrDateJoined'))
                vstrStandNumber = self.request.get('vstrStandNumber')
                vstrStreetName = self.request.get('vstrStreetName')
                vstrTownCity = self.request.get('vstrTownCity')
                vstrProvince = self.request.get('vstrProvince')
                vstrCountry = self.request.get('vstrCountry')
                vstrPostalCode = self.request.get('vstrPostalCode')

                try:
                    Employment = LoanEmploymentDetails()
                    Employment.writeReference(strinput=Guser.user_id())
                    Employment.writeAccountNumber(strinput=vstrAccountNumber)
                    Employment.writeNameOfEmployer(strinput=vstrNameOfEmployer)
                    Employment.writeEmployeeNumber(strinput=vstrEmployeeNumber)
                    Employment.writeDepartment(strinput=vstrDepartment)
                    Employment.writeEmployeeKind(strinput=vstrEmployeeKind)
                    Employment.writeContract(strinput=vstrContract)
                    DateList = vstrDateJoined.split("-")

                    year = int(DateList[0])
                    month = int(DateList[1])
                    day = int(DateList[2])

                    vstrDateJoined = datetime.date(year=year,month=month,day=day)
                    Employment.writeDateJoined(vstrDateJoined)
                    Employment.writeStandNumber(strinput=vstrStandNumber)
                    Employment.writeStreetName(strinput=vstrStreetName)
                    Employment.writeTownCity(strinput=vstrTownCity)
                    Employment.writeProvince(strinput=vstrProvince)
                    Employment.writeCountry(strinput=vstrCountry)
                    Employment.writePostalCode(strinput=vstrPostalCode)

                    Employment.put()
                    self.response.write("Succesfully Saved Employment Details")
                except:
                    self.response.write("An Error Occured while Saving Employment Details")

            else:
                pass
        except:
            self.response.write("A Fatal Error Occured while Saving Employment Details")
class LoansCreditProviderHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            findRequest = BranchDetails.query()
            BranchList = findRequest.fetch()

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            EmployeeList = findRequest.fetch()

            findRequest = CreditProvider.query(CreditProvider.strAccountNumber == vstrAccountNumber)
            CreditProviderList = findRequest.fetch()

            if len(CreditProviderList) > 0:
                CreditProviderDetail = CreditProviderList[0]
            else:
                CreditProviderDetail = CreditProvider()




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
                template = template_env.get_template('templates/dynamic/loans/CreditProvider.html')
                context = {'BranchList' : BranchList, 'EmployeeList': EmployeeList, 'CreditProviderDetail':CreditProviderDetail,
                           'UserRights': Rights}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))


    def post(self):
        Guser = users.get_current_user()
        if Guser:
            self.response.write("Credit Provider Saving Database")
class AdvancedAmountHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == vstrAccountNumber)
            AdvancedList = findRequest.fetch()

            if len(AdvancedList) > 0:
                Advanced = AdvancedList[len(AdvancedList) - 1]
            else:
                Advanced = AdvancedAmount()


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
                template = template_env.get_template('templates/dynamic/loans/AdvanceAmount.html')
                context = {'Advanced': Advanced,'UserRights': Rights}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            vstrCreditAdvanceCapital = self.request.get('vstrCreditAdvanceCapital')
            vstrInitiationFee = self.request.get('vstrInitiationFee')
            vstrMonthlyFee = self.request.get('vstrMonthlyFee')
            vstrMonthlyInterestRate = self.request.get('vstrMonthlyInterestRate')
            vstrFreequency = self.request.get('vstrFreequency')
            vstrNumberInstallments = self.request.get('vstrNumberInstallments')
            vstrLoanTerm = self.request.get('vstrLoanTerm')
            vstrAmountAdvancedToClient = self.request.get('vstrAmountAdvancedToClient')
            vstrMonthlyInstallment = self.request.get('vstrMonthlyInstallment')
            vstrTotalInstallments = self.request.get('vstrTotalInstallments')

            Advanced = AdvancedAmount()
            try:
                findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
                EmployList = findRequest.fetch()
                if len(EmployList) > 0:
                    Employ = EmployList[0]
                else:
                    Employ = EmploymentDetails()

                findRequest = AdvancedAmount.query()
                AdvancedList = findRequest.fetch()


                Advanced.writeReference(strinput=Guser.user_id())
                Advanced.writeAccountNumber(strinput=vstrAccountNumber)
                Advanced.writeEmployeeCode(strinput=Employ.strEmployeeCode)
                Advanced.writeCreditAdvancedCapital(strinput=vstrCreditAdvanceCapital)
                Advanced.writeInitiationFee(strinput=vstrInitiationFee)
                Advanced.writeMonthlyServiceFee(strinput=vstrMonthlyFee)
                Advanced.writeMonthlyInterest(strinput=vstrMonthlyInterestRate)
                Advanced.writeFrequency(strinput=vstrFreequency)
                Advanced.writeNumberInstallments(strinput=vstrNumberInstallments)
                Advanced.writeLoanTerm(strinput=vstrLoanTerm)
                Advanced.writeAmountAdvancedToClient(strinput=vstrAmountAdvancedToClient)
                Advanced.writeMonthlyInstallments(strinput=vstrMonthlyInstallment)
                Advanced.writeTotalInstallments(strinput=vstrTotalInstallments)
                Advanced.strAdvancedIndex = len(AdvancedList)
                Advanced.setReference()

                Advanced.put()
                self.response.write("Succesfully updated advanced amount")
            except:
                self.response.write("Error Updating Advanced Amount Data")
class IncomeExpenditureHandler(webapp2.RequestHandler):
    def get(self):

        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')

            IncExpense = IncomeExpense()
            findRequest = IncomeExpense.query(IncomeExpense.strAccountNumber == vstrAccountNumber)
            IncomeExpenseList = findRequest.fetch()

            if len(IncomeExpenseList) > 0:
                IncExpense = IncomeExpenseList[0]
            else:
                pass

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
                template = template_env.get_template('templates/dynamic/loans/IncomeExpenditure.html')
                context = {'IncExpense': IncExpense,'UserRights': Rights}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))


    def post(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            vstrIncomeAfterDeduction = self.request.get('vstrIncomeAfterDeduction')
            vstrOverTime = self.request.get('vstrOverTime')
            vstrCommission = self.request.get('vstrCommission')
            vstrOtherIncome = self.request.get('vstrOtherIncome')
            vstrTotalIncome = self.request.get('vstrTotalIncome')
            vstrBondRepayments = self.request.get('vstrBondRepayments')
            vstrLoanInstallments = self.request.get('vstrLoanInstallments')
            vstrWaterElectricityTel = self.request.get('vstrWaterElectricityTel')
            vstrInsurance = self.request.get('vstrInsurance')
            vstrChildrenMaintenance = self.request.get('vstrChildrenMaintenance')
            vstrVehicleMaintenance = self.request.get('vstrVehicleMaintenance')
            vstrBasicNecessities = self.request.get('vstrBasicNecessities')
            vstrDomesticWages = self.request.get('vstrDomesticWages')
            vstrEducation = self.request.get('vstrEducation')
            vstrOtherExpenses = self.request.get('vstrOtherExpenses')
            vstrTotalExpenses = self.request.get('vstrTotalExpenses')
            vstrAffordability = self.request.get('vstrAffordability')


            findRequest = IncomeExpense.query(IncomeExpense.strAccountNumber == vstrAccountNumber)
            IncomeExpenseList = findRequest.fetch()

            if len(IncomeExpenseList) > 0:
                IncExpense = IncomeExpenseList[0]
            else:
                IncExpense = IncomeExpense()


            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            EmployList = findRequest.fetch()

            if len(EmployList) > 0:
                Employ = EmployList[0]
            else:
                Employ = EmploymentDetails()

            IncExpense.writeReference(strinput=Guser.user_id())
            IncExpense.writeAccountNumber(strinput=vstrAccountNumber)
            IncExpense.writeEmployeeCode(strinput=Employ.strEmployeeCode)
            logging.info("Income After Deduction : " + vstrIncomeAfterDeduction)
            IncExpense.writeIncomeAfterDeduction(strinput=vstrIncomeAfterDeduction)
            IncExpense.writeOverTime(strinput=vstrOverTime)
            logging.info("Overtime : "  + vstrOverTime)
            IncExpense.writeCommission(strinput=vstrCommission)
            IncExpense.writeOtherIncome(strinput=vstrOtherIncome)
            IncExpense.writeTotalIncome(strinput=vstrTotalIncome)
            IncExpense.writeBondRepayments(strinput=vstrBondRepayments)
            IncExpense.writeLoanInstallements(strinput=vstrLoanInstallments)
            IncExpense.writeWaterElectricity(strinput=vstrWaterElectricityTel)
            IncExpense.writeInsurance(strinput=vstrInsurance)
            IncExpense.writeChildrenMaintanance(strinput=vstrChildrenMaintenance)
            IncExpense.writeVehicleMaintenance(strinput=vstrVehicleMaintenance)
            IncExpense.writeBasicNecessity(strinput=vstrBasicNecessities)
            IncExpense.writeDomesticWages(strinput=vstrDomesticWages)
            IncExpense.writeEducation(strinput=vstrEducation)
            IncExpense.writeOtherExpenses(strinput=vstrOtherExpenses)
            IncExpense.writeTotalExpenses(strinput=vstrTotalExpenses)
            IncExpense.writeAffordability(strinput=vstrAffordability)

            try:
                IncExpense.put()
                self.response.write("Income and Expense Saved")
            except:
                self.response.write("Error Saving Income and Expense")
class ClientBankingDetailsHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            findRequest = LoanBankingDetails.query(LoanBankingDetails.strAccountNumber == vstrAccountNumber)
            BankingDetailsList = findRequest.fetch()

            if len(BankingDetailsList) > 0:
                Banking = BankingDetailsList[0]
            else:
                Banking = LoanBankingDetails()


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
                template = template_env.get_template('templates/dynamic/loans/ClientBankingDetails.html')
                context = {'Banking':Banking,'UserRights': Rights}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))


    def post(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            vstrAccountHolder = self.request.get('vstrAccountHolder')
            vstrBankAccountNumber = self.request.get('vstrBankAccountNumber')
            vstrBankingInstitution = self.request.get('vstrBankingInstitution')
            vstrBranchCode = self.request.get('vstrBranchCode')
            vstrAccountType = self.request.get('vstrAccountType')
            vstrCommencementDate = self.request.get('vstrCommencementDate')

            findRequest = LoanBankingDetails.query(LoanBankingDetails.strAccountNumber == vstrAccountNumber)
            BankingList = findRequest.fetch()

            if len(BankingList) > 0:
                Banking = BankingList[0]
            else:
                Banking = LoanBankingDetails()

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            EmployeeList = findRequest.fetch()
            if len(EmployeeList) > 0:
                Employee = EmployeeList[0]
            else:
                Employee = EmploymentDetails()

            try:
                Banking.writeReference(strinput=Guser.user_id())
                Banking.writeEmployeeCode(strinput=Employee.strEmployeeCode)
                Banking.writeAccountNumber(strinput=vstrAccountNumber)
                Banking.writeAccountHolder(strinput=vstrAccountHolder)
                Banking.writeBankAccountNumber(strinput=vstrBankAccountNumber)
                Banking.writeBankingInstitution(strinput=vstrBankingInstitution)
                Banking.writeBranchCode(strinput=vstrBranchCode)
                Banking.writeAccountType(strinput=vstrAccountType)
                DateList = vstrCommencementDate.split("-")
                year = int(DateList[0])
                month = int(DateList[1])
                day = int(DateList[2])
                vstrCommencementDate = datetime.date(year=year,month=month,day=day)
                Banking.writeCommencementDate(strinput=vstrCommencementDate)

                Banking.put()

                self.response.write("Succesfully updated Banking Details")
            except:
                self.response.write("Error Updating Banking Details")
class CopyFromApplicantHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')

            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber  == vstrAccountNumber)
            LoanApplicantList = findRequest.fetch()
            LoanApplicant = LoanApplicantDetails()
            if len(LoanApplicantList) > 0:
                LoanApplicant = LoanApplicantList[0]
            else:
                pass



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
                context = {'LoanApplicant' : LoanApplicant,'UserRights':Rights}
                template = template_env.get('templates/dynamic/temp/applicanttemp.html')
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))

class CloseAccountNumberHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:

            vstrAccountNumber = self.request.get('vstrAccountNumber')
            findRequest = WorkingAccount.query(WorkingAccount.strAccountNumber == vstrAccountNumber)
            WorkingAccountList = findRequest.fetch()

            for Working in WorkingAccountList:
                Working.strActivated = True
                Working.put()

            self.response.write("Account Number : " + vstrAccountNumber + "  has been closed refresh to create a new one")

class CreateFileHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == vstrAccountNumber)
            LoanApplicantList = findRequest.fetch()

            if len(LoanApplicantList) > 0:
                LoanApplicant = LoanApplicantList[0]
            else:
                LoanApplicant = LoanApplicantDetails()


            findRequest = LoanEmploymentDetails.query(LoanEmploymentDetails.strAccountNumber == vstrAccountNumber)
            EmploymentList = findRequest.fetch()

            if len(EmploymentList) > 0:
                Employment = EmploymentList[0]
            else:
                Employment = EmploymentDetails()

            findRequest = IncomeExpense.query(IncomeExpense.strAccountNumber == vstrAccountNumber)
            IncomeExpList = findRequest.fetch()

            if len(IncomeExpList) > 0:
                IncomeExp = IncomeExpList[0]
            else:
                IncomeExp = IncomeExpense()

            findRequest = CreditProvider.query(CreditProvider.strAccountNumber == vstrAccountNumber)
            CreditProviderList = findRequest.fetch()

            if len(CreditProviderList) > 0:
                Creditor = CreditProviderList[0]
            else:
                Creditor = CreditProvider()

            findRequest = LoanReceiver.query(LoanReceiver.strAccountNumber == vstrAccountNumber)
            LoanReceiverList = findRequest.fetch()

            if len(LoanReceiverList) > 0:
                LoanClient = LoanReceiverList[0]
            else:
                LoanClient = LoanReceiver()

            findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == vstrAccountNumber)
            AmountAdvancedList = findRequest.fetch()

            if len(AmountAdvancedList) > 0:
                AmountAdvanced = AmountAdvancedList[0]
            else:
                AmountAdvanced = AdvancedAmount()

            findRequest = LoanBankingDetails.query(LoanBankingDetails.strAccountNumber == vstrAccountNumber)
            BankingList = findRequest.fetch()

            if len(BankingList) > 0:
                Banking = BankingList[0]
            else:
                Banking = LoanBankingDetails()



            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == LoanApplicant.strReference)
            EmployList = findRequest.fetch()
            if len(EmployList) > 0:
                Employ = EmployList[0]
            else:
                Employ = EmploymentDetails()

            findRequest = UserRights.query(UserRights.strReference == Guser.user_id())
            RightsList = findRequest.fetch()

            if len(RightsList) > 0:
                Rights = RightsList[0]
            else:
                Rights = UserRights()

            if Rights.bolIsEmployee:
                template = template_env.get_template("templates/dynamic/loans/createfile.html")
                context = {'LoanApplicant': LoanApplicant , 'Employment': Employment ,'Employ':Employ, 'IncomeExp': IncomeExp, 'Creditor': Creditor,
                           'LoanClient': LoanClient,'AmountAdvanced':AmountAdvanced,'Banking':Banking,'UserRights': Rights}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template("templates/500.html")
                context = {}
                self.response.write(template.render(context))

class ActivateLoanHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            vstrALLPS = self.request.get('vstrALLPS')
            vstrPayDay = self.request.get('vstrPayDay')


            findRequest = Loan.query(Loan.strAccountNumber == vstrAccountNumber)
            LoanList = findRequest.fetch()
            try:
                if len(LoanList) > 0:
                    thisLoan = LoanList[0]
                else:
                    thisLoan = Loan()

                findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == vstrAccountNumber)
                AmountAdvancedList = findRequest.fetch()

                if len(AmountAdvancedList) > 0:
                    AmountAdvanced = AmountAdvancedList[0]
                else:
                    AmountAdvanced = AdvancedAmount()


                if AmountAdvanced.strCreditAdvancedCapital > 10:
                    thisLoan.writeReference(strinput=Guser.user_id())
                    thisLoan.writeAccountNumber(strinput=vstrAccountNumber)
                    thisLoan.writeBalance(strinput=str(AmountAdvanced.strAmountAdvancedToClient))
                    today = datetime.datetime.now()
                    today = today.date()
                    thisLoan.writeDateLoaned(strinput=today)
                    thisLoan.writeLoanedAmount(strinput=str(AmountAdvanced.strCreditAdvancedCapital))

                    thisLoan.writePaymentDate(strinput=vstrPayDay)

                    AmountAdvanced.strPaymentDate = int(vstrPayDay)

                    findRequest = LoanEmploymentDetails.query(LoanEmploymentDetails.strReference == Guser.user_id())
                    EmploymentList = findRequest.fetch()
                    if len(EmploymentList) > 0:
                        Employment = EmploymentList[0]
                    else:
                        Employment = LoanEmploymentDetails()
                    thisLoan.writeEmployeeCode(strinput=Employment.strEmployeeCode)
                    thisLoan.ActivateLoan()
                    thisLoan.put()

                    findRequest = WorkingAccount.query(WorkingAccount.strAccountNumber == vstrAccountNumber)
                    WorkingList = findRequest.fetch()

                    if len(WorkingList) > 0:
                        Working = WorkingList[0]
                    else:
                        Working = WorkingAccount()

                    Working.strActivated = True
                    Working.put()

                    findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == vstrAccountNumber)
                    LoanDetailList = findRequest.fetch()

                    if len(LoanDetailList) > 0:
                        LoanDetail = LoanDetailList[0]
                    else:
                        LoanDetail = LoanApplicantDetails()

                    LoanDetail.writeALLPS(strinput=vstrALLPS)
                    LoanDetail.put()

                    findRequest = UserRights.query(UserRights.bolEmployeeLoanFormSendPayment  == True)
                    AdminUSersList = findRequest.fetch()

                    for AdminUser in AdminUSersList:
                        Task = Tasks()
                        Task.writeReference(strinput=Guser.user_id())
                        Task.writeTaskNote(strinput="Payment for loan")
                        PaymentURL = "/loans/list/" + vstrAccountNumber
                        Task.writeTaskURL(strinput=PaymentURL)
                        Task.writeTaskType(strinput="Admin")
                        Task.writeToReference(strinput=AdminUser.strReference)
                        Task.writeReference(strinput=Guser.user_id())
                        Task.put()

                    thisActivity = Activity()
                    thisActivity.writeReference(strinput=Guser.user_id())
                    thisActivity.writeAction(strinput="Loan")
                    thisLeadLink = "/loans/list/" + str(LoanDetail.strAccountNumber)
                    thisActivity.writeActionLink(strinput=thisLeadLink)
                    thisActivity.put()

                    self.response.write("""
                    Loan Successfully Activated <a href="/employees/loans" type="button" class="btn btn-warning btn-block" >Close Loan Application</a>
                    """)
                else:
                    self.response.write("Loan Cannot be activated please fill in proper loan details first")
            except:
                self.response.write("Error Activating Loan")
class LoansActivateFormHandler(webapp2.RequestHandler):
    def get(self):
        try:
            template = template_env.get_template('templates/dynamic/loans/activate.html')
            context = {}
            self.response.write(template.render(context))
        except:
            pass
class PrintLoansHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = ActiveLoan.query(ActiveLoan.strReference == Guser.user_id())
            ActiveList = findRequest.fetch()
            if len(ActiveList) > 0:
                Active = ActiveList[0]
            else:
                Active = ActiveLoan()

            vstrAccountNumber = Active.strAccountNumber
            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == vstrAccountNumber)
            LoanApplicantList = findRequest.fetch()

            if len(LoanApplicantList) > 0:
                LoanApplicant = LoanApplicantList[0]
            else:
                LoanApplicant = LoanApplicantDetails()
            findRequest = LoanEmploymentDetails.query(LoanEmploymentDetails.strAccountNumber == vstrAccountNumber)
            EmploymentList = findRequest.fetch()

            if len(EmploymentList) > 0:
                Employment = EmploymentList[0]
            else:
                Employment = LoanEmploymentDetails()

            findRequest = IncomeExpense.query(IncomeExpense.strAccountNumber == vstrAccountNumber)
            IncomeExpList = findRequest.fetch()

            if len(IncomeExpList) > 0:
                IncomeExp = IncomeExpList[0]
            else:
                IncomeExp = IncomeExpense()

            findRequest = CreditProvider.query(CreditProvider.strAccountNumber == vstrAccountNumber)
            CreditProviderList = findRequest.fetch()

            if len(CreditProviderList) > 0:
                Creditor = CreditProviderList[0]
            else:
                Creditor = CreditProvider()

            findRequest = LoanReceiver.query(LoanReceiver.strAccountNumber == vstrAccountNumber)
            LoanReceiverList = findRequest.fetch()

            if len(LoanReceiverList) > 0:
                LoanClient = LoanReceiverList[0]
            else:
                LoanClient = LoanReceiver()

            findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == vstrAccountNumber)
            AmountAdvancedList = findRequest.fetch()

            if len(AmountAdvancedList) > 0:
                AmountAdvanced = AmountAdvancedList[len(AmountAdvancedList) - 1]
            else:
                AmountAdvanced = AdvancedAmount()

            findRequest = LoanBankingDetails.query(LoanBankingDetails.strAccountNumber == vstrAccountNumber)
            BankingList = findRequest.fetch()

            if len(BankingList) > 0:
                Banking = BankingList[0]
            else:
                Banking = LoanBankingDetails()

            vstrTodayDate = datetime.datetime.now()
            vstrTodayDate = vstrTodayDate.date()

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            EmployList = findRequest.fetch()

            if len(EmployList) > 0:
                Employee = EmployList[0]
            else:
                Employee = EmploymentDetails()

            template = template_env.get_template("templates/dynamic/loans/printfile.html")
            context = {'vstrTodayDate':vstrTodayDate,'LoanApplicant': LoanApplicant, 'Employment': Employment, 'IncomeExp': IncomeExp,
                       'Creditor': Creditor, 'Employee':Employee,
                       'LoanClient': LoanClient, 'AmountAdvanced': AmountAdvanced, 'Banking': Banking}
            self.response.write(template.render(context))
class LoansListHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:
            URL = str(self.request.uri)
            URLlist = URL.split("/")
            vstrAccountNumber = URLlist[len(URLlist) - 1]
            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == vstrAccountNumber)
            LoanApplicantList = findRequest.fetch()

            if len(LoanApplicantList) > 0:
                LoanApplicant = LoanApplicantList[0]
            else:
                LoanApplicant = LoanApplicantDetails()

            findRequest = LoanEmploymentDetails.query(LoanEmploymentDetails.strAccountNumber == vstrAccountNumber)
            EmploymentList = findRequest.fetch()

            if len(EmploymentList) > 0:
                Employment = EmploymentList[0]
            else:
                Employment = LoanEmploymentDetails()

            findRequest = IncomeExpense.query(IncomeExpense.strAccountNumber == vstrAccountNumber)
            IncomeExpList = findRequest.fetch()

            if len(IncomeExpList) > 0:
                IncomeExp = IncomeExpList[0]
            else:
                IncomeExp = IncomeExpense()

            findRequest = CreditProvider.query(CreditProvider.strAccountNumber == vstrAccountNumber)
            CreditProviderList = findRequest.fetch()

            if len(CreditProviderList) > 0:
                Creditor = CreditProviderList[0]
            else:
                Creditor = CreditProvider()

            findRequest = LoanReceiver.query(LoanReceiver.strAccountNumber == vstrAccountNumber)
            LoanReceiverList = findRequest.fetch()

            if len(LoanReceiverList) > 0:
                LoanClient = LoanReceiverList[0]
            else:
                LoanClient = LoanReceiver()

            findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == vstrAccountNumber)
            AmountAdvancedList = findRequest.fetch()

            if len(AmountAdvancedList) > 0:
                AmountAdvanced = AmountAdvancedList[0]
            else:
                AmountAdvanced = AdvancedAmount()

            findRequest = LoanBankingDetails.query(LoanBankingDetails.strAccountNumber == vstrAccountNumber)
            BankingList = findRequest.fetch()

            if len(BankingList) > 0:
                Banking = BankingList[0]
            else:
                Banking = LoanBankingDetails()

            vstrTodayDate = datetime.datetime.now()
            vstrTodayDate = vstrTodayDate.date()

            findRequest = LoanNotes.query(LoanNotes.strAccountNumber == vstrAccountNumber)
            NotesList = findRequest.fetch()

            ActivateLoan = ActiveLoan()
            ActivateLoan.setActiveLoan(strReference=Guser.user_id(),strAccountNumber=vstrAccountNumber)


            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == LoanApplicant.strReference)
            EmployList = findRequest.fetch()
            if len(EmployList) > 0:
                Employ = EmployList[0]
            else:
                Employ = EmploymentDetails()



            findRequest = UserRights.query(UserRights.strReference == Guser.user_id())
            RightsList = findRequest.fetch()

            if len(RightsList) > 0:
                Rights = RightsList[0]
            else:
                Rights = UserRights()

            if Rights.bolIsEmployee:
                template = template_env.get_template('templates/dynamic/loans/LoanDetail.html')
                context = {'vstrTodayDate': vstrTodayDate, 'LoanApplicant': LoanApplicant, 'Employment': Employment,
                           'IncomeExp': IncomeExp,'Creditor': Creditor, 'LoanClient': LoanClient,
                           'AmountAdvanced': AmountAdvanced, 'Banking': Banking, 'NotesList': NotesList,'UserRights':Rights,
                           'Employee':Employ}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))


class RenewLoanHandler(webapp2.RequestHandler):
    """
        Renew Loan Must attach a new advance amount record to the present one

        This means that Advance Amount Records must be loaded as an Array or List wherever they are loaded
    """
    def get(self):
        Guser = users.get_current_user()
        if Guser:


            findRequest = ActiveLoan.query(ActiveLoan.strReference == Guser.user_id(), ActiveLoan.strLoanActive == True)
            ActiveLoanList = findRequest.fetch()

            if len(ActiveLoanList) > 0:
                Actives = ActiveLoanList[0]
            else:
                Actives = ActiveLoan()

            findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == Actives.strAccountNumber)
            AdvanceList = findRequest.fetch()

            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == Actives.strAccountNumber)
            LoanApplicantList = findRequest.fetch()
            if len(LoanApplicantList) > 0:
                LoanApplicant = LoanApplicantList[0]
            else:
                LoanApplicant = LoanApplicantDetails()

            template = template_env.get_template('templates/dynamic/loans/RenewLoan.html')
            context = {'LoanApplicant':LoanApplicant,'AdvanceList':AdvanceList}
            self.response.write(template.render(context))

class RenewPrintHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()

        if Guser:

            findRequest = ActiveLoan.query(ActiveLoan.strReference == Guser.user_id(), ActiveLoan.strLoanActive == True)
            ActiveLoanList = findRequest.fetch()

            if len(ActiveLoanList) > 0:
                Actives = ActiveLoanList[0]
            else:
                Actives = ActiveLoan()

            findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == Actives.strAccountNumber).order(AdvancedAmount.strDateTaken)
            AdvanceList = findRequest.fetch()

            if len(AdvanceList) > 0:
                Advanced = AdvanceList[len(AdvanceList) - 1]
            else:
                Advanced = AdvancedAmount()



            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == Actives.strAccountNumber)
            LoanApplicantList = findRequest.fetch()

            if len(LoanApplicantList) > 0:
                LoanApplicant = LoanApplicantList[0]
            else:
                LoanApplicant = LoanApplicantDetails()

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            EmployList = findRequest.fetch()

            if len(EmployList) > 0:
                Employee = EmployList[0]
            else:
                Employee = EmploymentDetails()

            vstrTodayDate = datetime.datetime.now()
            vstrTodayDate = vstrTodayDate.date()


            template = template_env.get_template('templates/dynamic/loans/RenewLoanPrint.html')
            context = {'LoanApplicant': LoanApplicant, 'AmountAdvanced': Advanced,'Employee': Employee,'vstrTodayDate':vstrTodayDate}
            self.response.write(template.render(context))


class NotesHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Loading Notes....")
        vstrAccountNumber = self.request.get('vstrAccountNumber')
        findRequest = LoanNotes.query(LoanNotes.strAccountNumber == vstrAccountNumber)
        NotesList = findRequest.fetch()

        template = template_env.get_template('templates/dynamic/loans/noteslist.html')
        context = {'NotesList': NotesList}
        self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()

        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            vstrNoteSubject = self.request.get('vstrNoteSubject')
            vstrNote = self.request.get('vstrNote')

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            EmployList = findRequest.fetch()

            if len(EmployList) > 0:
                Employee = EmployList[0]
            else:
                Employee = EmploymentDetails()

            newNotes = LoanNotes()
            newNotes.writeAccountNumber(strinput=vstrAccountNumber)
            newNotes.writeReference(strinput=Guser.user_id())
            newNotes.writeEmployeeCode(strinput=Employee.strEmployeeCode)
            newNotes.writeFullNames(strinput=Employee.strFullNames)
            newNotes.writeSurname(strinput=Employee.strSurname)
            newNotes.writeSubject(strinput=vstrNoteSubject)
            newNotes.writeNotes(strinput=vstrNote)
            newNotes.put()

            findRequest = LoanNotes.query(LoanNotes.strAccountNumber == vstrAccountNumber)
            NotesList = findRequest.fetch()

            template = template_env.get_template('templates/dynamic/loans/noteslist.html')
            context = {'NotesList':NotesList}
            self.response.write(template.render(context))
        else:
            template = template_env.get_template('templates/dynamic/loans/noteslist.html')
            context = {}
            self.response.write(template.render(context))
class PrintSettlementHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:

            vstrTodayDate = datetime.datetime.now()
            vstrTodayDate = vstrTodayDate.date()

            findRequest = ActiveLoan.query(ActiveLoan.strReference == Guser.user_id(),ActiveLoan.strLoanActive == True)
            ActiveLoanList = findRequest.fetch()

            if len(ActiveLoanList) > 0:
                ActivatedLoan = ActiveLoanList[0]
            else:
                ActivatedLoan = ActiveLoan()

            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == ActivatedLoan.strAccountNumber)
            LoanAppList = findRequest.fetch()

            if len(LoanAppList) > 0:
                LoanApplicant = LoanAppList[0]
            else:
                LoanApplicant = LoanApplicantDetails()

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
                template = template_env.get_template('templates/dynamic/loans/settlement.html')
                context = {'vstrTodayDate' : vstrTodayDate, 'LoanApplicant' : LoanApplicant}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('template/500.html')
                context = {}
                self.response.write(template.render(context))
        else:
            pass
class PrintPaidUpHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrTodayDate = datetime.datetime.now()
            vstrTodayDate = vstrTodayDate.date()
            findRequest = ActiveLoan.query(ActiveLoan.strReference == Guser.user_id(), ActiveLoan.strLoanActive == True)
            ActiveLoanList = findRequest.fetch()

            if len(ActiveLoanList) > 0:
                ActivatedLoan = ActiveLoanList[0]
            else:
                ActivatedLoan = ActiveLoan()

            findRequest = LoanApplicantDetails.query(
                LoanApplicantDetails.strAccountNumber == ActivatedLoan.strAccountNumber)
            LoanAppList = findRequest.fetch()

            if len(LoanAppList) > 0:
                LoanApplicant = LoanAppList[0]
            else:
                LoanApplicant = LoanApplicantDetails()

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
                template = template_env.get_template('templates/dynamic/loans/paidup.html')
                context = {'LoanApplicant': LoanApplicant, 'vstrTodayDate': vstrTodayDate}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('template/500.html')
                context = {}
                self.response.write(template.render())

class EditLoanHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            self.response.write("Edit Loan Called..")
            vstrUserAccountNumber = self.request.get('vstrAccountNumber')

            findRequest = WorkingAccount.query(WorkingAccount.strReference == Guser.user_id())
            MyWorkingAccounts = findRequest.fetch()

            for working in MyWorkingAccounts:
                if working.strActivated == False :
                    working.strActivated = True
                    working.put()

            findRequest = WorkingAccount.query(WorkingAccount.strAccountNumber == vstrUserAccountNumber)
            WorkingAccountList = findRequest.fetch()

            if len(WorkingAccountList) > 0:
                Working = WorkingAccountList[0]
            else:
                Working = WorkingAccount()

            Working.writeAccountNumber(strinput=vstrUserAccountNumber)
            Working.writeReference(strinput=Guser.user_id())
            Working.writeActivated(strinput=False)
            Working.put()
            self.response.write("""
            <h4>Edit Loan Activated</h4>
            <a href="/employees/loans" class="btn btn-success btn-block">Edit Loan</a>
            """)

    def post(self):
        self.response.write("Edit Loans")

class DeleteLoanHandler(webapp2.RequestHandler):
    def get(self):

        Guser = users.get_current_user()

        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')

            try:
                findRequests = Loan.query(Loan.strAccountNumber == vstrAccountNumber)
                LoanList = findRequests.fetch()
                for loan in LoanList:
                    loan.key.delete()

                findRequests = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == vstrAccountNumber)
                LoanAppList = findRequests.fetch()
                for loanApp in LoanAppList:
                    loanApp.key.delete()

                findRequests = LoanEmploymentDetails.query(LoanEmploymentDetails.strAccountNumber == vstrAccountNumber)
                LoanEmploymentList = findRequests.fetch()
                for loanEmployment in LoanEmploymentList:
                    loanEmployment.key.delete()


                findRequests = CreditProvider.query(CreditProvider.strAccountNumber == vstrAccountNumber)
                CreditProList = findRequests.fetch()
                for creditpro in CreditProList:
                    creditpro.key.delete()

                findRequests = IncomeExpense.query(IncomeExpense.strAccountNumber == vstrAccountNumber)
                IncomeExpList = findRequests.fetch()
                for incomeExp in IncomeExpList:
                    incomeExp.key.delete()


                findRequests = AdvancedAmount.query(AdvancedAmount.strAccountNumber == vstrAccountNumber)
                AdvancedList = findRequests.fetch()
                for advanced in AdvancedList:
                    advanced.key.delete()

                findRequests = LoanBankingDetails.query(LoanBankingDetails.strAccountNumber == vstrAccountNumber)
                LoanBankingList = findRequests.fetch()
                for banking in LoanBankingList:
                    banking.key.delete()

                findRequests = LoanReceiver.query(LoanReceiver.strAccountNumber == vstrAccountNumber)
                LoanReceiveList = findRequests.fetch()
                for loanreceive in LoanReceiveList:
                    loanreceive.key.delete()

                findRequests = LoanNotes.query(LoanNotes.strAccountNumber == vstrAccountNumber)
                LoanNotesList = findRequests.fetch()
                for notes in LoanNotesList:
                    notes.key.delete()

                self.response.write("All Records deleted")
            except:
                self.response.write("Error Deleting Records")


class ReprintLoanHandler(webapp2.RequestHandler):
    def get(self):
        pass

class PaymentsHandler(webapp2.RequestHandler):
    """
        Payments from Clients as repayments for loans
    """
    def get(self):
        Guser = users.get_current_user()
        if Guser:

            thisDay = datetime.datetime.now()
            thisDay = thisDay.date()
            thisDay = thisDay.day

            if (thisDay >= 16) and (thisDay < 22):
                findRequest = AdvancedAmount.query(AdvancedAmount.strInstallmentsPaid == False,AdvancedAmount.strPaymentDate == 15)
                UpcomingList = findRequest.fetch()
            elif (thisDay >= 23 ) and (thisDay < 25):
                findRequest = AdvancedAmount.query(AdvancedAmount.strInstallmentsPaid == False,AdvancedAmount.strPaymentDate == 22)
                UpcomingList = findRequest.fetch()
            elif (thisDay >= 26 ) and (thisDay <27):
                findRequest = AdvancedAmount.query(AdvancedAmount.strInstallmentsPaid == False,AdvancedAmount.strPaymentDate == 25)
                UpcomingList = findRequest.fetch()
            elif (thisDay >= 28 ) and (thisDay < 30):
                findRequest = AdvancedAmount.query(AdvancedAmount.strInstallmentsPaid == False,AdvancedAmount.strPaymentDate == 30)
                UpcomingList = findRequest.fetch()
            elif (thisDay >= 30 ) and (thisDay < 3):
                findRequest = AdvancedAmount.query(AdvancedAmount.strInstallmentsPaid == False,AdvancedAmount.strPaymentDate == 30)
                UpcomingList = findRequest.fetch()
            elif (thisDay >= 2 ) and (thisDay < 5):
                findRequest = AdvancedAmount.query(AdvancedAmount.strInstallmentsPaid == False,AdvancedAmount.strPaymentDate == 1)
                UpcomingList = findRequest.fetch()
            else:
                UpcomingList = []


            findRequest = AdvancedAmount.query(AdvancedAmount.strOutStanding == True)
            OutStandingList = findRequest.fetch()


            findRequest = AdvancedAmount.query(AdvancedAmount.strAccountChange == True)
            AccountChangeList = findRequest.fetch()


            findRequest = AdvancedAmount.query(AdvancedAmount.strInstallmentsPaid == True)
            CompleteList = findRequest.fetch()

            findRequest = CompanyRepaymentAccount.query()
            CompanyRepayAccList = findRequest.fetch()

            if len(CompanyRepayAccList) > 0:
                CompanyRepayAcc = CompanyRepayAccList[0]
            else:
                CompanyRepayAcc = CompanyRepaymentAccount()


            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            thisEmployeeList = findRequest.fetch()

            if len(thisEmployeeList) > 0:
                thisEmployee = thisEmployeeList[0]
            else:
                thisEmployee = EmploymentDetails()


            findRequest = UserRights.query(UserRights.strEmployeeCode == thisEmployee.strEmployeeCode)
            thisUserRightsList = findRequest.fetch()

            if len(thisUserRightsList) > 0:
                thisUserRights = thisUserRightsList[0]
            else:
                thisUserRights = UserRights()

            if thisUserRights.bolIsEmployee:
                template = template_env.get_template('templates/dynamic/payments/payments.html')
                context = {'UpcomingList':UpcomingList,'OutStandingList':OutStandingList,'AccountChangeList':AccountChangeList,
                           'CompleteList':CompleteList,'CompanyRepayAcc':CompanyRepayAcc}
                self.response.write(template.render(context))
            else:
                template = template_env.get_template('templates/500.html')
                context = {}
                self.response.write(template.render(context))

class PaymentsProcessingHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            EmployeeList = findRequest.fetch()

            if len(EmployeeList) > 0:
                Employee = EmployeeList[0]
            else:
                Employee = EmploymentDetails()

            findRequest = UserRights.query(UserRights.strReference == Guser.user_id())
            RightsList = findRequest.fetch()
            if len(RightsList) > 0:
                Rights = RightsList[0]
            else:
                Rights = UserRights()


            findRequest = ActiveLoan.query(ActiveLoan.strReference == Guser.user_id())
            ActiveList = findRequest.fetch()
            if len(ActiveList) > 0:
                Active = ActiveList[0]
            else:
                Active = ActiveLoan()


            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == Active.strAccountNumber)
            LoanApplicantList = findRequest.fetch()

            if len(LoanApplicantList) > 0:
                LoanApplicant = LoanApplicantList[0]
            else:
                LoanApplicant = LoanApplicantDetails()

            findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == Active.strAccountNumber)
            AdvanceList = findRequest.fetch()

            if len(AdvanceList) > 0:
                Advance = AdvanceList[0]
            else:
                Advance = AdvancedAmount()


            template = template_env.get_template('templates/dynamic/payments/payee.html')
            context = {'Rights':Rights,'LoanApplicant':LoanApplicant,'Advance':Advance}

            self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()

        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            vstrBankName = self.request.get('vstrBankName')
            vstrBankAccountNumber = self.request.get('vstrBankAccountNumber')
            vstrBankAccountHolder = self.request.get('vstrBankAccountHolder')
            vstrAccountType = self.request.get('vstrAccountType')
            vstrBranchCode = self.request.get('vstrBranchCode')
            vstrBranchName = self.request.get('vstrBranchName')
            vstrNotes = self.request.get('vstrNotes')

            findRequest = PayTO.query(PayTO.strAccountNumber == vstrAccountNumber)
            PayAccountList = findRequest.fetch()

            if len(PayAccountList) > 0:
                PayAccount = PayAccountList[0]
            else:
                PayAccount = PayTO()

            PayAccount.writeReference(strinput=Guser.user_id())
            PayAccount.writeAccountNumber(strinput=vstrAccountNumber)
            PayAccount.writeBankName(strinput=vstrBankName)
            PayAccount.writeBankAccountNumber(strinput=vstrBankAccountNumber)
            PayAccount.writeAccountHolder(strinput=vstrBankAccountHolder)
            PayAccount.writeAccountType(strinput=vstrAccountType)
            PayAccount.writeBranchCode(strinput=vstrBranchCode)
            PayAccount.writeBranchName(strinput=vstrBranchName)
            PayAccount.writeNotes(strinput=vstrNotes)
            PayAccount.put()

            self.response.write("Successfully Update Pay To Account")




class PaymentStatusHandler(webapp2.RequestHandler):
    def get(self):
        vstrAccountNumber = self.request.get('vstrAccountNumber')

        findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == vstrAccountNumber)
        AdvanceList =findRequest.fetch()
        if len(AdvanceList) > 0:
            Advance = AdvanceList[0]
        else:
            Advance = AdvancedAmount()

        findRequest = PayTO.query(PayTO.strAccountNumber == vstrAccountNumber)
        PayToList = findRequest.fetch()
        if len(PayToList) > 0:
            PayAccount = PayToList[0]
        else:
            PayAccount = PayTO()

        findRequest = LoanBankingDetails.query(LoanBankingDetails.strAccountNumber == vstrAccountNumber)
        LBankingList = findRequest.fetch()

        if len(LBankingList) > 0:
            LoanBanking = LBankingList[0]
        else:
            LoanBanking = LoanBankingDetails()


        template = template_env.get_template('templates/dynamic/payments/status.html')
        context = {'Advance': Advance,'PayAccount':PayAccount,'LoanBanking':LoanBanking}

        self.response.write(template.render(context))

class PayClientHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = ActiveLoan.query(ActiveLoan.strReference == Guser.user_id())
            ActiveList = findRequest.fetch()

            if len(ActiveList) > 0:
                Active = ActiveList[0]
            else:
                Active = ActiveLoan()

            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == Active.strAccountNumber)
            LoanAppList = findRequest.fetch()

            if len(LoanAppList) > 0:
                LoanApplicant = LoanAppList[0]
            else:
                LoanApplicant = LoanApplicantDetails()

            findRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == Active.strAccountNumber)
            AdvancedList = findRequest.fetch()

            if len(AdvancedList) > 0:
                Advanced = AdvancedList[0]
            else:
                Advanced = AdvancedAmount()

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Advanced.strReference)
            EmployList = findRequest.fetch()

            if len(EmployList) > 0:
                Employee = EmployList[0]
            else:
                Employee = EmploymentDetails()

            findRequest = CompanyCoffers.query(CompanyCoffers.strBranchCode == Employee.strBranchCode)
            CompanyCofferList = findRequest.fetch()

            if len(CompanyCofferList) > 0:
                thisCompanyCoffer = CompanyCofferList[0]
            else:
                thisCompanyCoffer = CompanyCoffers()


            template = template_env.get_template('templates/dynamic/payments/PayFromFunds.html')
            context = {'LoanApplicant':LoanApplicant,'Advanced': Advanced,'thisCompanyCoffer':thisCompanyCoffer,'Employee':Employee}
            self.response.write(template.render(context))

    def post(self):
        Guser = users.get_current_user()

        if Guser:
            vstrAccountNumber = self.request.get('vstrAccountNumber')
            vstrPayAmount = self.request.get('vstrPayAmount')

            FindRequest = AdvancedAmount.query(AdvancedAmount.strAccountNumber == vstrAccountNumber)
            AdvanceList = FindRequest.fetch()

            if len(AdvanceList) > 0:
                Advanced = AdvanceList[0]
            else:
                Advanced = AdvancedAmount()

            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            EmployList = findRequest.fetch()

            if len(EmployList) > 0:
                Employ = EmployList[0]
            else:
                Employ = EmploymentDetails()

            findRequest = CompanyCoffers.query(CompanyCoffers.strBranchCode == Employ.strBranchCode)
            CompanyCofferList = findRequest.fetch()

            if len(CompanyCofferList) > 0:
                CompanyCoffer = CompanyCofferList[0]
            else:
                CompanyCoffer = CompanyCoffers()

            CompanyCoffer.writeBranchCode(strinput=Employ.strBranchCode)
            CompanyCoffer.writeReference(strinput=Guser.user_id())
            CompanyCoffer.withdrawCashFromBank(strinput=vstrPayAmount)
            CompanyCoffer.put()

            Advanced.setToPaid()
            Advanced.put()
            self.response.write("An Amount of R " + vstrPayAmount + " was paid from Company Bank Account to Client")

class ProcessAdvancedHandler(webapp2.RequestHandler):
    def get(self):

        findRequest = LoanApplicantDetails.query()
        LoanApplicantList = findRequest.fetch()

        for thisLoanApplicant in LoanApplicantList:
            thisLoanApplicant.put()

        self.response.write("Thank you Justice Advanced Fully Reprocessed")

class RepaymentsUpcomingHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:

            URL = self.request.uri
            URLlist = URL.split("/")
            strAdvancedIndex = URLlist[len(URLlist) - 1]
            strAdvancedIndex = int(strAdvancedIndex)

            findRequest = AdvancedAmount.query(AdvancedAmount.strAdvancedIndex == strAdvancedIndex)
            AdvancedList = findRequest.fetch()

            if len(AdvancedList) > 0:
                Advanced = AdvancedList[0]
            else:
                Advanced = AdvancedAmount()

            findRequest = LoanApplicantDetails.query(LoanApplicantDetails.strAccountNumber == Advanced.strAccountNumber)
            ApplicantList = findRequest.fetch()

            if len(ApplicantList) > 0:
                Applicant = ApplicantList[0]
            else:
                Applicant = LoanApplicantDetails()


            template = template_env.get_template('templates/dynamic/repayments/process.html')
            context = {'Advanced':Advanced,'Applicant': Applicant}
            self.response.write(template.render(context))


class DeleteAdvancedHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAdvancedIndex = self.request.get('vstrAdvancedIndex')
            vstrAdvancedIndex = int(vstrAdvancedIndex)

            findRequest = AdvancedAmount.query(AdvancedAmount.strAdvancedIndex == vstrAdvancedIndex)
            AdvancedList = findRequest.fetch()

            for thisAdvanced in AdvancedList:
                thisAdvanced.key.delete()

            thisActivity = Activity()
            thisActivity.writeReference(strinput=Guser.user_id())
            thisActivity.writeAction(strinput="Payments-Delete Advanced")
            thisLeadLink = "/loans/repayments/" + str(AdvancedAmount.strAdvancedIndex )
            thisActivity.writeActionLink(strinput=thisLeadLink)
            thisActivity.put()

            self.response.write("Advanced Amount Deleted Successfully")


class AccountChangeHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAdvancedIndex = self.request.get('vstrAdvancedIndex')
            vstrAdvancedIndex = int(vstrAdvancedIndex)

            findRequest = AdvancedAmount.query(AdvancedAmount.strAdvancedIndex == vstrAdvancedIndex)
            AdvancedList = findRequest.fetch()

            for thisAdvanced in AdvancedList:
                thisAdvanced.strAccountChange = True
                thisAdvanced.put()
            thisActivity = Activity()
            thisActivity.writeReference(strinput=Guser.user_id())
            thisActivity.writeAction(strinput="Payments-Advanced Account Change")
            thisLeadLink = "/loans/repayments/" + str(AdvancedAmount.strAdvancedIndex )
            thisActivity.writeActionLink(strinput=thisLeadLink)
            thisActivity.put()
            self.response.write("Account Change Set")

class AdvancedPaidHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAdvancedIndex = self.request.get('vstrAdvancedIndex')
            vstrTotalAmountRePaid = self.request.get('vstrTotalAmountRePaid')
            vstrAdvancedIndex = int(vstrAdvancedIndex)
            vstrTotalAmountRePaid = int(vstrTotalAmountRePaid)

            findRequest = AdvancedAmount.query(AdvancedAmount.strAdvancedIndex == vstrAdvancedIndex)
            AdvancedList = findRequest.fetch()

            for thisAdvanced in AdvancedList:
                thisAdvanced.strTotalAmountRePaid = vstrTotalAmountRePaid
                if thisAdvanced.strTotalInstallments == vstrTotalAmountRePaid :
                    thisAdvanced.strInstallmentsPaid = True
                else:
                    pass
                thisAdvanced.put()
            thisActivity = Activity()
            thisActivity.writeReference(strinput=Guser.user_id())
            thisActivity.writeAction(strinput="Payments- Advanced Paid")
            thisPaymentLink = "/loans/repayments/" + str(AdvancedAmount.strAdvancedIndex )
            thisActivity.writeActionLink(strinput=thisPaymentLink)
            thisActivity.put()


            findRequest = EmploymentDetails.query(EmploymentDetails.strReference == Guser.user_id())
            thisEmployeeList = findRequest.fetch()

            if len(thisEmployeeList) > 0:
                thisEmployee = thisEmployeeList[0]
            else:
                thisEmployee = EmploymentDetails()


            vstrBalance = thisAdvanced.strAmountAdvancedToClient - thisAdvanced.strTotalInstallments
            vstrDateOfPayment = thisAdvanced.strPaymentDate



            template = template_env.get_template('templates/dynamic/repayments/receipt.html')
            context = {'vstrReferenceNum': vstrAdvancedIndex , 'vstrAccountNumber': thisAdvanced.strAccountNumber ,
                       'vstrCashier': thisEmployee.strSurname + " " + thisEmployee.strFullNames,
                       'vstrAmountOwed': thisAdvanced.strAmountAdvancedToClient,'vstrAmountPaid': thisAdvanced.strTotalInstallments,
                       'vstrBalance':vstrBalance,'vstrDateOfPayment':vstrDateOfPayment}
            self.response.write(template.render(context))



class NotPaidHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrAdvancedIndex = self.request.get('vstrAdvancedIndex')
            vstrAdvancedIndex = int(vstrAdvancedIndex)

            findRequest = AdvancedAmount.query(AdvancedAmount.strAdvancedIndex == vstrAdvancedIndex)
            AdvancedList = findRequest.fetch()

            for thisAdvanced in AdvancedList:
                thisAdvanced.strOutStanding = True
                thisAdvanced.put()
            thisActivity = Activity()
            thisActivity.writeReference(strinput=Guser.user_id())
            thisActivity.writeAction(strinput="Payments- Advanced Not Paid")
            thisLeadLink = "/loans/repayments/" + str(AdvancedAmount.strAdvancedIndex )
            thisActivity.writeActionLink(strinput=thisLeadLink)
            thisActivity.put()
            self.response.write("Installment marked as not Paid")


class LoadDateHandler(webapp2.RequestHandler):

    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrLoadDate = self.request.get('vstrLoadDate')
            vstrLoadDate = int(vstrLoadDate)


            if not( vstrLoadDate == 0):
                findRequest = AdvancedAmount.query(AdvancedAmount.strPaymentDate == vstrLoadDate,AdvancedAmount.strInstallmentsPaid == False)
                thisAdvanceList = findRequest.fetch()
            else:
                findRequest = AdvancedAmount.query(AdvancedAmount.strInstallmentsPaid == False)
                thisAdvanceList = findRequest.fetch()


            template = template_env.get_template('templates/dynamic/payments/repaylist.html')
            context = {'thisAdvanceList':thisAdvanceList}
            self.response.write(template.render(context))


class SaveRepaymentAccountHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrCompanyName = self.request.get('vstrCompanyName')
            vstrCompanyRegistrationNumber = self.request.get('vstrCompanyRegistrationNumber')
            vstrBankName = self.request.get('vstrBankName')
            vstrBankAccountNumber = self.request.get('vstrBankAccountNumber')
            vstrAccountType = self.request.get('vstrAccountType')
            vstrBranchCode = self.request.get('vstrBranchCode')
            vstrReferenceNumber = self.request.get('vstrReferenceNumber')

            findRequest = CompanyRepaymentAccount.query()
            CompanyRepayList = findRequest.fetch()
            if len(CompanyRepayList) > 0:
                CompanyRepayAccount = CompanyRepayList[0]
            else:
                CompanyRepayAccount = CompanyRepaymentAccount()

            CompanyRepayAccount.writeCompanyName(strinput=vstrCompanyName)
            CompanyRepayAccount.writeCompanyReg(strinput=vstrCompanyRegistrationNumber)
            CompanyRepayAccount.writeBankName(strinput=vstrBankName)
            CompanyRepayAccount.writeBankAccount(strinput=vstrBankAccountNumber)
            CompanyRepayAccount.writeAccountType(strinput=vstrAccountType)
            CompanyRepayAccount.writeBranchCode(strinput=vstrBranchCode)
            CompanyRepayAccount.writeAccountReference(strinput=vstrReferenceNumber)
            CompanyRepayAccount.put()

            self.response.write("Succesfully Saved Loan Repayment Account")

class SetupCollectionHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Loan Collection Service Coming Soon from Blue IT Marketing...")


class LoadCSVHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            self.response.write("Load CSV Handler Running")

app = webapp2.WSGIApplication([
    ('/employees/loans', LoansHandler),
    ('/employees/loan-applications', LoansApplicationsHandler),
    ('/loans/employmentdetails', LoansEmploymentDetailsHandler),
    ('/loans/creditprovider', LoansCreditProviderHandler),
    ('/loans/advancedamount', AdvancedAmountHandler),
    ('/loans/incomeexpenditure', IncomeExpenditureHandler),
    ('/loans/clientbankingdetails', ClientBankingDetailsHandler),
    ('/loans/closeaccountnumber', CloseAccountNumberHandler),
    ('/loans/createfile', CreateFileHandler),
    ('/loans/activate', ActivateLoanHandler),
    ('/loans/activateform', LoansActivateFormHandler),
    ('/employees/loans/print', PrintLoansHandler),
    ('/employees/payments', PaymentsHandler),
    ('/loans/payments', PaymentsProcessingHandler),
    ('/loans/payclient', PayClientHandler),
    ('/loans/paymentstatus', PaymentStatusHandler),
    ('/loans/printsettlement', PrintSettlementHandler),
    ('/loans/printpaidup', PrintPaidUpHandler),
    ('/loans/notes', NotesHandler),
    ('/loans/edit', EditLoanHandler),
    ('/loans/delete', DeleteLoanHandler),
    ('/loans/renew', RenewLoanHandler),
    ('/loans/renew/print',RenewPrintHandler),
    ('/loans/list/.*', LoansListHandler),
    ('/loans/reprint', ReprintLoanHandler),
    ('/loans/processadvanced', ProcessAdvancedHandler),
    ('/loans/repayments/.*', RepaymentsUpcomingHandler),
    ('/loans/deleteadvanced', DeleteAdvancedHandler),
    ('/loans/advanced/paid', AdvancedPaidHandler),
    ('/loans/advanced/notpaid', NotPaidHandler),
    ('/loans/loaddate', LoadDateHandler),
    ('/loans/advanced/accountChange', AccountChangeHandler),
    ('/loans/saveaccountsett', SaveRepaymentAccountHandler),
    ('/loans/setupcollection', SetupCollectionHandler),
    ('/loans/payments/loadcsv', LoadCSVHandler)



], debug=True)
