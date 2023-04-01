from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://79kexqsirs64sn6p9efl:pscale_pw_sR4nRGuRIw8SBA1TpCOkIxYgxYnoJNf89zaF2eQuqSw@aws.connect.psdb.cloud/paakontoret"

engine = create_engine(db_connection_string, connect_args={
    "ssl": {
        "ssl_ca": "/etc/ssl/cert.pem"
    }

})


def load_plasser_from_db(dato):
    plasser = {}
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT plass_id,bruker_id,bookings_dato FROM paakontoret.bookingsv2"
                                   f" Where bookings_dato = '{dato}';"))

        data_list = []
        for row in result.all():
            data_dict = dict(zip(result.keys(), row))
            data_list.append(data_dict)

        plasser = data_list
        print(plasser)
        return plasser


def book_plass(navn, booket_plass, booket_dato, kode):
    # check if there are any existing bookings with the same plass_id and bookings_dato
    query = text("""
    SELECT count(*) as count
    FROM paakontoret.bookingsv2
    WHERE plass_id = :plass_id AND bookings_dato = :bookings_dato
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"plass_id": booket_plass, "bookings_dato": booket_dato})
        count = result.fetchone()[0]

        if count > 0:
            feil_popup = {'message': 'Plassen var allerede booket!', 'status': 'danger'}
            return feil_popup
        else:
            # insert the new booking
            query = text("""
            INSERT INTO paakontoret.bookingsv2 (plass_id, bruker_id, bookings_dato, kode)
            VALUES (:plass_id, :bruker_id, :bookings_dato, :kode)
            """)
            result = conn.execute(query, {"plass_id": booket_plass, "bruker_id": navn, "bookings_dato": booket_dato,
                                          "kode": kode})
            print(f"{result.rowcount} rows inserted")
            ok_popup = {'message': 'Plassen er booket!', 'status': 'success'}
            return ok_popup


def unbook_plass(navn, booket_plass, booket_dato, kode):
    # check if there are any existing bookings with the same plass_id, bookings_dato, and kode
    query = text("""
    SELECT count(*) as count
    FROM paakontoret.bookingsv2
    WHERE plass_id = :plass_id AND bookings_dato = :bookings_dato AND kode = :kode
    """)

    delete_query = text("""DELETE FROM paakontoret.bookingsv2 WHERE plass_id = :plass_id AND kode = :kode""")
    with engine.connect() as conn:
        result = conn.execute(query, {"plass_id": booket_plass, "bookings_dato": booket_dato, "kode": kode})
        count = result.fetchone()[0]

        if count == 1:
            result = conn.execute(delete_query, {"plass_id": booket_plass, "kode": kode})
            print(result)
            print(f"{result.rowcount} rows deleted")
            ok_popup = {'message': 'Plassen er slettet!', 'status': 'success'}

            return ok_popup
        else:
            feil_popup = {'message': 'Feil kode eller finner ikke bookingen', 'status': 'danger'}
            return feil_popup

