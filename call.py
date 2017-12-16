from twilio.rest import Client
from env import env

env = env()

account_sid = env['account_sid']
auth_token = env['auth_token']
client = Client(account_sid, auth_token)

report_number = env['report_number']
twilio_number = env['twilio_number']
api_url = env['api_url']

call = client.api.account.calls\
      .create(to=report_number,
              from_=twilio_number,
              url=api_url+'/record',
              send_digits='1')

return str(call.sid)
