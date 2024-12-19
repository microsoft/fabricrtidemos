import json
import pyodbc
from fhir.resources.observation import Observation
from fhir.resources.quantity import Quantity
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from datetime import datetime
from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
from azure.kusto.data.exceptions import KustoServiceError
from azure.kusto.data.helpers import dataframe_from_result_table
import pandas as pd


AAD_TENANT_ID  = spark.conf.get("trident.tenant.id")
KUSTO_CLUSTER = "https://<cluster_id>.z0.kusto.data.microsoft.com"
KUSTO_DATABASE = "<kusto_db_name>"


# Function to convert JSON data to FHIR Observation
def convert_to_fhir_observation(data):
    observation = Observation(
        status="final",
        category=[CodeableConcept(coding=[Coding(system="http://terminology.hl7.org/CodeSystem/observation-category", code="vital-signs")])],
        code=CodeableConcept(coding=[Coding(system="http://loinc.org", code="85354-9", display="Vital signs")]),
        subject={"reference": f"Device/{data['DeviceId']}"},
        effectiveDateTime=FHIRDate(data["MeasurementDate"]),
        component=[
            {
                "code": CodeableConcept(coding=[Coding(system="http://loinc.org", code="8867-4", display="Heart rate")]),
                "valueQuantity": Quantity(value=data["HeartRate"], unit="beats/minute", system="http://unitsofmeasure.org", code="/min")
            },
            {
                "code": CodeableConcept(coding=[Coding(system="http://loinc.org", code="8480-6", display="Systolic blood pressure")]),
                "valueQuantity": Quantity(value=data["BloodPressure"]["Systolic"], unit="mmHg", system="http://unitsofmeasure.org", code="mm[Hg]")
            },
            {
                "code": CodeableConcept(coding=[Coding(system="http://loinc.org", code="8462-4", display="Diastolic blood pressure")]),
                "valueQuantity": Quantity(value=data["BloodPressure"]["Diastolic"], unit="mmHg", system="http://unitsofmeasure.org", code="mm[Hg]")
            },
            {
                "code": CodeableConcept(coding=[Coding(system="http://loinc.org", code="8310-5", display="Body temperature")]),
                "valueQuantity": Quantity(value=data["Temperature"], unit="degrees Celsius", system="http://unitsofmeasure.org", code="Cel")
            }
        ]
    )
    return observation

# Connect to the KQL database
conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=your_server_name;Database=your_database_name;UID=your_username;PWD=your_password"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Query to retrieve JSON entries from the KQL database
query = "SELECT json_data FROM your_kql_table"
cursor.execute(query)

# Fetch all JSON entries
json_entries = cursor.fetchall()

# Connect to the Microsoft Fabric lakehouse
lakehouse_conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=your_lakehouse_server_name;Database=your_lakehouse_database_name;UID=your_username;PWD=your_password"
lakehouse_conn = pyodbc.connect(lakehouse_conn_str)
lakehouse_cursor = lakehouse_conn.cursor()

# Iterate through JSON entries, convert to FHIR, and insert into the lakehouse table
for entry in json_entries:
    data = json.loads(entry[0])
    fhir_observation = convert_to_fhir_observation(data)
    fhir_json = fhir_observation.json()
    
    # Insert the FHIR JSON into the lakehouse table
    insert_query = "INSERT INTO dbo.ClinicalFhir (fhir_data) VALUES (?)"
    lakehouse_cursor.execute(insert_query, fhir_json)
    lakehouse_conn.commit()

# Close the connections
cursor.close()
conn.close()
lakehouse_cursor.close()
lakehouse_conn.close()