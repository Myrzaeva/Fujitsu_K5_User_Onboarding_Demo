#!/usr/bin/python
from flask import Flask

adminUser =  'JohnDoe'
adminPassword = 'K5Forever'
contract = 'Potatoes'
region = 'Europe'

app = Flask(__name__)
from app import views

