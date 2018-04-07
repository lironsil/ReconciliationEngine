# Reconciliation Engine

The service exposes an API, with payment data as a json input, and the engine returns the possibly related business transactions.

### Prerequisites
```
Python 2.7
Flask
```
### Example of how to run the application
```
python ReconciliationEngineAPI.py
```
### Example of how to test the application
#### Json file with Payment details
```
python test.py
```
### Query Details
the access to the DB goes through the GraphQL,
the BusinessId is in query.txt 
