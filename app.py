""" Copyright (c) 2023 Cisco and/or its affiliates.
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

# Import Section
from flask import Flask, render_template, request, jsonify
import datetime
import requests
import json
from dotenv import load_dotenv
import os
from vtt_to_srt.vtt_to_srt import ConvertFile
import ffmpeg
import webex_api

# load all environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")


# Global variables
app = Flask(__name__)


# Methods
# Returns location and time of accessing device
def getSystemTimeAndLocation():
    # request user ip
    userIPRequest = requests.get('https://get.geojs.io/v1/ip.json')
    userIP = userIPRequest.json()['ip']

    # request geo information based on ip
    geoRequestURL = 'https://get.geojs.io/v1/ip/geo/' + userIP + '.json'
    geoRequest = requests.get(geoRequestURL)
    geoData = geoRequest.json()

    #create info string
    location = geoData['country']
    timezone = geoData['timezone']
    current_time=datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    timeAndLocation = "System Information: {}, {} (Timezone: {})".format(location, current_time, timezone)

    return timeAndLocation


##Routes
#Instructions


#Table
@app.route('/')
def table():
    try:
        #Use APIs to get all Webex recordings of user
        headers = {
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json; charset=utf-8"
        }
        webex_recordings = webex_api.get_recordings(BASE_URL, headers,
                                                    from_datetime="2020-01-27T8:00:00Z",
                                                    to_datetime="2023-05-31T9:00:00Z")
        recording_info = []
        for recording in webex_recordings:
            info = {
                "name": recording["topic"],
                "date": recording["timeRecorded"],
                "duration": recording["durationSeconds"],
                "size": recording["sizeBytes"],
                "format": recording["format"],
                "id": recording["id"]
            }
            recording_info.append(info)
        #Page without error message and defined header links
        #Pass the recording information to the template for displaying
        return render_template('table.html', hiddenLinks=False,
                               timeAndLocation=getSystemTimeAndLocation(),
                               recordings=recording_info)
    except Exception as e:
        print(e)
        #OR the following to show error message
        return render_template('table.html', error=False,
                               errormessage="CUSTOMIZE: Add custom message here.",
                               errorcode=e,
                               timeAndLocation=getSystemTimeAndLocation())


#This route is called when the user downloads a recording
@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        try:
            #Get the list of recordings the user wants to download
            recordings = request.json["items"]

            headers = {
                "Authorization": "Bearer " + API_KEY,
                "Content-Type": "application/json; charset=utf-8"
            }

            #Get the recording and transcript download links
            for recording_id in recordings:
                recording = webex_api.get_specific_recording(BASE_URL, headers, recording_id)

                recording_name = recording["topic"].replace(" ", "").replace("'", "").replace(":", "")
                video_link = recording["temporaryDirectDownloadLinks"]["recordingDownloadLink"]
                webex_api.get_recording_video(video_link, recording_name)

                transcript_link = recording["temporaryDirectDownloadLinks"]["transcriptDownloadLink"]
                webex_api.get_transcript(transcript_link, recording_name)

                #Convert the vtt file to an srt file

                convert_file = ConvertFile(recording_name+"_transcript.vtt", "utf-8")
                convert_file.convert()

                #Modify srt file to the proper format
                add_lines = []
                with open(recording_name+"_transcript.srt", "r") as transcript_file:
                    for line in transcript_file.readlines():
                        if line[0].isdigit() and line[1] == " ":
                            continue
                        add_lines.append(line)

                with open(recording_name+"_transcript.srt", "w") as transcript_file:
                    for line in add_lines:
                        transcript_file.write(line)

                #Add the subtitles from the srt file to the video
                video = ffmpeg.input(recording_name+"_movie.mp4").video
                audio = ffmpeg.input(recording_name+"_movie.mp4").audio

                video_with_subtitles = video.filter("subtitles",
                                                    recording_name+"_transcript.srt")
                final_recording = ffmpeg.output(video_with_subtitles, audio,
                                                recording_name+"_subtitled_video.mp4")
                final_recording.overwrite_output().run()

            #Everything works
            return jsonify({"status": "Success"})

        except Exception as e:
            print(e)

            #Something has gone wrong
            return jsonify({"status": "Failure"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
