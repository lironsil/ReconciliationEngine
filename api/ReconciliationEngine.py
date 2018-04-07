import requests
import json
from Payment import Payment
from Payable import Payable
from dateutil import parser


class ReconciliationEngine():
	def __init__(self):
		pass
	def load_query(self):
	   file = open("query.txt", "r")
	   query=file.read() 
	   return str(query)

	def run_query(self,query):
		request = requests.post( 'https://web-backend-dev.zeitgold.com/graphql', json={'query': query})
		if request.status_code == 200:
			return request.json()
		else:
			raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

	def check_fitting(self,payment,payable,splits):
		#same id,same amount,valid date
		if  payable.referencedId==payment.payment_reference and payable.amount==payment.amount  and  parser.parse(payable.dateOccured) <= parser.parse(payment.payment_date):
			 return True
		#splited payment, same id,valid date
		if  splits>1 and payable.referencedId==payment.payment_reference  and  parser.parse(payable.dateOccured) <= parser.parse(payment.payment_date):
			 return True
		#same id,small amount,valid date
		if  payable.referencedId==payment.payment_reference and payable.amount<payment.amount  and  parser.parse(payable.dateOccured) <= parser.parse(payment.payment_date):
			 return True
		#same amount, valid date, wrong Id
		if  payable.amount==payment.amount  and  parser.parse(payable.dateOccured) <= parser.parse(payment.payment_date):
			return True
		else:
			return False

	def handle_result(self,result,payment):
		res=[]
		transactions= result["data"]["transactions"]["edges"]
		sub_payments=[]
		ids=payment["payment_reference"].split(' ') #In case of split payment
		for id in ids:
			current_payment=Payment(payment["amount"],id,payment["payment_date"])
			for transaction in transactions:
				transactionId=transaction["node"]["id"]
				payables= transaction["node"]["payables"]["edges"]
				for payable in payables:
					curr_payable=Payable(payable["node"]["id"],payable["node"]["referenceId"], payable["node"]["amount"], payable["node"]["dateOccurred"])
					if self.check_fitting(current_payment,curr_payable,len(ids)):
						res.append(transactionId)
						break
		return res

   





