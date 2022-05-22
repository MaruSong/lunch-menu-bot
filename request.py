# This file send a request with Cookies to access to the lunch menu pdf

import os
import requests
from requests.structures import CaseInsensitiveDict

def request(cookiefile):
    url = "https://max.mpg.de/sites/fkf/Current-Information/Documents/gourmet_compagnie_Speiseplan_EN.pdf"
    
    headers = CaseInsensitiveDict()
    with open(cookiefile, "r") as f:
        cookie = f.read().replace('\n', '')
    
    headers["Cookie"] = cookie
    
    resp = requests.get(url, headers=headers)
    
    if resp.content == b'403 FORBIDDEN':
        raise AssertionError()
    
    filename = "menu_data/menu.pdf"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(resp.content)
