import datetime

import pandas as pd
import requests
from pandas import DataFrame

from financial.finanical_data_repo import FinancialDataRepo

api_key = 'SZ9F3VIAWRVF0Z36'
date_format = '%Y-%m-%d'


def get_data(symbol: str, start_date: datetime, end_date: datetime) -> DataFrame:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADA' \
          f'Y&apikey={api_key}' \
          f'&symbol={symbol}' \
          f'&start_date={start_date.strftime(date_format)}' \
          f'&end_date={end_date.strftime(date_format)}' \
          f'&interval=60min'

    data = requests.get(url).json()
    df = pd.DataFrame.from_dict(data['Time Series (60min)']).transpose()
    df = df.rename(columns={
        '1. open': 'open',
        '4. close': 'close',
        '5. volume': 'volume'
    })

    df['symbol'] = symbol
    df['date'] = df.index
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime(date_format)
    df['open'] = df.groupby('date')['open'].transform('first')
    df['close'] = df.groupby('date')['close'].transform('last')
    df['volume'] = df['volume'].astype(int)
    df['volume'] = df.groupby('date')['volume'].transform('sum')

    df = df[['symbol', 'date', 'open', 'close', 'volume']]
    df.drop_duplicates(subset=None, inplace=True)
    return df


if __name__ == '__main__':
    symbols = ['IBM', 'AAPL', 'QQQ']
    for symbol in symbols:
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(weeks=2)

        print(symbol + ' processing: ' + start_date.strftime(date_format) + ' - ' + end_date.strftime(date_format))
        data = get_data(symbol, start_date, end_date).to_dict('records')
        print(data)
        FinancialDataRepo.get_instance().delete(symbol, start_date, end_date)
        FinancialDataRepo.get_instance().insert(data)

    print('insert success')
