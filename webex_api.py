"""
Copyright (c) 2024 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import requests, json
import sys
import os
import urllib.request
from dotenv import load_dotenv
from pprint import pprint


def get_recordings(base_url, headers, from_datetime=None, to_datetime=None):
    recordings_endpoint = "/recordings"
    if from_datetime and to_datetime:
        recordings_endpoint += "?from={}&to={}".format(from_datetime, to_datetime)
    elif from_datetime:
        recordings_endpoint += "?from={}".format(from_datetime)
    elif to_datetime:
        recordings_endpoint += "?to={}".format(to_datetime)

    recordings_response = requests.get(base_url+recordings_endpoint,
                                       headers=headers)
    recordings = json.loads(recordings_response.text)["items"]

    return recordings


def get_specific_recording(base_url, headers, recording_id):
    recording_endpoint = "/recordings/" + recording_id
    recording_response = requests.get(base_url+recording_endpoint, headers=headers)
    recording = json.loads(recording_response.text)

    return recording


def get_transcript(transcript_link, recording_name):
    transcript = requests.get(transcript_link)
    with open(recording_name + "_transcript.vtt", "w") as transcript_file:
        transcript_file.write(transcript.text)


def get_recording_video(recording_link, recording_name):
    urllib.request.urlretrieve(recording_link, recording_name+"_movie.mp4")
