import zulip
import pickle

def send_message(menu):

    msg = \
"**Lunch menu today ({})** \n\
* Menu I : {}\n\
* Menu II: {}\n\
* Special: {}".format(menu[0], menu[1], menu[2], menu[3])
    
    # Pass the path to your zuliprc file here.
    client = zulip.Client(config_file="zuliprc")
    
    ## Send a stream message
    request = {
        "type": "stream",
        "to": "lunch",
        "topic": "lunch menu",
        "content": msg,
    }
    result = client.send_message(request)
