1. Create virtualenv
* cd <project> and install requirements:
`pip install -r requirements.txt`

2. [Create a Google cloud service account](https://cloud.google.com/docs/authentication/getting-started)
and set the environment variable GOOGLE_APPLICATION_CREDENTIALS


3. [Create bucket on Google Cloud Storage](https://cloud.google.com/storage/docs/creating-buckets?hl=en_US)
and set the environment variable GCP_STORAGE_BACKEND 
to the name of Cloud Storage bucket.

4. Run tests
`python -m pytest`
