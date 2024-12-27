Fabric Real-time Grafana Demo

This repo will walk you through creating a Fabric Eventstream and Eventhouse and then streaming synthetic server telemetry data to it. We will then create an Azure Managed Grafana dashboard to visualize the data. This demo assumes you have a regular or trial Fabric or Power BI Premium instance you can use. Create the Grafana and Event Hubs items below in the same region as your Power BI Premium or Fabric instance if possible. 

To start, open an Azure portal to create an Azure Managed Grafana instance. Type in Grafana and then select the 'Azure Managed Grafana' service:

![image](https://github.com/user-attachments/assets/c875c8f7-fc40-4e88-aae1-e9937885d829)

Now select 'Create' to create a new instance:

![image](https://github.com/user-attachments/assets/00a2fd07-3971-46aa-960e-6c30dac23b3b)

Use the image below to fill in the required details for the demo environment. Name your Grafana instance any name you like. Once the fields below are filled in, select to 'Review and Create', then select 'Create':

![image](https://github.com/user-attachments/assets/a383df38-85d4-4d47-b43b-a3695b4fa9ea)
![image](https://github.com/user-attachments/assets/8be166a3-43a3-42ac-84d7-2bef5dcd5cfd)

Once the Managed Grafana instance is created, search for 'Event Hubs' at the top of the Azure portal in the search bar:

![image](https://github.com/user-attachments/assets/abc4acd5-6fec-4186-9d76-a3c59dcb4e90)

Now select 'Create' to create an Azure Event Hub namespace:

![image](https://github.com/user-attachments/assets/ff79ced3-1000-410e-84e9-c6f3ac6edc55)

Fill in the details below. Create any name and location you would like, but use the same location as the Grafana and Fabric instances. Once done, select to 'Review and Create' and then 'Create' the Event Hub namespace:

![image](https://github.com/user-attachments/assets/85ff1644-378a-4c10-a7fd-b2eeedc03311)

Once the event hub namespace is created, create an event hub in it:

![image](https://github.com/user-attachments/assets/9c271028-8f21-44c9-8f3d-c850c5762820)

![image](https://github.com/user-attachments/assets/f3a4dfce-5587-4173-898a-4c02bf977836)

Take the defaults for everything else and hit ‘Review and Create’ to create the event hub.

Onece the event hub has been created, create a SAS policy we can use to connect to it and stream data in as shown below. First select 'Add' to add a new policy, then give it a name and check the 'Send' and 'Listen' check boxes and then hit 'Create'. Make sure you are creating the policy for the Event hub and not the Event hub namespace it belongs to:

![image](https://github.com/user-attachments/assets/738c57ad-f04c-4753-8c57-45240e61e714)

Now back in Fabric, create a new Eventhouse to store the telemetry data that will be streamed in:

![image](https://github.com/user-attachments/assets/b6e8fcd2-7a89-44e2-92a8-f1a1790cadeb)

Name the Eventhouse 'Server Telemetry' as shown below:

![image](https://github.com/user-attachments/assets/0a2a4f69-7648-44b6-8b7e-04bb185acebe)

Next open the Server Telemetry Eventhouse and select the Server Telemetry KQL Database to open it.

![image](https://github.com/user-attachments/assets/f584f675-98ce-4900-8596-10f51e171c5e)

Now click on Server_Telemetry_queryset
 
Copy and paste the code below at the bottom of the code section, then highlight the code and hit the ‘Run’ button to create the new table.
.create table bronzeServerTelemetry(
    datacenter_id: int,
    server_name: string,
    cpu_usage: real,
    memory_usage: real,
    disk_usage: real,
    network_in: real,
    network_out: real,
    power_usage: real,
    timestamp: datetime,
    EventProcessedUtcTime: datetime,
    PartitionID: int,
    EventEnqueuedUtcTime: datetime 
)

As shown below:

 ![image](https://github.com/user-attachments/assets/098a41fb-ca89-4db6-a786-62b8a8282fc4)

You should see the new table shown above once the script runs.

Now open the Event Stream and create a new connection to the Event Hub

Now create a new Event Stream to process the data as shown below:

![image](https://github.com/user-attachments/assets/79de8763-0288-4189-b5ee-4d7f9df07798)

![image](https://github.com/user-attachments/assets/6aed5065-7a93-4678-923e-956a24cc94d5)

Connect the source to the Event Hub that we created earlier by selecting ‘Azure Event Hubs’ from the New source section of the Event Stream.

![image](https://github.com/user-attachments/assets/d83e1faf-cb76-493a-9b42-ea3eb4ffb270)

![image](https://github.com/user-attachments/assets/91299630-c32b-4d7f-9d42-1b11bcc1a4e9)


Grafana image
![image](https://github.com/user-attachments/assets/2f70f91c-ceb3-402a-bd8e-81f51be62922)










