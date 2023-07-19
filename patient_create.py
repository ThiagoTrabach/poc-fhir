from typing import Any, Dict  # noqa: E402
from googleapiclient import discovery
from dotenv import load_dotenv
import os

load_dotenv()

project_id = os.environ.get('PROJECT_ID')
location = os.environ.get('LOCATION')
dataset_id = os.environ.get('DATASET_ID')
fhir_store_id = os.environ.get('FHIR_STORE_ID')



def main():

    patient_to_create = {
        "name": [{"use": "official", "family": "Thiago", "given": ["Trabach"]}],
        "gender": "male",
        "birthDate": "1988-01-18",
        "resourceType": "Patient",
    }


    create_patient(project_id, location, dataset_id, fhir_store_id, patient_to_create)


def create_patient(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
    patient_to_create: dict
) -> Dict[str, Any]:
    """Creates a new Patient resource in a FHIR store.

    See
    https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/healthcare/api-client/v1/fhir
    before running the sample.
    See
    https://googleapis.github.io/google-api-python-client/docs/dyn/healthcare_v1.projects.locations.datasets.fhirStores.fhir.html#create
    for the Python API reference.

    Args:
      project_id: The project ID or project number of the Cloud project you want
        to use.
      location: The name of the parent dataset's location.
      dataset_id: The name of the parent dataset.
      fhir_store_id: The name of the FHIR store that holds the Patient resource.

    Returns:
      A dict representing the created Patient resource.
    """
    # Imports the Google API Discovery Service.
  

    api_version = "v1"  
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_store_name = f"{fhir_store_parent}/fhirStores/{fhir_store_id}"

    patient_body = patient_to_create

    request = (
        client.projects()
        .locations()
        .datasets()
        .fhirStores()
        .fhir()
        .create(parent=fhir_store_name, type="Patient", body=patient_body)
    )
    # Sets required application/fhir+json header on the googleapiclient.http.HttpRequest.
    request.headers["content-type"] = "application/fhir+json;charset=utf-8"
    response = request.execute()

    print(f"Created Patient resource with ID {response['id']}")
    return response


if __name__ == '__main__':
    main()