from datetime import datetime
from decouple import config
from khayyam import JalaliDatetime
import requests
import json

from send_mail import send_smtp_email

# Load Variables
URL = config('URL')
SECRET_KEY = config('SECRET_KEY')
url = URL + SECRET_KEY
SEND_MAIL = config('SEND_MAIL', cast=bool)
ALLOWED_CURRENCY = config('ALLOWED_CURRENCY', cast=lambda v: [s.strip() for s in v.split(',')], default=None)



def get_rates():
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        rates = data['rates']
        if ALLOWED_CURRENCY[0] != '':
            tmp = {}
            for exc in ALLOWED_CURRENCY:
                tmp[exc] = rates[exc]
            rates = tmp
            if 'BTC' in rates.keys():
                rates['BTC'] = 1 / rates['BTC']
            return rates
    return None



def send_mail(rates):
    subject = "currency rate"
    time_chris = datetime.now()
    time_jalali = JalaliDatetime(datetime.now()).localdatetimeformat()
    if ALLOWED_CURRENCY[0] != '':
        text = json.dumps(rates)
        send_smtp_email(subject, time_chris, time_jalali, text)
    else:
        print("None")




if __name__ == '__main__':
    rates = get_rates()
    if SEND_MAIL:
        send_mail(rates)