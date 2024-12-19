# Work in progress. Ignore this file for now.

from fhir.resources.observation import Observation
from datetime import datetime
from fhir.resources.quantity import Quantity
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
import json

# Sample JSON data
data_json = '{"DeviceId": "Device-2", "HeartRate": 84, "BloodPressure": {"Systolic": 133, "Diastolic": 76}, "Temperature": 37.1, "MeasurementDate": "2024-12-03T21:44:20.641585"}'

# Parse JSON data
data = json.loads(data_json)

# Convert to FHIR Observation
def convert_to_fhir_observation(data):
    # Create FHIR Observation resource
    observation = Observation(
        status="final",
        category=[CodeableConcept(coding=[Coding(system="http://terminology.hl7.org/CodeSystem/observation-category", code="vital-signs")])],
        code=CodeableConcept(coding=[Coding(system="http://loinc.org", code="85354-9", display="Vital signs")]),
        subject={"reference": f"Device/{data['DeviceId']}"},
        effectiveDateTime=datetime.fromisoformat(data['MeasurementDate']),
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

# Convert the sample data to FHIR Observation
fhir_observation = convert_to_fhir_observation(data)

# Print the FHIR Observation resource as JSON
print(fhir_observation.json(indent=2))