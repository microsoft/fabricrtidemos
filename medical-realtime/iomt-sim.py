import os
import random
import time
import json
import logging
from datetime import datetime
from azure.eventhub import EventHubProducerClient, EventData
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.functions as func

print("Starting the IoMT Synthetic Device Simulator...")
# Read environment variables -- change the default values as needed if not deploying to Azure Functions

key_vault_name = os.getenv("KEY_VAULT_NAME", "akv-rjb-wu3")
secret_name = os.getenv("SECRET_NAME", "eventHubConn")
event_hub_name = os.getenv("EVENT_HUB_NAME", "meddevice")
message_limit = int(os.getenv("MESSAGE_LIMIT", 3)) 

# Azure Key Vault details
key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"

# Authenticate to Azure Key Vault
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

# Retrieve the Event Hub connection string from Azure Key Vault
connection_str = secret_client.get_secret(secret_name).value

# Create a producer client to send messages to the event hub
producer = EventHubProducerClient.from_connection_string(
    conn_str=connection_str,
    eventhub_name=event_hub_name
)

# List of predefined DeviceIds
device_ids = [f"Device-{i}" for i in range(1, 7)]

# Dictionary to keep track of the number of messages sent by each device
device_message_count = {device_id: 0 for device_id in device_ids}

def generate_synthetic_data():
    # Select a random DeviceId from the list
    device_id = random.choice(device_ids)
    
    # Check if the device has reached the message limit
    if device_message_count[device_id] >= message_limit:
        return None
    
    # Generate synthetic heart rate data (in beats per minute)
    heart_rate = random.randint(60, 100)
    
    # Generate synthetic blood pressure data (systolic and diastolic in mmHg)
    systolic_bp = random.randint(90, 140)
    diastolic_bp = random.randint(60, 90)
    
    # Generate synthetic body temperature data (in degrees Farenheit)
    temperature = round(random.uniform(90, 106.1), 1)
    
    # Create a dictionary to hold the synthetic data
    data = {
        "DeviceId": device_id,
        "HeartRate": heart_rate,
        "BloodPressure": {
            "Systolic": systolic_bp,
            "Diastolic": diastolic_bp
        },
        "Temperature": temperature,
        "MeasurementDate": datetime.utcnow().isoformat()
    }
    
    # Increment the message count for the device
    device_message_count[device_id] += 1
    
    return data

def main():
    while True:
        # Generate synthetic data
        data = generate_synthetic_data()
        
        # If data is None, it means the message limit has been reached for the device
        if data is None:
            if all(count >= message_limit for count in device_message_count.values()):
                print("All devices have reached the message limit.")
                break
            continue
        
        # Convert the data to JSON format
        data_json = json.dumps(data)
        
        # Create an EventData object
        event_data = EventData(data_json)
        
        try:
            # Send the event data to the Event Hub
            with producer:
                event_batch = producer.create_batch()
                event_batch.add(event_data)
                producer.send_batch(event_batch)
            print(f"Sent data: {data_json}")
        except AzureError as e:
            print(f"Failed to send data: {e.message}")
        
        # Wait for 1 second before generating the next set of data
        

if __name__ == "__main__":
    main()