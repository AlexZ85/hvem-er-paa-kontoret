from sqlalchemy import create_engine, text
import pymysql

db_connection_string = "mysql+pymysql://79kexqsirs64sn6p9efl:pscale_pw_sR4nRGuRIw8SBA1TpCOkIxYgxYnoJNf89zaF2eQuqSw1@aws.connect.psdb.cloud/paakontoret"

engine = create_engine(db_connection_string, connect_args={
    "ssl": {
        "ssl_ca": "/etc/ssl/cert.pem"
    }

})


def load_plasser_from_db():
    plasser = {}
    with engine.connect() as conn:
        result = conn.execute(text("SELECT bp.plass_id,bp.bruker_id,bp.booket_dato,p.coord FROM paakontoret.booked_plasser bp join paakontoret.plasser p on bp.plass_id = p.plass_id;"))

        data_list = []
        for row in result.all():
            data_dict = dict(zip(result.keys(), row))
            data_list.append(data_dict)

        plasser = data_list
        print(plasser)
        return plasser


