<p style="text-align: center;"><strong>Fabric Real-time Grafana Demo</strong></p>

This repo will walk you through creating a Fabric Eventstream and Eventhouse and then streaming synthetic server telemetry data to it. We will then create an Azure Managed Grafana dashboard to visualize the data. This demo assumes you have a regular or trial Fabric or Power BI Premium instance you can use. Create the Grafana and Event Hubs items below in the same region as your Power BI Premium or Fabric instance if possible. This demo will use VS Code with a Python script to generate the server telemetry data, so you will need VS Code and Python installed on your client machine. 

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

Fill in the details below. Create any name and location you would like, but use the same region as the Grafana and Fabric instances is possible. Once done, select to 'Review and Create' and then 'Create' the Event Hub namespace:

![image](https://github.com/user-attachments/assets/85ff1644-378a-4c10-a7fd-b2eeedc03311)

Once the event hub namespace is created, create an event hub in it:

![image](https://github.com/user-attachments/assets/9c271028-8f21-44c9-8f3d-c850c5762820)

![image](https://github.com/user-attachments/assets/f3a4dfce-5587-4173-898a-4c02bf977836)

Take the defaults for everything else and hit ‘Review and Create’ to create the event hub.

Once the event hub has been created, create a SAS policy we can use to connect to it and stream data in as shown below. First select 'Add' to add a new policy, then give it a name and check the 'Send' and 'Listen' check boxes and then hit 'Create'. Make sure you are creating the policy for the Event hub and not the Event hub namespace it belongs to:

![image](https://github.com/user-attachments/assets/738c57ad-f04c-4753-8c57-45240e61e714)

Now back in Fabric, create a new Eventhouse to store the telemetry data that will be streamed in:

![image](https://github.com/user-attachments/assets/b6e8fcd2-7a89-44e2-92a8-f1a1790cadeb)

Name the Eventhouse 'Server Telemetry' as shown below:

![image](https://github.com/user-attachments/assets/0a2a4f69-7648-44b6-8b7e-04bb185acebe)

Next open the Server Telemetry Eventhouse and select the Server Telemetry KQL Database to open it.

<img src="https://github.com/user-attachments/assets/f584f675-98ce-4900-8596-10f51e171c5e" alt="Image description" width="500" height="300">
![image](https://github.com/user-attachments/assets/f584f675-98ce-4900-8596-10f51e171c5e)

Now click on Server_Telemetry_queryset. Copy and paste the code below at the bottom of the code section, then highlight the code and hit the ‘Run’ button to create the new table.
 
=============    
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

=============  

As shown below:

 ![image](https://github.com/user-attachments/assets/098a41fb-ca89-4db6-a786-62b8a8282fc4)

You should see the new table shown above once the script runs.



Now create a new Event Stream to process the data as shown below:

![image](https://github.com/user-attachments/assets/79de8763-0288-4189-b5ee-4d7f9df07798)

![image](https://github.com/user-attachments/assets/6aed5065-7a93-4678-923e-956a24cc94d5)

Connect the source to the Event Hub that we created earlier by selecting ‘Use External Source’ from the home screen of the Event Stream. Then select to connect to an 'Azure Event Hub':

![image](https://github.com/user-attachments/assets/2ed5294c-1bfc-4396-a2f4-49e4ecccf9cd)

Select to add a new connection and then add the connection details for the Event Hub we created earlier. For the Shared Access Key Name and Key, reference the values we created above for the Event Hub SAS key.

![image](https://github.com/user-attachments/assets/91299630-c32b-4d7f-9d42-1b11bcc1a4e9)

If you are asked for the consumer group put in '$Default', for the data format put in 'Json':

![image](https://github.com/user-attachments/assets/e9ce335c-61b1-41ab-8fda-d18d269c9b80)

Hit 'Next' and then add the new connection.

![image](https://github.com/user-attachments/assets/b7429f81-3c88-492b-b6a1-85882d00ffc8)

Now add the destination for the Eventhouse we created as shown below:

![image](https://github.com/user-attachments/assets/bd94abd8-f4f3-42e8-be98-4223f24093c9)

Setup the connection as shown below and select to save it when done:

![image](https://github.com/user-attachments/assets/42581d00-6b16-41e7-b3d6-0c65ffb73e53)

Now publish the new Eventstream so that it can start processing events:

![image](https://github.com/user-attachments/assets/afd6e4cf-133c-478a-9a8e-497e4205a0ef)

Now open VS Code and then select ‘File’ -> ‘Open Folder’ and then navigate to the location of the ‘Send Event Hub Message’ folder downloaded from this repo. On line 8 and 9 change the connection string and event hub name for your event hub. 

![image](https://github.com/user-attachments/assets/7e671c40-002a-4e88-94d2-fa5445623c4f)

The event hub connection string can be found on the page below where we created the SAS key for the Event hub above. For the Event Hub name put in the name of the Event hub (not the name of the Event hub namespace).

![image](https://github.com/user-attachments/assets/d405406b-7749-4aba-8b7b-a3bc80367786)

Once that is complete, run the script to start sending messages to the event hub that can be consumed by the Event Stream. The Event Stream will send the messages to the Server_Telemetry KQL database. Note you may need to do a pip install of the azure-eventhub library in your Python environment for the script to work. 

Now go back to the Azure Managed Grafana instance in Azure created at the beginning. Click on the Endpoint to launch the Grafana interface. Login with your id:

![image](https://github.com/user-attachments/assets/289cdb8f-ef74-411e-a92f-006b5aa0ee4a)

Select to ‘Configure a new data source’

![image](https://github.com/user-attachments/assets/ac831ec0-bc3a-46d5-963e-f9674b2c0bd8)

Search for ‘data explorer’, then select Azure Data Explorer datasource. This is the same connector that will work with the Fabric KQL databases. On the configuration screen that pops up next, change the name to something like ‘Fabric-Server-Telemetry’ to easily identify the source. 

![image](https://github.com/user-attachments/assets/60682681-b233-4a0a-8dc0-d86e53260b36

Now back in Fabric in the KQL database, copy the ingestion URI as shown below. 

![image](https://github.com/user-attachments/assets/e4c344dc-5863-4227-80fa-777cac10f246)

Now paste it into the Default cluster URL. Set the authentication to use ‘Current User’ for this demo.

![image](https://github.com/user-attachments/assets/85f4374c-4c64-4d48-a8b4-e6c7838e3ba0)

Before saving the new source and testing it, first copy the name of your Azure Managed Grafana instance, which is the name of the managed identity, and add it as a contributor on your Fabric workspace. 

![image](https://github.com/user-attachments/assets/9442d158-2c53-4c1a-abe5-866618303396)

Once that is done, go back to your Grafana instance and ‘Save and Test’ the connection.
Now click on ‘Dashboards’ on the left, then select ‘New -> Dashboard’.

![image](https://github.com/user-attachments/assets/b49b366d-b864-4393-b354-bbaf7ecaf519)

Select to add a new visualization

![image](https://github.com/user-attachments/assets/499fae82-334c-40db-82e5-b532eb8018ff)

Select the Fabric-Server-Telemetry connection:

![image](https://github.com/user-attachments/assets/c47dd0c3-6e64-4a80-abb7-6e11d001e11d)

![image](https://github.com/user-attachments/assets/09f98cd9-3d7d-4daf-afbc-c70db2b54d96)

Note there is a bug in Grafana where sometimes it doesn’t show the graphical query builder correctly as shown below:

![image](https://github.com/user-attachments/assets/08658088-51ac-4e2d-85fd-3f81eba3d5fc)

If that happens, just hit ‘Apply’ on the top right of the screen to reset the builder. 

![image](https://github.com/user-attachments/assets/835670a3-df5a-4b36-8653-3ec42ec359e2)

Then select the menu on the top right corner of the blank visual and select ‘Edit’:

![image](https://github.com/user-attachments/assets/9f65c7c9-1b0d-4a9c-b0cf-6739fcd865ab)

Now in the query builder, select the ‘server_name, cpu_usage, and timestamp fields to include in the visual.

![image](https://github.com/user-attachments/assets/82d90639-6d36-411c-bbce-cf696bc598a0)

Also select the options below to ensure the data is displayed correctly:
![image](https://github.com/user-attachments/assets/2f70f91c-ceb3-402a-bd8e-81f51be62922)










