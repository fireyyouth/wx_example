import redis
import time
import json
import requests

r = redis.Redis()

class MyException(Exception):
    pass

def init_menu():
    query = {'access_token' : r.get('access_token')}

    resp = requests.get('https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info', params=query)
    resp_data = resp.json()

    if resp_data['is_menu_open']:
        resp = requests.get('https://api.weixin.qq.com/cgi-bin/menu/delete', params=query)
        resp_data = resp.json()
        if resp_data['errcode'] != 0:
            raise MyException(resp_data['errmsg'])

    data = {
            'button' : [
                {
                    'type' : 'click',
                    'name' : '点一下',
                    'key' : 'JUST_A_CLICK'
                }
            ]
        }
    data_bytes = json.dumps(data, ensure_ascii=False).encode('utf-8')
    resp = requests.post('https://api.weixin.qq.com/cgi-bin/menu/create', params=query, data=data_bytes)
    resp_data = resp.json()
    if resp_data['errcode'] != 0:
        raise MyException(resp_data['errmsg'])



def update_token():
    query = {
	     'appid' :  'wxe84560561b0f888e',
	     'secret' : 'bda18749aab75900998f135a8d3d1d9b',
	     'grant_type' : 'client_credential'
	    }
    resp = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=query)
    resp_data = resp.json()
    r.set('access_token', resp_data['access_token'])
    r.set('access_token_expire_time', str(time.time() + resp_data['expires_in']))
    return resp_data['expires_in']

expires_in = update_token()
init_menu()
