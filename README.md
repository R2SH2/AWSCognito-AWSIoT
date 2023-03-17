# AWS Cognito and IoT MQTT Example

This script demonstrates how to use AWS Cognito User Pools to authenticate a user, obtain temporary AWS credentials, and then interact with AWS IoT using MQTT messaging. The script uses the AWSIoTPythonSDK and boto3 libraries.

## Dependencies

- AWSIoTPythonSDK
- boto3

## Overview

The script contains the following sections:

1. Import required libraries.
2. Set up necessary configuration variables for Cognito User Pools, AWS IoT, and MQTT.
3. Define a function `generate_secret_hash` to generate the secret hash required for authentication.
4. Authenticate the user using Cognito and obtain the ID token.
5. Obtain temporary AWS credentials using the ID token.
6. Initialize the AWSIoTMQTTShadowClient with the given configuration.
7. Connect to the AWS IoT platform using the initialized MQTT shadow client.
8. Configure the MQTT connection settings.
9. Define a callback function `on_message_received` to handle message events when subscribed to a topic.
10. Subscribe to the specified topic and register the callback function.
11. Publish a message to the subscribed topic.
12. Keep the script running to receive messages until interrupted.

## Configuration

To use this script, make sure to replace the following variables with your own values:

- `COGNITO_USER_POOL_ID`
- `COGNITO_APP_CLIENT_ID`
- `COGNITO_IDENTITY_POOL_ID`
- `COGNITO_APP_CLIENT_SECRET`
- `AWS_REGION`
- `IOT_ENDPOINT`
- `ROOT_CA_PATH`
- `CERTIFICATE_FILE`
- `PRIVATE_KEY_FILE`
- `TOPIC_NAME`
- `USERNAME`
- `PASSWORD`

## Security Note

Please note that this script is a standalone example, and you should properly handle sensitive information (such as credentials) by storing them in a secure way (e.g., AWS Secrets Manager, environment variables) instead of hardcoding them in the script.
