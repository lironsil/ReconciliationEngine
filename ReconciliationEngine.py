import requests
import json
from Payment import Payment
from Payable import Payable
from dateutil import parser
from datetime import timedelta


def load_query():
   file = open("query.txt", "r")
   query=file.read() 
   return str(query)

def run_query(query):
    request = requests.post( 'https://web-backend-dev.zeitgold.com/graphql', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def check_fitting(payment,payable,splits):
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

def handel_result(result,payments):
    transactions= result["data"]["transactions"]["edges"]
    for payment in payments["payments"]:
        print("recommended transactions for this payment: ")
        sub_payments=[]
        ids=payment["payment_reference"].split(' ') #in case the payment was splitted
        for id in ids:
            current_payment=Payment(payment["amount"],id,payment["payment_date"])
            for transaction in transactions:
                transactionId=transaction["node"]["id"]
                payables= transaction["node"]["payables"]["edges"]
                for payable in payables:
                    curr_payable=Payable(payable["node"]["id"],payable["node"]["referenceId"], payable["node"]["amount"], payable["node"]["dateOccurred"])
                    if check_fitting(current_payment,curr_payable,len(ids)):
                        print(transactionId)
                        break

if __name__ == "__main__":
    query=load_query()
    result = run_query(query) 
    payments = json.load(open('payments.json'))
    handel_result(result,payments)
   
        




