#!/usr/bin/env python
import requests

headers = {
    'Accept': 'application/json AppKey:ba063966-5d0d-46ff-be4f-2a9ace0f40a0 Content-Type:application/json',
}

params = (
    ('Accept', 'application/json-compressed'),
    ('_twsr', '1'),
    ('Content-Type', 'application/json'),
)

data = '{"visitorButtonClicked":true}'

button_press = requests.put('https://academic-ni.cloud.thingworx.com/Thingworx/Things/myWindow_billchurch/Properties/*', headers=headers, params=params, data=data, auth=('billchurch', '!ntern3t0fth1ngS'))
# print(button_press.headers)
# print(button_press.text)
# print(button_press.status_code)