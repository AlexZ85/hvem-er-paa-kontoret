from flask import Flask, render_template, request, jsonify


import datetime as dt
from datetime import datetime as datetime
import routes as routes
import database as db
import locale
from sqlalchemy import create_engine, text

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'



db_connection_string = "mysql+pymysql://sdvpe5m9dgho5tsl80b1:pscale_pw_t6s60C3KBfke7tY8ihjipWK6diw5wVQqOtyI7Av2SQA@aws.connect.psdb.cloud/paakontoret"
engine = create_engine(db_connection_string, connect_args={
    "ssl": {
        "ssl_ca": "/etc/ssl/cert.pem"
    }

})


def list_weekday_dates():
    # Get the current date
    current_date = datetime.today()

    # Define a dictionary to store the weekday dates
    weekday_dates = {}

    # Iterate over the next 4 days
    for i in range(1, 7):
        # Add the current day to the date offset by i days
        dato = current_date + dt.timedelta(days=i)

        # Check if the date is a weekday (not a Saturday or Sunday)
        if dato.weekday() < 5:
            # Add the weekday date to the dictionary with day as key and date as value
            weekday_dates.update({dato.strftime("%A"): dato.strftime("%d-%m-%Y")})

    # Print the dictionary of weekday dates
    return weekday_dates


today = datetime.today()
today_formated = today.strftime("%d-%m-%Y")


@app.route("/")
def index():
    return render_template('home.html', oppttate_plasser=db.load_plasser_from_db(), ukedager=list_weekday_dates())

@app.route('/book', methods=['POST'])
def book():
    navn = request.form['navn']
    booket_plass = request.form['plass_id']
    booket_dato = request.form['dato']
    # process the form data as needed
    db.book_plass(navn,booket_plass,booket_dato)
    return db.book_plass(navn,booket_plass,booket_dato)


@app.route('/show_booked', methods=['POST'])
def vis_booked():
    dato = request.json['dato']
    oppttate_plasser=db.load_plasser_from_db(dato)
    return jsonify(oppttate_plasser)



if __name__ == "__main__":
    print(__name__)
    app.run(host='0.0.0.0', debug=True)
