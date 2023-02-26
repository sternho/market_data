import math
import re
from datetime import datetime

from flask import Flask, request

from finanical_data_repo import FinancialDataRepo

app = Flask(__name__)
date_format = '%Y-%m-%d'


@app.route('/')
def home():
    return 'Market Data!'


@app.route('/api/statistics')
def statistics():
    error = ''
    start_date = request.args.get('start_date')
    if start_date is not None:
        if is_date_format(start_date):
            start_date = datetime.strptime(start_date, date_format)
        else:
            error = "start date format should yyyy-MM-dd"
    end_date = request.args.get('end_date')
    if end_date is not None:
        if is_date_format(end_date):
            end_date = datetime.strptime(end_date, date_format)
        else:
            error = "end date format should yyyy-MM-dd"

    symbol = request.args.get('symbol')
    page = request.args.get('page', type=int)
    page = page if page is not None else 1
    limit = request.args.get('limit', type=int)
    limit = limit if limit is not None else 3

    data = []
    if not error:
        data = FinancialDataRepo.get_instance().select(symbol, start_date, end_date)
        response_payload = ['symbol', 'date', 'open', 'close', 'volume']
        data = [{key: values[key] for key in response_payload} for values in data]
        error = 'Record not found' if not data else ''

    return {
        'data': data[(page - 1) * limit:page * limit],
        'pagination': {
            'count': len(data),
            'page': page,
            'limit': limit,
            'pages': math.ceil(len(data) / limit),
        },
        'info': {'error': error}
    }


def is_date_format(date: str) -> bool:
    return date is not None and re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', date)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
