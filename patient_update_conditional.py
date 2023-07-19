from dotenv import load_dotenv
import os
from utils import import_json_to_dictionary
import json
from google.auth.transport import requests
from google.oauth2 import service_account


load_dotenv()

#conditional update only available in beta endpoint
_BASE_URL = "https://healthcare.googleapis.com/v1beta1" 

def main():

    # Load environment variables
    gcp_credentials = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    project_id = os.environ.get('PROJECT_ID')
    location = os.environ.get('LOCATION')
    dataset_id = os.environ.get('DATASET_ID')
    fhir_store_id = os.environ.get('FHIR_STORE_ID')
    

    # Import patient data from JSON file
    #patient_to_create = import_json_to_dictionary('./data/patient_to_update_conditional.json')


    conditional_update_resource(
        gcp_credentials,
        _BASE_URL,
        project_id,
        location,
        dataset_id,
        fhir_store_id
        )

def get_session(service_account_json):
    """
    Returns an authorized Requests Session class using the service account
    credentials JSON. This class is used to perform requests to the
    Healthcare API endpoint.
    """

    # Pass in the credentials and project ID. If none supplied, get them
    # from the environment.
    credentials = service_account.Credentials.from_service_account_file(
        service_account_json
    )
    scoped_credentials = credentials.with_scopes(
        ["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Create a requests Session object with the credentials.
    session = requests.AuthorizedSession(scoped_credentials)

    return session


def conditional_update_resource(
    service_account_json,
    base_url,
    project_id,
    cloud_region,
    dataset_id,
    fhir_store_id
):
    """
    If a resource is found based on the search criteria specified in
    the query parameters, updates the entire contents of that resource.
    """
    url = f"{base_url}/projects/{project_id}/locations/{cloud_region}"

    # The search query in this request updates all Observations
    # using the Observation's identifier (ABC-12345 in my-code-system)
    # so that their 'status' is 'cancelled'.
    resource_path = "{}/datasets/{}/fhirStores/{}/fhir/Patient".format(
        url, dataset_id, fhir_store_id
    )

    # Make an authenticated API request
    session = get_session(service_account_json)

    body = {
    "identifier": [
        {
            "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
            "code": "SS",
            "value": "999-87-3391"
        }
    ],
    "name": [{"use": "official", "family": "Pilar", "given": ["Melgar"]}],
    "gender": "male",
    "birthDate": "1900-01-10",
    "resourceType": "Patient",
    "active": True}

    headers = {"Content-Type": "application/fhir+json;charset=utf-8"}

    params = {"identifier": "ss|999-87-3391"}

    response = session.put(resource_path, headers=headers, params=params, json=body)

    response.raise_for_status()
    resource = response.json()

    print(
        "Conditionally updated Observations with the identifier "
        "'my-code-system|ABC-12345' to have a 'status' of "
        "'cancelled'."
    )
    print(json.dumps(resource, indent=2))

    return resource


if __name__ == '__main__':
    main()
