from difflib import SequenceMatcher
from env import env
from flask import Flask, request
import json
from pprint import pprint
from twilio.rest import Client
from twilio.twiml.voice_response import Dial, Number, Record, VoiceResponse

# TODO: use similar() to check transcriptions and mark duplicates
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

app = Flask(__name__)
env = env()

account_sid = env['account_sid']
auth_token = env['auth_token']
client = Client(account_sid, auth_token)

report_number = env['report_number']
twilio_number = env['twilio_number']
api_url = env['api_url']

@app.route('/', methods=['GET', 'POST'])
def get_calls():
    calls = client.calls.list(from_=twilio_number, to=report_number, status="completed")
    recordings = client.recordings.list()
    transcriptions = client.transcriptions.list()

    all_calls = []
    for idx, val in enumerate(calls):
        # if int(val.duration) > 15:
        recording = next((x for x in recordings if x.call_sid == val.sid), None)
        if recording:
            _call = {}
            _call['created_at'] = val.date_created.isoformat()

            _call['recording'] = 'https://api.twilio.com' + recording.uri.replace('.json', '')

            _call['transcription'] = ''
            transcription = next((x for x in transcriptions if x.recording_sid == recording.sid), None)
            if transcription:
                _call['transcription'] = transcription.transcription_text

            all_calls.append(_call)

    return json.dumps(all_calls)


@app.route('/record', methods=['GET', 'POST'])
def record():
    response = VoiceResponse()
    response.record(
        timeout=2, transcribe=True,
        max_length=60, play_beep=False,
        action=api_url+'/call-ended'
    )

    return str(response)

@app.route('/call-ended', methods=['GET', 'POST'])
def call_ended():
    return '<Response/>'


if __name__ == "__main__":
    app.run(debug=True)
