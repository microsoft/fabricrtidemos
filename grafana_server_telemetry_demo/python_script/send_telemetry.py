import random
import string
from datetime import datetime
import time
import json
from azure.eventhub import EventHubProducerClient, EventData
 

CONNECTION_STR = "Endpoint=sb://.."
EVENT_HUB_NAME = "event_hub_name"

def generate_server_data1():
    data = {
        'datacenter_id': 1,
        'server_name': "Server 101",
        'cpu_usage': random.uniform(50, 60),  # Assuming percentage
        'memory_usage': random.uniform(75, 95),  # Assuming percentage
        'disk_usage': random.uniform(20, 25),  # Assuming percentage
        'network_in': random.uniform(20, 30),  # 
        'network_out': random.uniform(30, 40),  # 
        'power_usage': random.uniform(80, 100),  #
        'timestamp': datetime.now().isoformat()
    }
    return data

def generate_server_data2():
    data = {
        'datacenter_id': 2,
        'server_name': "Server 102",
        'cpu_usage': random.uniform(20, 40),  # Assuming percentage
        'memory_usage': random.uniform(40, 70),  # Assuming percentage
        'disk_usage': random.uniform(40, 50),  # Assuming percentage
        'network_in': random.uniform(50, 70),  # 
        'network_out': random.uniform(50, 70),  # A
        'power_usage': random.uniform(50, 100),  # 
        'timestamp': datetime.now().isoformat()
    }
    return data

def generate_server_data3():
    data = {
        'datacenter_id': 3,
        'server_name': "Server 103",
        'cpu_usage': random.uniform(35, 55),  # Assuming percentage
        'memory_usage': random.uniform(65, 80),  # Assuming percentage
        'disk_usage': random.uniform(80, 65),  # Assuming percentage
        'network_in': random.uniform(70, 90),  # 
        'network_out': random.uniform(40, 50),  # 
        'power_usage': random.uniform(50, 60),  # 
        'timestamp': datetime.now().isoformat()
    }
    return data
 
def send_data_to_event_hub(producer, data):
    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData(json.dumps(data)))
    producer.send_batch(event_data_batch)
 
def main():

    producer = EventHubProducerClient.from_connection_string(conn_str=CONNECTION_STR, eventhub_name=EVENT_HUB_NAME)
   
    # Generate a list of 100 random server names
    #servers = [{'server_name': ''.join(random.choices(string.ascii_letters + string.digits, k=20)), 'datacenter_id': random.randint(1, 5)} for _ in range(100)]
   
    
    print("Trying the try statement")
    try:
        while True:
            data1 = generate_server_data1()
            data2 = generate_server_data2()
            data3 = generate_server_data3()
            send_data_to_event_hub(producer, data1)
            send_data_to_event_hub(producer, data2)
            send_data_to_event_hub(producer, data3)
            print(f"Sent data1: {data1}")
            print(f"Sent data2: {data2}")
            print(f"Sent data3: {data3}")
            time.sleep(5)  # Wait for 5 seconds before sending the next batch of data
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        producer.close()    
 
if __name__ == "__main__":
    main()
 