from flask import Flask, render_template
from datetime import datetime, timedelta
import routes as routes
import database as db
import locale



app = Flask(__name__)

locale.setlocale(locale.LC_TIME, 'nb_NO')
ukedager = []
today = datetime.today()
two_weeks = timedelta(weeks=0)
future_date = today + two_weeks
for i in range(7):
    future_date += timedelta(days=1)
    while future_date.weekday() >= 5: # Skip weekends (Saturday and Sunday)
        future_date += timedelta(days=1)
    # Print the day and date of the weekday
    ukedager.append(future_date.strftime('%A, %B %d').capitalize())





@app.route("/")
def hello_world():
    plasser = db.load_plasser_from_db()
    return render_template('home.html', plasser=plasser, ukedager=ukedager)

@app.route('/my_function', methods=['POST'])
def test():
    msg = "Alex er kul"
    return msg


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
