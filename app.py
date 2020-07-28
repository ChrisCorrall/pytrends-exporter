#import jinja
import pandas as pd
from flask import Flask, render_template, request, redirect, send_file, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)


pytrends = TrendReq(hl='en-GB', tz=212)

@app.route('/interest-over-time', methods=['GET','POST'])
def process_keywords():
    if request.method == 'POST':
        input = request.form

        keyword_list = input["keywords"].split(",")
        name_of_file = keyword_list[0] + keyword_list[-1] + ".csv"

        payload_df = pytrend_payload(keyword_list, name_of_file)
        return send_file(name_of_file, attachment_filename = name_of_file, as_attachment = True)



    else:
        return render_template("form.html")



def pytrend_payload(keywords, filename):
    if len(keywords)<=100:
        data = []
        for kw in keywords:
            payload = pytrends.build_payload([kw], cat=0, timeframe='today 3-m', geo='GB', gprop='')
            data.append(pytrends.interest_over_time().drop('isPartial', axis=1))

        df = pd.DataFrame(index=data[0].index)
        for i in range(len(data)):
            name = data[i].columns[0]
            values = data[i].values
            df.insert(i, name, values)
        return df.to_csv(filename)

    else:
        return("Too many keywords - the limit is 100. Split your list up and try again.")











app.run(port=5000)