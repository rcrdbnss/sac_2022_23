export PROJECT_ID=rbenassi-20220224

export TOPIC1=hand_irr
export TOPIC2=humidity

export TOKEN="zxcvtoken"

export SUBSCRIPTION_NAME1=hand_irr_sub
export SUBSCRIPTION_NAME2=humidity_sub

gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME1} --topic ${TOPIC1} --push-endpoint \
"https://${PROJECT_ID}.appspot.com/pubsub/push/hand_irr?token=${TOKEN}" --ack-deadline=10

gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME2} --topic ${TOPIC2} --push-endpoint \
"https://${PROJECT_ID}.appspot.com/pubsub/push/humidity?token=${TOKEN}" --ack-deadline=10
