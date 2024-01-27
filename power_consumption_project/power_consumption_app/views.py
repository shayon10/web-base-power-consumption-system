from django.http import HttpResponse
import csv
import plotly.graph_objs as go
from django.shortcuts import render, redirect
from tuya_connector import TuyaOpenAPI
import datetime

# Update the new access credentials and device ID
ACCESS_ID = "4fyf4qv4axmx5hnge5yp"
ACCESS_KEY = "1a73abf1139b472a8f6542952d9686eb"
API_ENDPOINT = "https://openapi.tuyaeu.com"
DEVICE_ID = "bfa4406adb4df9f075xoey"

file_path = 'C:\\power_consumption_project\\cur_power_data.csv'

def get_power_data():
    openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
    openapi.connect()
    try:
        # Update the device ID in the API request
        response = openapi.get(f'/v1.0/iot-03/devices/status?device_ids={DEVICE_ID}')
       

        currentconsumption = response['result'][0]['status'][2]
        currentcurrent = response['result'][0]['status'][3]
        currentpower = response['result'][0]['status'][4]
        currentvoltage = response['result'][0]['status'][5]
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        power = currentpower['value']
        current = currentcurrent['value']
        voltage = currentvoltage['value']
        consumption = currentconsumption['value']

        # Constructing the absolute path to the CSV file
        csv_file_path = 'C:\\power_consumption_project\\cur_power_data.csv'  # Replace with the absolute path

        # New values to add for each column
        new_data = {
            'Current Power': power,
            'Current Voltage': voltage,
            'Current Current': current,
            'Energy Consumption': consumption,
            'TimeStamp': current_time  # current timestamp
        }

        # Open the existing CSV file in append mode
        with open(csv_file_path, 'a', newline='') as csvfile:
            fieldnames = ['Current Power', 'Current Voltage', 'Current Current', 'Energy Consumption', 'TimeStamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # If the file is empty, write the header
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow(new_data)
            print("Successful")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Rest of your code remains unchanged



def current(request):
    #get_power_data()
    x_data = []
    y_data = []
    hover_text = []
    total_power = 0
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            x_data.append(row['TimeStamp'])
            y_data.append(float(row['Current Current']))
            hover_text.append(f"Current: {row['Current Current']}")
            
    for y in y_data:
        total_power += y
    return render(request, 'power.html', {'x_data': x_data, 'y_data': y_data, 'hover_text': hover_text,'total_power':total_power})

def latest_data(request):
    get_power_data()
    return redirect('current')

def voltage(request):
    x_data = []
    y_data = []
    hover_text = []
    total_voltage = 0
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            x_data.append(row['TimeStamp'])
            y_data.append(float(row['Current Voltage']))
            hover_text.append(f"Current: {row['Current Voltage']}")
            
    for y in y_data:
        total_voltage += y
    return render(request, 'voltage.html', {'x_data': x_data, 'y_data': y_data, 'hover_text': hover_text,'total_voltage':total_voltage})

def latest_voltage_data(request):
    get_power_data()
    return redirect('voltage')

def elec_con(request):
    x_data = []
    y_data = []
    hover_text = []
    total_con = 0
    cost = 0
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            x_data.append(row['TimeStamp'])
            y_data.append(float(row['Energy Consumption']))
            hover_text.append(f"Current: {row['Energy Consumption']}")
            
    for y in y_data:
        total_con += y
        cost = (y*6*36)/1000
    return render(request, 'electricity.html', {'x_data': x_data, 'y_data': y_data, 'hover_text': hover_text,'total_con':total_con,'cost':cost})

def latest_electrictiy_data(request):
    get_power_data()
    return redirect('elec_con')