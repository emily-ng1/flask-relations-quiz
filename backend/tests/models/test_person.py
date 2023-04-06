from api.models.person import Person
from api.lib.db import save, test_cursor, test_conn, drop_records, save_address
import pytest
from api.models.address import Address
from api.models.business_entity_address import BusinessEntityAddress

def build_records(conn, cursor):
    for i in range(1, 3):
        sam = Person(firstname =f'Sam {i}', lastname = 'ok', businessentityid = i, persontype = 'EM')
        save(sam, conn, cursor)

@pytest.fixture()
def build_people():
    
    drop_records(test_cursor, test_conn, 'person.person')
    build_records(test_conn, test_cursor)

    yield

    drop_records(test_cursor, test_conn, 'person.person')

def test_person_accepts_mass_assignment():
    person = Person(persontype = 'EM', namestyle = 'f', 
                    firstname = 'Ken', middlename = 'J', lastname = 'Sanchez')
    assert person.firstname == 'Ken'

def test_person_has_property_of__table__():
    assert Person.__table__ == 'person.person'

def test_person_has_property_of_columns():
    assert Person.columns == ['businessentityid', 'persontype', 'namestyle', 'title', 'firstname',
      'middlename', 'lastname', 'suffix', 'emailpromotion', 
      'additionalcontactinfo', 'demographics', 'rowguid', 'modifieddata']
     
def test_find_or_create_by_first_and_last_name_finds_the_related_person_if_already_in_the_database(build_people):
    #breakpoint()
    person1=Person()
    person=person1.find_or_create_by_first_last_name_and_id(firstname = 'Sam 1', lastname = 'ok', businessentityid = 1, conn = test_conn)
    assert person.firstname == 'Sam 1'
    assert person.businessentityid == 1
    test_cursor.execute('select count(*) from person.person')
    num_records = test_cursor.fetchone()
    assert num_records == (2,)

def test_find_or_create_by_first_and_last_name_creates_a_new_person_when_not_in_db(build_people):
    person1=Person()
    
    person = person1.find_or_create_by_first_last_name_and_id(firstname = 'Sam 10', lastname = 'ok', businessentityid = 3, conn = test_conn)
    #breakpoint()
    assert person.firstname == 'Sam 10'
    assert person.lastname == 'ok'    
    
    test_cursor.execute('select count(*) from person.person')
    num_records = test_cursor.fetchone()
    assert num_records == (3,)


@pytest.fixture()
def person_test():
    drop_records(test_cursor, test_conn, 'person.person')
    drop_records(test_cursor, test_conn, 'person.address')
    drop_records(test_cursor, test_conn, 'person.businessentityaddress')

    person = Person(businessentityid=10, persontype = 'EM', namestyle = 'f', firstname = 'Ken', middlename = 'J', lastname = 'Sanchez')
    saved_person=save(person, test_conn, test_cursor)
    
    address_1=Address(addressid=5, addressline1="1970 Napa Ct.", city="Bothell", stateprovinceid=79, postalcode="98011")
    saved_address_1=save_address(address_1, test_conn, test_cursor)
    address_2=Address(addressid=5, addressline1="1810 Napa Ct.", city="Wothell", stateprovinceid=79, postalcode="98011")
    saved_address_2=save_address(address_2, test_conn, test_cursor)

    bea_1=BusinessEntityAddress(addressid=saved_address_1.addressid, businessentityid=saved_person.businessentityid, addresstypeid=2)
    saved_bea_1=save(bea_1, test_conn, test_cursor)
    bea_2=BusinessEntityAddress(addressid=saved_address_2.addressid, businessentityid=saved_person.businessentityid, addresstypeid=6)
    saved_bea_2=save(bea_2, test_conn, test_cursor)

    yield saved_person
    drop_records(test_cursor, test_conn, 'person.person')
    drop_records(test_cursor, test_conn, 'person.address')
    drop_records(test_cursor, test_conn, 'person.businessentityaddress')

def test_addresses(person_test):
    address_objs=person_test.addresses(test_conn)
    address_dicts=[address_obj.__dict__ for address_obj in address_objs]
    #breakpoint()
    assert set([address["addressline1"] for address in address_dicts])==set(["1970 Napa Ct.", "1810 Napa Ct."])

def test_to_json(person_test):
    person_json=person_test.to_json(test_conn)
    assert set([address["addressline1"] for address in person_json["addresses"]])==set(["1970 Napa Ct.", "1810 Napa Ct."])

