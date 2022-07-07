from tracemalloc import start
from flask import Flask, render_template, request, jsonify
import pandas as pd
import pandas_datareader as web
from datetime import date
import json

app = Flask("Html trial")

# start_date = date(2018, 1, 1)
# end_date = date(2022, 5, 31)
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
    results = {}
    if request.method == "POST":
        name = request.form.get('name')
        start = request.form.get('start_date')
        y, m, d = start.split('-')
        start_date = date(int(y),int(m), int(d))
        end = request.form.get('end_date')
        y_e, m_e, d_e = end.split('-')
        end_date = date(int(y_e),int(m_e), int(d_e))
        
        interval = request.form.get('interval')
        
        df = get_finance_data(name, start_date, end_date, interval)
    return df.to_html(classes='table table-striped text-center', justify='center')


@app.route('/')
def home():
    #results = my_form_post()
    return render_template('yahoo_fin.html')


if __name__ == '__main__':
    # app.run(debug=True, host='127.0.0.1', port=5000)
    app.run()