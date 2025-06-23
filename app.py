from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import database as db  # your db.py file with load/book/unbook functions

# --------------------------
# Flask Setup
# --------------------------
app = Flask(__name__)
app.secret_key = '!Alexxx!02'

# --------------------------
# Database Setup
# --------------------------
engine = create_engine("sqlite:///paakontoret.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Booking(Base):
    __tablename__ = 'bookingsv2'
    bookings_id = Column(Integer, primary_key=True, autoincrement=True)
    plass_id = Column(String(45))
    bruker_id = Column(String(45))
    bookings_dato = Column(String(45))  # Optional: use Date type
    kode = Column(String(45))


# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# --------------------------
# Helper Functions
# --------------------------

def list_weekday_dates():
    current_date = datetime.today()
    weekday_dates = {}

    if current_date.weekday() < 5:
        weekday_dates[current_date.strftime("%A")] = current_date.strftime("%d-%m-%Y")

    for i in range(1, 7):
        dato = current_date + timedelta(days=i)
        if dato.weekday() < 5:
            weekday_dates[dato.strftime("%A")] = dato.strftime("%d-%m-%Y")

    return weekday_dates


# --------------------------
# Routes
# --------------------------

@app.route("/")
def load_booked_plasser():
    return render_template('home.html', ukedager=list_weekday_dates())


@app.route('/hent_bookings', methods=['POST'])
def hent_bookings():
    dato = request.form.get('dato')
    booket_plasser = db.load_plasser_from_db(dato)
    return jsonify(booket_plasser)


@app.route('/book', methods=['POST'])
def book():
    navn = request.form.get('Navn')
    plass = request.form.get('Plass')
    dato = request.form.get('Dato')
    kode = request.form.get('Kode')

    popup = db.book_plass(navn, plass, dato, kode)
    flash(popup)
    return redirect(url_for('load_booked_plasser'))


@app.route('/unbook', methods=['POST'])
def unbook():
    navn = request.form.get('Navn')
    plass = request.form.get('Plass')
    dato = request.form.get('Dato')
    kode = request.form.get('Kode')

    popup = db.unbook_plass(navn, plass, dato, kode)
    flash(popup)
    return redirect(url_for('load_booked_plasser'))


# --------------------------
# App Runner
# --------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False, ssl_context=('cert.pem', 'privkey.pem'))
