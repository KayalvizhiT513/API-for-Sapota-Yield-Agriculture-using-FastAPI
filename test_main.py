# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 14:09:41 2023

@author: Kayalvizhi
"""

import pandas as pd
from fastapi.testclient import TestClient
from main import app, uploaded_csv_content

client = TestClient(app)

def test_upload_csv():
    files = {'file': ('test.csv', open(r'"D:\TK\padi padAI GAI\sales_data_1.csv"', 'rb'), 'text/csv')}
    response = client.post("/upload_csv", files=files)
    assert response.status_code == 200
    assert response.json() == {"message": "CSV file uploaded successfully"}

def test_overall_gross_margin():
    response = client.get("/overall_gross_margin")
    assert response.status_code == 200
    assert response.json() == {"Overall Gross Margin": "24.63%"}  # Replace 0 with the expected value

def test_most_profitable_vendor():
    response = client.get("/most_profitable_vendor")
    assert response.status_code == 200
    assert response.json() == {"Most Profitable Vendor": "Vendor4"}  # Replace None with the expected value

def test_least_profitable_customer():
    response = client.get("/least_profitable_customer")
    assert response.status_code == 200
    assert response.json() == {"Least Profitable Customer": "Customer3"}  # Replace None with the expected value

def test_most_profitable_day():
    response = client.get("/most_profitable_day")
    assert response.status_code == 200
    assert response.json() == {"Most Profitable Day": "Monday"}  # Replace None with the expected value
