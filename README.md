# Market Data

## Design
This application is made by the Python and Mongodb.
As python is typeless programming language,
using mongodb to store the data is less issue/error on type casting
and more similar with the json format in API server.
And also mongodb is a NoSQL database, is good for store such of market data.

## Libraries
All the library is included in the requirements.txt file.
- alpha-vantage
  - the library that required to download the market data
- pymongo
  - This is used to connection the mongodb
- pandas
  - This is used to group the data and change the data format easier
- flask
  - This is the web server for create the API
- requests
  - This is the library to support flask server

## Guideline
### Start API Server
1. start the docker in your local
2. docker-compose up
   - The server will start as port 5000 
3. API:
  - [GET] /
    - Just welcome page
  - [GET] /api/statistics?start_date={start_date}&end_date={end_date}&symbol={symbol}&limit={limit}&page={page}
    - start_date, should be a date value and format as: yyyy-MM-dd
    - end_date, should be a date value and format as: yyyy-MM-dd
    - symbol, the stock code, e.g.: IBM
    - limit, page size, display the number of record per page, default 3
    - page, page number, should be a numeric value, default 1

### Run Job
1. Enter the project root
2. run python get_raw_data.py 

