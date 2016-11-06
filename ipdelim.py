## f = open('proxylist.csv','r')
## file_text = f.readlines()
## for line in file_text:
##    print '"' + line.strip() + '"' + ','
from multiprocessing import Pool, Lock, Manager
import multiprocessing
import time
import urllib
import requests
import sys
import random
import os
from requests.exceptions import ConnectTimeout
from requests.exceptions import ReadTimeout
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ProxyError
from requests.exceptions import ConnectionError
from requests.exceptions import ContentDecodingError
from requests.exceptions import TooManyRedirects
from functools import partial
from bs4 import BeautifulSoup
import re
from functools import partial
from tqdm import *
import datetime
import settings 


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}

def get_proxy():
    ports = ['8080','80','3128','8888','81']
    proxlst = []
    proxyipport =[]	
	
    for port in tqdm(ports):
        url = 'http://gatherproxy.com/embed/?t=Elite&p=' + port + '&c='
        while True:
            try: 
		response = requests.get(url, headers=headers,  timeout = (1,5))
		break
            except: print "Something wrong grabbing proxies"
                
        html = response.content
        soup = BeautifulSoup(html,'html.parser')
        try:
            proxlstraw = soup.find_all('script',attrs={'type':'text/javascript'})
            proxlstraw = soup.find_all('script',attrs={'type':'text/javascript'})[3:len(proxlstraw)-3]
        except: print "Something wrong during scriping proxies from gatherproxy"
            
        
        for proxraw in proxlstraw:
            proxraw = unicode(proxraw.string).strip()
            beg = '"PROXY_IP":"'
            end = '","PROXY_LAST_UPDATE":'
            try:
                proxclean =  proxraw[proxraw.index(beg)+len(beg):proxraw.index(end)] + ':' + port
		proxyipport.append(proxclean)
            except: print "proxclean not properly read: Error arising from get_proxy()"
    f = open('proxies.txt', 'w')
    for proxy in proxyipport:
	f.write(proxy + '\n')
    f.close()
    return proxyipport

