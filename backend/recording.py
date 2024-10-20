import requests
import time
import json
import os 

# Replace with your actual Agora app ID and other necessary details
AGORA_APP_ID = os.getenv('VITE_AGORA_APP_ID')
AGORA_APP_CERTIFICATE = 'your_app_certificate'
BASE_URL = 'https://api.agora.io/v1/apps/{AGORA_APP_ID}/cloud_recording'

def acquire_resource():
    url = f"{BASE_URL}/acquire"
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Basic {}'.format(AGORA_APP_CERTIFICATE)  # Base64 encoded
    }
    payload = {
        "cname": "meeting_channel",
        "uid": "user_id",
        "clientRequest": {
            "resourceExpiredHour": 24,
            "scene": 0
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def start_recording(resource_id):
    url = f"{BASE_URL}/resourceid/{resource_id}/mode/mix/start"
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Basic {}'.format(AGORA_APP_CERTIFICATE)
    }
    payload = {
        "uid": "user_id",
        "cname": "meeting_channel",
        "clientRequest": {
            "token": "your_token_if_any",
            "recordingConfig": {
                "maxIdleTime": 30,
                "streamTypes": 2,
                "audioProfile": 1,
                "channelType": 0,
                "videoStreamType": 0,
                "transcodingConfig": {
                    "height": 640,
                    "width": 360,
                    "bitrate": 500,
                    "fps": 15,
                    "mixedVideoLayout": 1,
                    "backgroundColor": "#FF0000"
                },
                "subscribeVideoUids": ["user_id"],  # Replace with actual UIDs
                "subscribeAudioUids": ["user_id"],
                "subscribeUidGroup": 0
            },
            "storageConfig": {
                "accessKey": "your_access_key",
                "region": 3,
                "bucket": "your_bucket_name",
                "secretKey": "your_secret_key",
                "vendor": 2,
                "fileNamePrefix": ["directory1", "directory2"]
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def stop_recording(resource_id, sid):
    url = f"{BASE_URL}/resourceid/{resource_id}/sid/{sid}/mode/mix/stop"
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'Basic {}'.format(AGORA_APP_CERTIFICATE)
    }
    payload = {
        "cname": "meeting_channel",
        "uid": "user_id",
        "clientRequest": {}
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def main():
    resource_response = acquire_resource()
    resource_id = resource_response['resourceId']

    while True:
        start_response = start_recording(resource_id)
        sid = start_response['sid']
        print(f"Started recording with SID: {sid}")

        # Record for 3 minutes (180 seconds)
        time.sleep(180)

        stop_response = stop_recording(resource_id, sid)
        print(f"Stopped recording: {stop_response}")

        # Optional: Wait before starting a new recording
        # time.sleep(10)  # Wait for 10 seconds before the next recording

if __name__ == "__main__":
    main()