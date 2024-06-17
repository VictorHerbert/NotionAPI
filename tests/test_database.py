import pytest
import os

from notion.client import Client
from notion.database import Database

@pytest.fixture
def database(token):
    DB_ID = '420c12cae2814ff0a947fe834a493dc1'

    client = Client(token)
    database = Database(client, DB_ID, populate=True)

    return database


def test_create_page(database):    
    ...

def test_create_invalid_pagepage(database):
    ...

def test_update(database):
    ...

def test_read(database):
    ...

def test_filter(database):
    db = database.filter(lambda page : True)

def test_aplly(database):
    db = database.filter(lambda page : True)
    
    def update_page(page):
        page.property = ...
        return page
    
    db.apply(update_page)