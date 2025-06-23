from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# --------------------------
# Database setup
# --------------------------

engine = create_engine("sqlite:///paakontoret.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# --------------------------
# ORM Model
# --------------------------

class Booking(Base):
    __tablename__ = 'bookingsv2'

    bookings_id = Column(Integer, primary_key=True, autoincrement=True)
    plass_id = Column(String(45))
    bruker_id = Column(String(45))
    bookings_dato = Column(String(45))  # Could also use Date type
    kode = Column(String(45))

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# --------------------------
# Initial test data (optional)
# --------------------------

def insert_test_data():
    session = Session()
    try:
        session.add_all([
            Booking(plass_id='1', bruker_id='alex', bookings_dato='20-06-2025', kode='abc'),
            Booking(plass_id='2', bruker_id='sofia', bookings_dato='20-06-2025', kode='def')
        ])
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error inserting test data: {e}")
    finally:
        session.close()

# insert_test_data()  # Uncomment to run

# --------------------------
# Logic Functions
# --------------------------

def load_plasser_from_db(dato):
    session = Session()
    try:
        results = session.query(Booking.plass_id, Booking.bruker_id, Booking.bookings_dato)\
                         .filter(Booking.bookings_dato == dato)\
                         .all()

        return [
            {
                "plass_id": r.plass_id,
                "bruker_id": r.bruker_id,
                "bookings_dato": r.bookings_dato
            } for r in results
        ]
    finally:
        session.close()


def book_plass(navn, booket_plass, booket_dato, kode):
    session = Session()
    try:
        existing = session.query(Booking)\
            .filter(Booking.plass_id == booket_plass)\
            .filter(Booking.bookings_dato == booket_dato)\
            .first()

        if existing:
            return {'message': 'Plassen var allerede booket!', 'status': 'danger'}

        new_booking = Booking(
            plass_id=booket_plass,
            bruker_id=navn,
            bookings_dato=booket_dato,
            kode=kode
        )
        session.add(new_booking)
        session.commit()
        return {'message': 'Plassen er booket!', 'status': 'success'}

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error occurred: {e}")
        return {'message': 'En feil oppstod ved booking.', 'status': 'danger'}
    finally:
        session.close()


def unbook_plass(navn, booket_plass, booket_dato, kode):
    session = Session()
    try:
        booking = session.query(Booking)\
            .filter(Booking.plass_id == booket_plass)\
            .filter(Booking.bookings_dato == booket_dato)\
            .filter(Booking.kode == kode)\
            .first()

        if booking:
            session.delete(booking)
            session.commit()
            return {'message': 'Plassen er slettet!', 'status': 'success'}

        return {'message': 'Feil kode eller finner ikke bookingen', 'status': 'danger'}

    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error occurred: {e}")
        return {'message': 'En feil oppstod ved sletting.', 'status': 'danger'}
    finally:
        session.close()
