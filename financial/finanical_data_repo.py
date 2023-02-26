import datetime
import os

from pymongo import MongoClient

date_format = '%Y-%m-%d'

database_name = 'financial_data'
url = os.getenv('MONGO_URI')


class FinancialDataRepo:
    instance = None

    def __init__(self):
        if not hasattr(self, 'client'):
            self.client = MongoClient(url)
            self.db = self.client[database_name]
            self.collection = self.db['financial_data']

    @classmethod
    def get_instance(cls):
        return cls() if cls.instance is None else cls.instance

    def delete(self, symbol: str, start_date: datetime, end_date: datetime):
        self.collection.delete_many({
            'symbol': symbol,
            'date': {
                '$gte': start_date.strftime(date_format),
                '$lte': end_date.strftime(date_format),
            }
        })

    def insert(self, data):
        self.collection.insert_many(data)

    def select(self, symbol: str, start_date: datetime, end_date: datetime):
        filtering = {}
        if symbol is not None:
            filtering['symbol'] = symbol
        date_filter = {}
        if start_date is not None:
            date_filter['$gte'] = start_date.strftime(date_format)
        if end_date is not None:
            date_filter['$lte'] = end_date.strftime(date_format)
        if date_filter:
            filtering['date'] = date_filter
        return self.collection.find(filtering)
