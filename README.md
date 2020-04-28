1. Create virtualenv
`virtualenv -p python3.8 google_vision`

Activate it
`source google_vision/bin/activate`

2. Install requirements
`pip install -r requirements.txt`

3. [Create a Google cloud service account](https://cloud.google.com/docs/authentication/getting-started)
and set the environment variable GOOGLE_APPLICATION_CREDENTIALS


4. [Create bucket on Google Cloud Storage](https://cloud.google.com/storage/docs/creating-buckets?hl=en_US)
and set the environment variable GCP_STORAGE_BACKEND 
to the name of Cloud Storage bucket.

5. Run tests
`python -m pytest`
