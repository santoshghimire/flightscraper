import uuid
import psycopg2
from datetime import datetime


class RedshiftWrapper(object):
    """Wrapper to insert data to Redshift database."""

    host = "flightsdata.cvcioaodlgvz.us-east-1.redshift.amazonaws.com"
    user = "admin"
    dbname = "flightsdata"
    port = "5439"
    password = ""

    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                "dbname='{0}' user='{1}' "
                "host='{2}' port='{3}' password='{4}'".format(
                    self.dbname, self.user, self.host,
                    self.port, self.password
                )
            )
        except:
            raise
        super(RedshiftWrapper, self).__init__()

    def create_table(self):
        cur = self.conn.cursor()
        query = """
            CREATE TABLE flightinfo(
                uuid VARCHAR (255) PRIMARY KEY NOT NULL,
                airline_name VARCHAR (255),
                origin VARCHAR (255) NOT NULL,
                destination VARCHAR (255) NOT NULL,
                num_adult VARCHAR (255) NOT NULL,
                num_child VARCHAR (255) NOT NULL,
                num_infant VARCHAR (255) NOT NULL,
                flight_number VARCHAR (255),
                fare_class VARCHAR (255),
                departure_date VARCHAR (255) NOT NULL,
                arrival_date VARCHAR (255) NOT NULL,
                price_date VARCHAR (255) NOT NULL,
                crawl_date VARCHAR (255) NOT NULL,
                price Real NOT NULL,
                days_to_flight Integer NOT NULL,
                currency VARCHAR (255)
            );
        """
        cur.execute(query)
        self.conn.commit()
        print('Table creation successful !')
        return True

    def insert_row(self, item):
        cur = self.conn.cursor()
        item['uuid'] = str(uuid.uuid4())
        item['crawl_date'] = datetime.today().strftime("%Y-%m-%d")
        cur.execute(
            """INSERT INTO flightinfo(
                uuid, airline_name, origin, destination, num_adult,
                num_child, num_infant, flight_number, fare_class,
                departure_date, arrival_date, price_date,
                crawl_date, price, days_to_flight, currency)
                VALUES (
                    %(uuid)s, %(airline_name)s, %(origin)s, %(destination)s,
                    %(num_adult)s, %(num_child)s, %(num_infant)s,
                    %(flight_number)s, %(fare_class)s, %(departure_date)s,
                    %(arrival_date)s, %(price_date)s, %(crawl_date)s,
                    %(price)s, %(days_to_flight)s, %(currency)s
                )
            """, item
        )
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    r = RedshiftWrapper()
    # r.create_table()
    item = {
        'airline_name': 'QZ - PT Indonesia AirAsia',
        'arrival_date': '2017-01-09 15:10',
        'days_to_flight': 0,
        'departure_date': '2017-01-09 12:15',
        'destination': 'DPS',
        'flight_number': 'QZ  505',
        'num_adult': '1',
        'num_child': '0',
        'num_infant': '0',
        'origin': 'SIN',
        'price': 129.8,
        'currency': 'SGD',
        'price_date': '2017-01-08',
        'fare_class': ''
    }
    r.insert_row(item)
    r.close()
