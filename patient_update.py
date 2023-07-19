from typing import Any, Dict
from googleapiclient import discovery
from dotenv import load_dotenv
import os
from utils import import_json_to_dictionary
import json

load_dotenv()

def main():
    # Load environment variables
    project_id = os.environ.get('PROJECT_ID')
    location = os.environ.get('LOCATION')
    dataset_id = os.environ.get('DATASET_ID')
    fhir_store_id = os.environ.get('FHIR_STORE_ID')

    # Import patient data from JSON file
    patient_to_update = import_json_to_dictionary('./data/patient_to_update.json')
    
     # Update the patient
    update_resource(
        project_id,
        location,
        dataset_id,
        fhir_store_id,
        patient_to_update,
        patient_to_update['resourceType'],
        patient_to_update['id']
    )


def update_resource(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    patient_to_update: dict,
    resource_type: str,
    resource_id: str,
) -> Dict[str, Any]:
    """Updates the entire contents of a FHIR resource.
    Creates a new current version if the resource already exists, or creates
    a new resource with an initial version if no resource already exists with
    the provided ID.
    Args:
        project_id: The project ID or project number of the Cloud project you want
        to use.
        location: The name of the parent dataset's location.
        dataset_id: The name of the parent dataset.
        fhir_store_id: The name of the FHIR store.
        patient_to_update: The dictionary representing the patient to be updated.
        resource_type: The type of the FHIR resource.
        resource_id: The "logical id" of the resource. The ID is assigned by the
        server.
    Returns:
        A dict representing the updated FHIR resource.
    """

    # Set up API client
    api_version = "v1"
    service_name = "healthcare"
    client = discovery.build(service_name, api_version)

    # Set up FHIR store information
    fhir_store_parent = f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    fhir_resource_path = f"{fhir_store_parent}/fhirStores/{fhir_store_id}/fhir/{resource_type}/{resource_id}"

    # Set up patient body
    patient_body = patient_to_update

    # Create the request to update the patient
    request = client.projects().locations().datasets().fhirStores().fhir().update(
        name=fhir_resource_path,
        body=patient_body
    )

    # Set required headers
    request.headers["content-type"] = "application/fhir+json;charset=utf-8"

    # Execute the request
    response = request.execute()

    # Print the ID of the updated patient
    print(f"Updated {resource_type} resource with ID {resource_id}:\n {json.dumps(response, indent=2)}")
    return response


if __name__ == '__main__':
    main()