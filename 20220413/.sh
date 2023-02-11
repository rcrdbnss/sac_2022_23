export PROJECT_ID=rbenassi-20220413

export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"

gcloud projects create ${PROJECT_ID} --set-as-default

export NAME=webuser

gcloud iam service-accounts create ${NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com" --role "roles/owner"
gcloud iam service-accounts keys create credentials.json --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com
