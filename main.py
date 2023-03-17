import boto3
import json
import uuid
import hashlib
import hmac
import base64
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient


# Replace the following variables with your own values 🥹
COGNITO_USER_POOL_ID = ''
COGNITO_APP_CLIENT_ID = ''
COGNITO_IDENTITY_POOL_ID = ''
COGNITO_APP_CLIENT_SECRET = ''
AWS_REGION = ''
IOT_ENDPOINT = ''
ROOT_CA_PATH = ""
CERTIFICATE_FILE = ""
PRIVATE_KEY_FILE = ""
CLIENT_ID = f'my-mqtt-client-{uuid.uuid4()}'
TOPIC_NAME = ''
MESSAGE = {"message": f"Hello from Cognito User Pool"}

# Replace with your user's credentials
USERNAME = ''
PASSWORD = ''

# Define a function to generate the SECRET_HASH:
def generate_secret_hash(username, app_client_id, app_client_secret):
    message = username + app_client_id
    secret_hash = hmac.new(
        key=bytes(app_client_secret, "utf-8"),
        msg=bytes(message, "utf-8"),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(secret_hash).decode()

# Generate the SECRET_HASH
secret_hash = generate_secret_hash(USERNAME, COGNITO_APP_CLIENT_ID, COGNITO_APP_CLIENT_SECRET)

# Authenticate the user
cognito_idp = boto3.client('cognito-idp', region_name=AWS_REGION)
response = cognito_idp.initiate_auth(
    AuthFlow='USER_PASSWORD_AUTH',
    AuthParameters={
        'USERNAME': USERNAME,
        'PASSWORD': PASSWORD,
        'SECRET_HASH': secret_hash
    },
    ClientId=COGNITO_APP_CLIENT_ID
)

id_token = response['AuthenticationResult']['IdToken']

# Obtain temporary AWS credentials
cognito_identity = boto3.client('cognito-identity', region_name=AWS_REGION)
response = cognito_identity.get_id(
    IdentityPoolId=COGNITO_IDENTITY_POOL_ID,
    Logins={
        f'cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}': id_token
    }
)
identity_id = response['IdentityId']
response = cognito_identity.get_credentials_for_identity(
    IdentityId=identity_id,
    Logins={
        f'cognito-idp.{AWS_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}': id_token
    }
)
credentials = response['Credentials']
print(f'Your credentials are {credentials}')


# Initialize the AWSIoTMQTTShadowClient
shadow_client = AWSIoTMQTTShadowClient(CLIENT_ID)
shadow_client.configureEndpoint(IOT_ENDPOINT, 8883)
shadow_client.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_FILE, CERTIFICATE_FILE)


# Connect to the AWS IoT platform
print("Connecting...")
shadow_client.connect()
print("Connected!")

# Initialize the MQTT client
mqtt_client = shadow_client.getMQTTConnection()

# Configure the MQTT connection settings
mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec

# Define a callback function to handle message events
def on_message_received(client, userdata, message):
    print(f"Received message on topic '{message.topic}': {message.payload.decode('utf-8')}")

# Subscribe to the topic and register the callback function
mqtt_client.subscribe(TOPIC_NAME, 1, on_message_received)

# Publish a message to the topic
print(f"Publishing message to topic '{TOPIC_NAME}'")
mqtt_client.publish(TOPIC_NAME, json.dumps(MESSAGE), 1)

# Keep the script running to receive messages
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnecting...")
    shadow_client.disconnect()
    print("Disconnected!")