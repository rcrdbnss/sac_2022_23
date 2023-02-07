export TOPIC=wine_orders
gcloud pubsub topics create ${TOPIC}

export SUBSCRIPTION_NAME=wine_sub
gcloud pubsub subscriptions create ${SUBSCRIPTION_NAME} --topic ${TOPIC}
