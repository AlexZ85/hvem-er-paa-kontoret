from flask import Flask, render_template
from datetime import datetime, timedelta
from database import engine,text
import calendar


app = Flask(__name__)
ukedager = []
today = datetime.today()
two_weeks = timedelta(weeks=0)
future_date = today + two_weeks
for i in range(7):
    future_date += timedelta(days=1)
    while future_date.weekday() >= 5: # Skip weekends (Saturday and Sunday)
        future_date += timedelta(days=1)
    # Print the day and date of the weekday
    ukedager.append(future_date.strftime('%A, %B %d'))



def load_plasser_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from plasser"))
        plasser = []

        for row in result.all():
            plass = dict(zip(result.keys(), row))
            plasser.append(plass)
            print(row)
        return plasser


@app.route("/")
def hello_world():
    plasser = load_plasser_from_db()
    return render_template('home.html', plasser=plasser, ukedager=ukedager)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
