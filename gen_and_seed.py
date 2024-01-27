import connect
from faker import Faker
from random import randint


def generate_client():
    fake_data = Faker()
    fullname = fake_data.name()
    age = randint(18, 82)
    address = fake_data.address()
    email = fake_data.email()
    return fullname, age, address, email


def fill_mongodb_fake_data(client):
    fullname, age, address, email = generate_client()
    client.fullname = fullname
    client.age = age
    client.address = address
    client.email = email
    client.save()