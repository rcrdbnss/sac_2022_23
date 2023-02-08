export PROJECT_ID=rbenassi-20220224

export TOPIC1=hand_irr

export TOPIC2=humidity

gcloud pubsub topics create ${TOPIC1}

gcloud pubsub topics create ${TOPIC2}
