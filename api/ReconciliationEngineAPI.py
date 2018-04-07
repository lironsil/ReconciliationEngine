import flask
from ReconciliationEngine import ReconciliationEngine 
import json
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Transactions API</h1><p>The service returns the possible related business transaction IDs</p>"

@app.route('/', methods = ['POST'])
def link():
	RecEngine=ReconciliationEngine()
	print (request.is_json)
	payments = request.get_json()
	query=RecEngine.load_query()
	result =RecEngine.run_query(query)
	transactions=RecEngine.handle_result(result,payments)
	ans={}
	for i,t in enumerate(transactions):
		ans.update({"transaction number " + str(i+1):t})
	return flask.jsonify(ans)
	
app.run()