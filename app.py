from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import datetime as dt
from datetime import datetime as datetime
import routes as routes
import database as db
import locale
from sqlalchemy import create_engine, text

app = Flask(__name__)



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
def load_booked_plasser(dato=today_formated):

    return render_template('home.html', oppttate_plasser=db.load_plasser_from_db(dato), ukedager=list_weekday_dates() )


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
