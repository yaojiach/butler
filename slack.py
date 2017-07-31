import configparser
import time
from slackclient import SlackClient
from db import LiteDB

config = configparser.ConfigParser()
config.read('slack.conf')
ACCESS_TOKEN = config['default']['bot_token']
BOT_ID = config['default']['bot_id']
BOT_NAME = config['default']['bot_name']
WEBSOC_DELAY = 1

slackc = SlackClient(ACCESS_TOKEN)

# check bot id
req = slackc.api_call('users.list')
if req.get('ok'):
    users = req.get('members')
    chk_bot_id = [u['id'] for u in users 
                  if 'name' in u and u.get('name') == BOT_NAME]
    chk_bot_id = chk_bot_id[0]
    if BOT_ID == '':
        BOT_ID = chk_bot_id

BOT_CALL = '<@{bid}>'.format(bid=BOT_ID)

def handler(cmd, chn):
    resp = 'All I can say is that it\'s a bouillon spoon'
    kw = ['water', 'temperature', 'ready']
    if any(w in cmd for w in kw):
        ldb = LiteDB()
        d = ldb.get_one()
        resp = 'Last time I checked ({ts}), it was {st}'.format(ts=d['ts'], 
                                                                st=d['st'])
    slackc.api_call('chat.postMessage', as_user=True,
                    channel=chn, text=resp)

def parser(rtm):
    res = (None, None)
    if isinstance(rtm, list) and len(rtm) > 0:
        rtm = rtm[0]
        txt = rtm.get('text')
        if txt:
            if BOT_CALL in txt:
                txt = txt.split(BOT_CALL)[1].strip().lower()
                chn = rtm.get('channel')
                res = (txt, chn)
    return res

if __name__ == '__main__':
    if slackc.rtm_connect():
        while True:
            cmd, chn = parser(slackc.rtm_read())
            if cmd and chn:
                handler(cmd, chn)
            time.sleep(WEBSOC_DELAY)
    else:
        print('Invalid token or bot id')

