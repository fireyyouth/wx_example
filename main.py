from flask import Flask, request
import xml.etree.ElementTree as ET
import hashlib
import time
from pprint import pprint

app = Flask(__name__)

def check_wx_msg(token, ts, nonce, sig):
    data = sorted([token, ts, nonce])
    m = hashlib.sha1()
    for s in data:
        m.update(s.encode())
    return sig == m.hexdigest()


def dict_from_xml(xml_str):
    root = ET.fromstring(xml_str)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

def xml_from_dict(msg):
    root = ET.Element('xml')
    for k, v in msg.items():
        ET.SubElement(root, k).text = v
    return ET.tostring(root)


@app.route('/', methods=['GET', 'POST'])
def index():
    WX_TOKEN = 'fireyyouth'
    if not check_wx_msg(WX_TOKEN, request.args.get('timestamp', ''), request.args.get('nonce', ''), request.args.get('signature', '')):
        return 'fuck you hacker'

    if 'echostr' in request.args:
        return request.args['echostr']

    req_msg = dict_from_xml(request.data)
    pprint(req_msg)

    resp_msg = {
            'ToUserName' : req_msg['FromUserName'],
            'FromUserName' : req_msg['ToUserName'],
            'CreateTime' : str(int(time.time())),
            'MsgType' : 'text',
            'Content' : 'it works bastard!'
            }

    if req_msg['MsgType'] == 'event':
        resp_msg['Content'] = 'you send %s event' % req_msg['EventKey']

    return xml_from_dict(resp_msg)

app.run('0.0.0.0', 80)

