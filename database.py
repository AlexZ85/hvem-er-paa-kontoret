from sqlalchemy import create_engine, text
from datetime import datetime as datetime

db_connection_string = "mysql+pymysql://79kexqsirs64sn6p9efl:pscale_pw_sR4nRGuRIw8SBA1TpCOkIxYgxYnoJNf89zaF2eQuqSw@aws.connect.psdb.cloud/paakontoret"

engine = create_engine(db_connection_string, connect_args={
    "ssl": {
        "ssl_ca": "/etc/ssl/cert.pem"
    }

})

today = datetime.today()
today_formated = today.strftime("%d-%m-%Y")
dato = ""
def load_plasser_from_db(dato=dato):
    plasser = {}
    if dato != "":
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT plass_id,bruker_id,bookings_dato FROM paakontoret.bookings"
                                   f" Where bookings_dato = '{dato}';"))

            data_list = []
            for row in result.all():
                data_dict = dict(zip(result.keys(), row))
                data_list.append(data_dict)

            plasser = data_list
            print(plasser)
        return plasser

def book_plass(navn, booket_plass, booket_dato):
    # check if there are any existing bookings with the same plass_id and bookings_dato
    query = text("""
    SELECT count(*) as count
    FROM paakontoret.bookings
    WHERE plass_id = :plass_id AND bookings_dato = :bookings_dato
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"plass_id": booket_plass, "bookings_dato": booket_dato})
        count = result.fetchone()[0]

        if count > 0:
            return {'message': 'Booking already exists'}
        else:
            # insert the new booking
            query = text("""
            INSERT INTO paakontoret.bookings (plass_id, bruker_id, bookings_dato)
            VALUES (:plass_id, :bruker_id, :bookings_dato)
            """)
            result = conn.execute(query, {"plass_id": booket_plass, "bruker_id": navn, "bookings_dato": booket_dato})
            print(f"{result.rowcount} rows inserted")
            return {'message': 'Data processed successfully'}


