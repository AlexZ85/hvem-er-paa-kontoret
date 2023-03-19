from flask import Flask, render_template, request
from datetime import datetime, timedelta
import routes as routes
import database as db
import locale




app = Flask(__name__)

locale.setlocale(locale.LC_TIME, 'nb_NO')
ukedager = {}
today = datetime.today()
two_weeks = timedelta(weeks=0)
future_date = today + two_weeks
for i in range(5):
    while True:
        future_date += timedelta(days=1)
        if future_date.weekday() < 5: # If weekday
            break # Exit the loop
    # Add the day and date of the weekday to the dictionary
    ukedager[future_date.strftime('%A').capitalize()] = future_date.strftime('%d-%m-%Y')








@app.route("/")
def load_booked_plasser():
    plasser = db.load_plasser_from_db()
    print(ukedager)
    return render_template('home.html', plasser=plasser, ukedager=ukedager)

@app.route('/my_function', methods=['POST'])
def test():
    dato = request.json['dato']
    print(dato)
    msg = "Alex er kul"
    return msg


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
