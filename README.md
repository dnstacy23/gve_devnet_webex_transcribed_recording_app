# GVE DevNet Webex Transcribed Recording App
This repository contains the source code of a Flask app that will display all the available Webex recordings of a Webex user. Additionally, the Flask app can create a video from the recording with closed captions from the transcription that the user can download. 

![/IMAGES/workflow.png](/IMAGES/workflow.png)

## Contacts
* Danielle Stacy

## Solution Components
* Python 3.12
* Webex

## Prerequisites
- **Webex API Personal Token**:
1. To use the Webex REST API, you need a Webex account backed by Cisco Webex Common Identity (CI). If you already have a Webex account, you're all set. Otherwise, go ahead and [sign up for a Webex account](https://cart.webex.com/sign-up).
2. When making request to the Webex REST API, the request must contain a header that includes the access token. A personal access token can be obtained [here](https://developer.webex.com/docs/getting-started).

> Note: This token has a short lifetime - only 12 hours after logging into this site - so it shouldn't be used outside of app development.

- **OAuth Integrations**: Integrations are how you request permission to invoke the Webex REST API on behalf of another Webex Teams user. To do this in a secure way, the API supports the OAuth2 standard which allows third-party integrations to get a temporary access token for authenticating API calls instead of asking users for their password. To register an integration with Webex Teams:
1. Log in to `developer.webex.com`
2. Click on your avatar at the top of the page and then select `My Webex Apps`
3. Click `Create a New App`
4. Click `Create an Integration` to start the wizard
5. Follow the instructions of the wizard and provide your integration's name, description, and logo
6. After successful registration, you'll be taken to a different screen containing your integration's newly created Client ID and Client Secret
7. Copy the secret and store it safely. Please note that the Client Secret will only be shown once for security purposes
8. Note that access token may not include all the scopes necessary for this prototype by default. To include the necessary scopes, select `My Webex Apps` under your avatar once again. Then click on the name of the integration you just created. Scroll down to the `Scopes` section. From there, select all the scopes needed for this integration.

> To read more about Webex Integrations & Authorization and to find information about the different scopes, you can find information [here](https://developer.webex.com/docs/integrations)

> Note: This code repository currently uses the Personal Token method, but it can be modified to authenticate through the OAuth Integration

## Installation/Configuration
1. Clone this repository with `git clone [repository name]`
2. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
3. Add Webex API Key (if using the API Personal Token) to the environmental variables in the .env file:
```python
API_KEY = "enter API key here"
BASE_URL = "https://webexapis.com/v1"
```
4. Install the requirements with the command `pip3 install -r requirements.txt`

## Usage
To start the web app, use the command
```
$ flask run
```

Then access the web app in the browser of you choice at the address `http://127.0.0.1:5000`. From here, you will be presented with a table of the available recordings in your Webex account in the date range specified.

![/IMAGES/table.png](/IMAGES/table.png)

To download the recordings with the transcript overlaid on the video, select the recordings you wish to download and then click the Download button. While the web server processes your request and creates the video, you will see a loading screen on the webpage. Once the video is complete, a success status message appears on the top of the web page. If there was an error, an error message will display.

![/IMAGES/loading.png](/IMAGES/loading.png)

![/IMAGES/success.png](/IMAGES/success.png)

If the download succeeds, then you will now find a zip file with all the videos in your Downloads. Unzip the file to reveal all the video recordings. To view a video, open it any video player. If the success message appears but the zip file has not downloaded, make sure pop-ups are allowed for the url in your browser.

![/IMAGES/video.png](/IMAGES/video.png)

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
