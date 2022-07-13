from tracemalloc import start
from flask import Flask, render_template, request, jsonify
import pandas as pd
import pandas_datareader as web
from datetime import date
import json

df_yahoo = pd.read_csv('yahoo_tickers.csv')
df_usa = df_yahoo[df_yahoo['Country'] == 'USA']

tickers = list(df_usa['Ticker'])
names = list(df_usa['Name'])
d_ticker = {}
for i in range(len(names)):
    d_ticker[names[i]] = tickers[i]
    
app = Flask("Html trial")


def get_finance_data(name, start_date, end_date, interval):
    df = web.get_data_yahoo(name, start_date, end_date, interval = interval)
    
    y = []
    for i in df.index:
        y.append(str(i).split(' ')[0])

    df_new = pd.DataFrame(columns=['Date', 'Volume', 'Adj Close'])
    df_new['Date'] = y
    df_new['Volume'] = list(df['Volume'])
    df_new['Adj Close'] = list(df['Adj Close'])
    
    return df_new



@app.route('/fin_data', methods=['GET','POST'])
def my_form_post():
    idx_name = ''
    columns = []
    if request.method == "POST":
        name = request.form.get('name')
        start = request.form.get('start_date')
        y, m, d = start.split('-')
        start_date = date(int(y),int(m), int(d))
        end = request.form.get('end_date')
        y_e, m_e, d_e = end.split('-')
        end_date = date(int(y_e),int(m_e), int(d_e))
        data_sources = {'1': 'yahoo', '2': 'fred'}
        # interval = request.form.get('interval')
        src_code = request.form.get('source')
        if src_code == '1':
            # for keys, value in d_ticker.items():
            #     if value == name:
            #         idx_name = keys
            idx_name = name
            columns = ['Volume', 'Adj Close']
            df = web.DataReader(idx_name, data_sources[src_code], start_date, end_date)[columns]

        if src_code == '2':
            idx_name = 'SP500'
            df = web.DataReader(idx_name, data_sources[src_code], start_date, end_date)

        
        #df = get_finance_data(name, start_date, end_date, interval)
    return df.to_html(classes='table table-striped text-center', justify='center')


@app.route('/')
def home():
    return render_template('yahoo_fin.html', data=d_ticker)


if __name__ == '__main__':
    app.run()