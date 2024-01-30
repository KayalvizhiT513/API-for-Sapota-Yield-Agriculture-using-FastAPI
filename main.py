from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO

app = FastAPI()

# Variable to store the uploaded CSV content
uploaded_csv_content = None

# Function to read and store the CSV content
async def read_csv(file: UploadFile = File(...)):
    global uploaded_csv_content
    content = await file.read()
    uploaded_csv_content = pd.read_csv(BytesIO(content), encoding='latin1')

# Function to calculate overall gross margin
def calculate_overall_gross_margin():
    if uploaded_csv_content is None:
        raise ValueError("CSV file not uploaded")
    
    # Calculate the cost and revenue columns
    uploaded_csv_content['Cost'] = uploaded_csv_content['Buying price'] * uploaded_csv_content['Quantity sold']
    uploaded_csv_content['Revenue'] = uploaded_csv_content['Selling price'] * uploaded_csv_content['Quantity sold']
    
    # Calculate the overall gross margin
    total_cost = uploaded_csv_content['Cost'].sum()
    total_revenue = uploaded_csv_content['Revenue'].sum()
    overall_gross_margin = (total_revenue - total_cost) / total_revenue * 100
    
    #{overall_gross_margin:.2f}%
    return {"Overall Gross Margin": f'{overall_gross_margin:.2f}%'}

# Function to find the most profitable vendor
def find_most_profitable_vendor():
    if uploaded_csv_content is None:
        raise ValueError("CSV file not uploaded")

    # Calculate profit
    uploaded_csv_content['Profit'] = (
        uploaded_csv_content['Selling price'] - uploaded_csv_content['Buying price']
    ) * uploaded_csv_content['Quantity sold']

    profit_by_vendor = (
        uploaded_csv_content.groupby('Firm bought from')['Profit'].sum()
    )
    most_profitable_vendor = profit_by_vendor.idxmax()

    return {"Most Profitable Vendor": most_profitable_vendor}

# Function to find the least profitable customer
def find_least_profitable_customer():
    if uploaded_csv_content is None:
        raise ValueError("CSV file not uploaded")

    # Calculate profit
    uploaded_csv_content['Profit'] = (
        uploaded_csv_content['Selling price'] - uploaded_csv_content['Buying price']
    ) * uploaded_csv_content['Quantity sold']

    profit_by_customer = (
        uploaded_csv_content.groupby('Customer')['Profit'].sum()
    )
    least_profitable_customer = profit_by_customer.idxmin()

    return {"Least Profitable Customer": least_profitable_customer}

# Function to find the most profitable day of the week
def find_most_profitable_day():
    if uploaded_csv_content is None:
        raise ValueError("CSV file not uploaded")

    # Calculate profit
    uploaded_csv_content['Profit'] = (
        uploaded_csv_content['Selling price'] - uploaded_csv_content['Buying price']
    ) * uploaded_csv_content['Quantity sold']

    uploaded_csv_content['Date'] = pd.to_datetime(uploaded_csv_content['Date'])
    uploaded_csv_content['Day of Week'] = uploaded_csv_content['Date'].dt.day_name()

    profit_by_day = uploaded_csv_content.groupby('Day of Week')['Profit'].sum()
    most_profitable_day = profit_by_day.idxmax()

    return {"Most Profitable Day": most_profitable_day}

# API endpoints
@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    await read_csv(file)
    return JSONResponse(content={"message": "CSV file uploaded successfully"})

@app.get("/overall_gross_margin")
def get_overall_gross_margin():
    return calculate_overall_gross_margin()

@app.get("/most_profitable_vendor")
def get_most_profitable_vendor():
    return find_most_profitable_vendor()

@app.get("/least_profitable_customer")
def get_least_profitable_customer():
    return find_least_profitable_customer()

@app.get("/most_profitable_day")
def get_most_profitable_day():
    return find_most_profitable_day()
