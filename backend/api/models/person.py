from api.lib.orm import build_from_record, build_from_records
from api.lib.db import save
import api.models as models

class Person:
    __table__ = 'person.person'
    columns = ['businessentityid', 'persontype', 'namestyle', 'title', 'firstname',
      'middlename', 'lastname', 'suffix', 'emailpromotion', 
      'additionalcontactinfo', 'demographics', 'rowguid', 'modifieddata']
    
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        self.__dict__ = kwargs

    def find_or_create_by_first_last_name_and_id(self, firstname, lastname, businessentityid, conn):
        cursor=conn.cursor()
        statement=f"SELECT * FROM {self.__table__} WHERE firstname=%s AND lastname=%s AND businessentityid=%s;"
        cursor.execute(statement, (firstname, lastname, businessentityid))
        person_record=cursor.fetchone()
        person_obj=build_from_record(Person, person_record)

        if person_record and person_record!=None:
            #breakpoint()
            return person_obj
        else:
            new_person_obj=Person(firstname=firstname, lastname=lastname, businessentityid=businessentityid)
            save(new_person_obj, conn, cursor)
            return new_person_obj


    def addresses(self, conn):
        cursor=conn.cursor()
        statement='''
        SELECT a.*
        FROM person.address a
        INNER JOIN person.businessentityaddress b ON a.addressid=b.addressid
        INNER JOIN person.person c ON b.businessentityid=c.businessentityid
        WHERE c.businessentityid=%s;
        '''
        cursor.execute(statement, (self.businessentityid,))
        address_records=cursor.fetchall()
        address_objs=build_from_records(models.Address, address_records)
        return address_objs
    
    def to_json(self, conn):
        person_dict=self.__dict__

        addresses=self.addresses(conn)
        person_dict["addresses"]=[address.__dict__ for address in addresses]
        return person_dict

        
            
            
        
        