import pytest
import json
from api import create_app
from api.models.business_entity_address import BusinessEntityAddress
from api.models.person import Person
from api.models.address import Address
from api.lib.db import drop_records, get_db, close_db, test_conn, test_cursor, save, save_address
from api.lib.orm import find
from settings import TEST_DB_NAME


@pytest.fixture(scope = 'module')
def app():
    flask_app = create_app(TEST_DB_NAME)

    with flask_app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        drop_records(cursor, conn, 'person.person')
        drop_records(cursor, conn, 'person.address')
        drop_records(cursor, conn, 'person.businessentityaddress')
        build_records(conn, cursor)

        conn.commit()
        close_db()
    yield flask_app

    with flask_app.app_context():
        close_db()
        conn = get_db()
        cursor = conn.cursor()
        drop_records(cursor, conn, 'person.person')
        close_db()

def build_records(conn, cursor):
    for i in range(1, 12):
        sam = Person(firstname =f'Sam {i}', lastname = 'ok', businessentityid = i, persontype = 'EM')
        save(sam, conn, cursor)
    bob = Person(firstname =f'Bob', lastname = 'not ok', businessentityid = 15, persontype = 'EM')
    save(bob, conn, cursor)
    address = Address(addressid = 1,addressline1 = '123 romeo',
                    addressline2 = 'earth', city= 'nyc', stateprovinceid = 12, postalcode = 11231,
            spatiallocation = 'ok')
    save_address(address, conn, cursor)
    bea1 = BusinessEntityAddress(addressid = address.addressid, 
                                 businessentityid = bob.businessentityid, addresstypeid = 2 )
    save(bea1, conn, cursor)
    address_2 = Address(addressid = 2,addressline1 = '456 juliett',
                    addressline2 = 'earth', city= 'nyc east', stateprovinceid = 12, 
                    postalcode = 11231, spatiallocation = 'ok')
    save_address(address_2, conn, cursor)
    bea2 = BusinessEntityAddress(addressid = address_2.addressid, addresstypeid = 1,
                                 businessentityid = bob.businessentityid)
    save(bea2, conn, cursor)
    

@pytest.fixture()
def build_people():
    
    drop_records(test_cursor, test_conn, 'person.person')
    build_records(test_conn, test_cursor)

    yield

    drop_records(test_cursor, test_conn, 'person.person')

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_root_url(app, client):
    response = client.get('/')
    assert b'welcome to the adventureworks app' in response.data

def test_persons_url_returns_first_ten_people(app, client):
    response = client.get('/persons')
    dicts = json.loads(response.data)
    assert len(dicts) == 10

def test_persons_last_name_returns_all_of_matching_last_name(app, client):
    response = client.get('/persons/lastname/ok')
    person_response = json.loads(response.data)
    assert len(person_response) == 11

def test_addresses_returns_all_of_the_addresses(app, client):
    response = client.get('/addresses')
    addresses = json.loads(response.data)
    first_address = addresses[0]
    assert first_address['addressline1'] == '123 romeo'
    assert len(addresses) == 2


def test_person_with_address_returns_address_info_along_with_person(app, client):
    bob = find(test_cursor, Person, 15)
    response = client.get(f'/person/addresses/{bob.businessentityid}') #display the address for Person.id
    person_with_addresses = json.loads(response.data)
    #breakpoint()
    assert person_with_addresses['businessentityid'] ==  15
    assert len(person_with_addresses['addresses']) ==  2
    assert person_with_addresses['addresses'][0]['addressline1'] == '123 romeo'
    