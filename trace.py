import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
import datetime
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))




class TracePricingDetails(ndb.Expando):
    strIDNumberTrace = ndb.IntegerProperty(default="3")
    strAddressTelephoneTrace = ndb.IntegerProperty(default="8")
    strConsumerTrace = ndb.IntegerProperty(default="8")
    strCellToID = ndb.IntegerProperty(default="8")
    strBankAccountVerification = ndb.IntegerProperty(default="12")
    strDriversLicenceVer = ndb.IntegerProperty(default="7")

    def writeIDNumberTrace(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strIDNumberTrace = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeAddressTelTrace(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strAddressTelephoneTrace = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeConsumerTrace(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strConsumerTrace = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeCellToID(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strCellToID = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeBankAccountVer(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strBankAccountVerification = int(strinput)
                return True
            else:
                return False
        except:
            return False


class BuyingPower(ndb.Expando):
    strIDNumberVerifications = ndb.IntegerProperty()
    strAddressTelTrace = ndb.IntegerProperty()
    strConsumerTrace = ndb.IntegerProperty()
    strCellToID = ndb.IntegerProperty()
    strBankAccVer = ndb.IntegerProperty()
    strDriversLicenseVerification = ndb.IntegerProperty()

    def writeIDNumberVer(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strIDNumberVerifications = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeAddTelTrace(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strAddressTelTrace = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeConsumerTrace(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strConsumerTrace = int(strinput)
                return True
            else:
                return False

        except:
            return False
    def writeCellToID(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strCellToID = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeBanAccVer(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strBankAccVer = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writeDriversLicenceVer(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strDriversLicenseVerification = int(strinput)
                return True
            else:
                return False
        except:
            return False




    def UpdatedBuyingPower(self):
        try:
            findRequest = TracePricingDetails.query()
            thisTracePricingList = findRequest.fetch()

            if len(thisTracePricingList) > 0:
                thisTracePricing = thisTracePricingList[0]
            else:
                thisTracePricing =TracePricingDetails()
                thisTracePricing.put()

            findRequest = Trace.query()
            thisTraceList = findRequest.fetch()
            if len(thisTraceList) > 0:
                thisTrace = thisTraceList[0]
            else:
                thisTrace = Trace()
                thisTrace.put()

            findRequest = BuyingPower.query()
            thisBuyingPowerList = findRequest.fetch()

            if len(thisBuyingPowerList) > 0:
                thisBuyingPower = thisBuyingPowerList[0]
            else:
                thisBuyingPower = BuyingPower()
                thisBuyingPower.put()

            thisBuyingPower.strBankAccVer = int(thisTrace.strAvailableBalance / thisTracePricing.strBankAccountVerification)
            thisBuyingPower.strConsumerTrace = int(thisTrace.strAvailableBalance / thisTracePricing.strConsumerTrace)
            thisBuyingPower.strCellToID = int(thisTrace.strAvailableBalance / thisTracePricing.strCellToID)
            thisBuyingPower.strIDNumberVerifications = int(thisTrace.strAvailableBalance / thisTracePricing.strIDNumberTrace)
            thisBuyingPower.strAddressTelTrace = int(thisTrace.strAvailableBalance / thisTracePricing.strAddressTelephoneTrace)
            thisBuyingPower.strDriversLicenseVerification = int(thisTrace.strAvailableBalance / thisTracePricing.strDriversLicenceVer)
            thisBuyingPower.put()
            return True
        except:
            return False




class TraceAccountDetails(ndb.Expando):
    strBankName = ndb.StringProperty(default="FNB")
    strBankAccountHolder = ndb.StringProperty(default="Justice Azwifarwi Ndou")
    strBranchCode = ndb.StringProperty(default="250655")
    strBankAccountNumber = ndb.StringProperty(default="62629494767")

    strPayPalAccountDepositHTML = ndb.StringProperty(default="")

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
    def writeBankAccountHolder(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strBankAccountHolder = strinput
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

class Trace(ndb.Expando):
    strAvailableBalance = ndb.IntegerProperty(default=0)
    strPaymentMethod = ndb.StringProperty(default="EFT") # Direct Deposit


    def writeAvailableBalance(self,strinput):
        try:
            strinput = str(strinput)
            if strinput.isdigit():
                self.strAvailableBalance = int(strinput)
                return True
            else:
                return False
        except:
            return False
    def writePaymentMethod(self,strinput):
        try:
            strinput = str(strinput)
            if not(strinput == None):
                self.strPaymentMethod = strinput
                return True
            else:
                return False

        except:
            return False



class TraceAdminHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            findRequest = Trace.query()
            thisTraceList = findRequest.fetch()
            if len(thisTraceList) > 0:
                thisTrace = thisTraceList[0]
            else:
                thisTrace = Trace()


            findRequest = BuyingPower.query()
            thisBuyingPowerList = findRequest.fetch()
            if len(thisBuyingPowerList) > 0:
                thisBuyingPower = thisBuyingPowerList[0]
            else:
                thisBuyingPower = BuyingPower()

            thisBuyingPower.UpdatedBuyingPower()
            thisBuyingPower.put()



            template = template_env.get_template('templates/dynamic/trace/traceveradmin.html')
            context = {'thisBuyingPower':thisBuyingPower,'thisTrace':thisTrace}
            self.response.write(template.render(context))



class RuntraceHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            vstrSelector = self.request.get('vstrSelector')
            vstrIDNumber = self.request.get('vstrIDNumber')

            if vstrSelector == "1": # Find Addresses
                template = template_env.get_template('templates/dynamic/trace/findAddresses.html')
                context = {}
                self.response.write(template.render(context))

            elif vstrSelector == "2": # Find Addresses
                template = template_env.get_template('templates/dynamic/trace/Verifyidnumber.html')
                context = {}
                self.response.write(template.render(context))

            elif vstrSelector == "3":
                template = template_env.get_template('templates/dynamic/trace/verifyDriverLicence.html')
                context = {}
                self.response.write(template.render(context))
            elif vstrSelector == "4":
                template = template_env.get_template('templates/dynamic/trace/ConsumerTrace.html')
                context = {}
                self.response.write(template.render(context))
            elif vstrSelector == "5":
                template = template_env.get_template('templates/dynamic/trace/CelltoID.html')
                context = {}
                self.response.write(template.render(context))

            elif vstrSelector == "6":
                template = template_env.get_template('templates/dynamic/trace/BankAccountVeri.html')
                context = {}
                self.response.write(template.render(context))



class TraceDepositFundHandler(webapp2.RequestHandler):
    def get(self):
        Guser = users.get_current_user()
        if Guser:
            template = template_env.get_template('templates/dynamic/trace/tracepayoptions.html')
            context = {}
            self.response.write(template.render(context))

app = webapp2.WSGIApplication([
    ('/trace/admin', TraceAdminHandler),
    ('/trace/runtrace', RuntraceHandler),
    ('/admin/trace/depositfunds', TraceDepositFundHandler)

], debug=True)
