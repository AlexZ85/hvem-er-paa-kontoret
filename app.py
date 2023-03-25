from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, date
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







@app.route("/")


def load_booked_plasser(dato=date.today()):
    #locale.setlocale(locale.LC_TIME, 'nb_NO') støttes ikke av onrender
    ukedager = {}
    today = datetime.today()
    ukedager[today.strftime('%A').capitalize()] = today.strftime('%d-%m-%Y')

    two_weeks = timedelta(weeks=0)
    future_date = today + two_weeks

    for i in range(4):
        while True:
            future_date += timedelta(days=1)
            if future_date.weekday() < 5:  # If weekday
                break  # Exit the loop
        # Add the day and date of the weekday to the dictionary
        ukedager[future_date.strftime('%A').capitalize()] = future_date.strftime('%d-%m-%Y')

    plasser = db.load_plasser_from_db(dato)
    print(plasser)
    return render_template('home.html', plasser=plasser, ukedager=ukedager)

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
