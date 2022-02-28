# Beans API

A simple CRUD API to manage coffee beans inventory

## Installation and Running

Python3.6 or later required. Prequisite installation handled by pipenv.  Install
pipenv:

	pip install pipenv
	
In the api directory, install pre-requisite libraries from PyPI:

	pipenv install
   
After installed, the server can be started:

	pipenv run uvicorn beans_api:app
	
This will start a webserver listening on localhost:8000.  You can check that by
visiting the docs page http://localhost:8000/docs

## Documentation

After starting the server you have two methods to view the API documentation

http://localhost:8000/docs

Or

http://localhost:8000/redoc

Part of the reason I went with the FastAPI library is that is supports the
OpenAPI Spec 3 out of the box.  All of the docs are automatically generated and
I'd probably want to tweak them in a production use case to make things more
clear.  That also means I can't take any of the credit for how nice the docs
look--that's all the tooling

## Testing

The docs page allows you to make calls against the API but I've also included
some cURL commands here for demonstration.

Create some records in the database:

	curl -X 'POST' \
	  'http://localhost:8000/beans/' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/json' \
	  -d '{
	  "type": "arabica",
	  "region": "colombia",
	  "roast": "light",
	  "quantity": 12,
	  "limited": false
	}'
	
	curl -X 'POST' \
	  'http://localhost:8000/beans/' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/json' \
	  -d '{
	  "type": "robusta",
	  "region": "brazil",
	  "roast": "medium",
	  "quantity": 13,
	  "limited": false
	}'
	
	curl -X 'POST' \
	  'http://localhost:8000/beans/' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/json' \
	  -d '{
	  "type": "excelsa",
	  "region": "kenya",
	  "roast": "dark",
	  "quantity": 10,
	  "limited": true
	}'
	
Take a look at all of the new records:

	curl -X 'GET' \
	  'http://localhost:8000/beans/all' \
	  -H 'accept: application/json'
	
Or a specific record by ID (ID 2 in this case):

	curl -X 'GET' \
	  'http://localhost:8000/beans/2' \
	  -H 'accept: application/json'
	
You can update a record with the PUT HTTP verb:

	curl -X 'PUT' \
	  'http://localhost:8000/beans/1' \
	  -H 'accept: application/json' \
	  -H 'Content-Type: application/json' \
	  -d '{
	  "type": "arabica",
	  "region": "colombia",
	  "roast": "light",
	  "quantity": 4,
	  "limited": true
	}'
	
And you can mark records deleted with the DELETE HTTP verb:

	curl -X 'DELETE' \
	  'http://localhost:8000/beans/1' \
	  -H 'accept: */*'
	  
## Notes

In a production use case I would make several improvements, most of which are
pretty obvious best practices.  I've forgone them here just to make it easier to
demonstrate the stated requirements of the task.

- Persistent data storage in a database (and eliminate the need to generate IDs
  and have janky lookup loops)
- Split models/controllers into separate files/directories
- Require authorization headers and an API key
- More thorough error handling and more detailed error messages
- Deploy versioning on API URIs to maintain consistency with updates (eg.
  /api/v1/beans/ ...)
- Allow batch record POST creation
- Allow PATCH requests to update with partial data, if necessary
- This goes along with the persistent data store, but there's some ambiguity as
  to whether we should allow duplicate type/region/roast records.  I chose to
  allow duplicates because it's unclear.  Ideally something like a lot number
  would serve has natural primary ID and would reduce the need for duplicate
  checking
- Implement an automated testing suite to ensure changes aren't going to break
  things
- Finally, it would be interesting/useful to allow lookups and filtering based
  on other data elements rather than just the DB ID
