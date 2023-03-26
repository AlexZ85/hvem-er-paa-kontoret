from flask import Flask, render_template, request, jsonify
from datetime import date, timedelta
import datetime
import routes as routes
import database as db
import locale
from sqlalchemy import create_engine, text

app = Flask(__name__)

db_connection_string = "mysql+pymysql://79kexqsirs64sn6p9efl:pscale_pw_sR4nRGuRIw8SBA1TpCOkIxYgxYnoJNf89zaF2eQuqSw@aws.connect.psdb.cloud/paakontoret"
engine = create_engine(db_connection_string, connect_args={
    "ssl": {
        "ssl_ca": "/etc/ssl/cert.pem"
    }

})


def list_weekday_dates():
    # Get the current date
    current_date = datetime.date.today()

    # Define a dictionary to store the weekday dates
    weekday_dates = {}

    # Iterate over the next 4 days
    for i in range(1, 7):
        # Add the current day to the date offset by i days
        date = current_date + datetime.timedelta(days=i)

        # Check if the date is a weekday (not a Saturday or Sunday)
        if date.weekday() < 5:
            # Add the weekday date to the dictionary with day as key and date as value
            weekday_dates.update({date.strftime("%A"): date.strftime("%d-%m-%Y")})

    # Print the dictionary of weekday dates
    return weekday_dates





@app.route("/")
def load_booked_plasser(dato=date.today()):
    return render_template('home.html', plasser=db.load_plasser_from_db(dato), ukedager=list_weekday_dates())


@app.route('/show_booked', methods=['POST'])
def vis_booked():
    dato = request.json['dato']
    with engine.connect() as conn:
        result = conn.execute(text(
            f"SELECT bp.plass_id,bp.bruker_id,bp.booket_dato FROM paakontoret.booked_plasser bp  Where bp.booket_dato = '{dato}';"))

        data_list = []
        for row in result.all():
            data_dict = dict(zip(result.keys(), row))
            data_list.append(data_dict)

        plasser = data_list
        print(plasser)
        return plasser


@app.route('/book', methods=['POST'])
def book():
    print("hei")
    data = request.get_json()

    # Extract the values from the JSON object
    bruker_navn = data['cookie_result']
    plass_id = data['clicked_area_id']
    booket_dato = data['booke_dato']
    print(bruker_navn, plass_id, booket_dato)

    with engine.connect() as conn:
        result = conn.execute(text(
            f"INSERT INTO paakontoret.booked_plasser(plass_id, bruker_id, booket_dato) VALUES ({plass_id}, '{bruker_navn}', '{booket_dato}')"
        ))
        print(f"{result.rowcount} rows inserted")

    # Return a JSON response
    return jsonify({'message': 'Data processed successfully'})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
