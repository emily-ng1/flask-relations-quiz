import psycopg2
from settings import DB_NAME
conn = psycopg2.connect(dbname = DB_NAME)
cursor = conn.cursor()

from api.models.person import Person
from api.lib.orm import build_from_record


statement=f"SELECT * FROM person.person WHERE firstname='Ken' AND lastname='Sánchez';"
cursor.execute(statement)
person_record=cursor.fetchone()
print(person_record)
person_obj=build_from_record(Person, person_record)
print(build_from_record.__dict__)