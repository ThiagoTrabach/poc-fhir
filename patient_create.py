# Imports the types Dict and Any for runtime type hints.
from typing import Any, Dict  # noqa: E402


def create_patient(
    project_id: str,
    location: str,
    dataset_id: str,
    fhir_store_id: str,
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
    from googleapiclient import discovery

    api_version = "v1"
    service_name = "healthcare"

    # Returns an authorized API client by discovering the Healthcare API
    # and using GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = discovery.build(service_name, api_version)

    # TODO(developer): Uncomment these lines and replace with your values.
    # project_id = 'my-project'
    # location = 'us-central1'
    # dataset_id = 'my-dataset'
    # fhir_store_id = 'my-fhir-store'
    fhir_store_parent = (
        f"projects/{project_id}/locations/{location}/datasets/{dataset_id}"
    )
    fhir_store_name = f"{fhir_store_parent}/fhirStores/{fhir_store_id}"

    patient_body = {
        "name": [{"use": "official", "family": "Smith", "given": ["Darcy"]}],
        "gender": "female",
        "birthDate": "1970-01-01",
        "resourceType": "Patient",
    }

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
