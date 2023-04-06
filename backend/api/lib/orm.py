
def build_from_record(Class, record):
    if not record: return None
    
    attr = dict(zip(Class.columns, record))
    obj = Class()
    obj.__dict__ = attr
    return obj

def build_from_records(Class, records):
    return [build_from_record(Class, record) for record in records]



def find(cursor, Class, id):
    cursor.execute(f"SELECT * FROM {Class.__table__} WHERE businessentityid=%s;", (id,))
    record=cursor.fetchone()
    obj=build_from_record(Class, record)
    return obj

def find_all(cursor, Class, limit = 10):
    cursor.execute(f"SELECT * FROM {Class.__table__} LIMIT {limit};")
    records=cursor.fetchall()
    objs=build_from_records(Class, records)
    return objs
