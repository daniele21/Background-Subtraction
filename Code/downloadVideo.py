# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 00:12:09 2019

@author: andre
"""

# START 15:28

#%%

import os
from datetime import datetime
import time
import urllib.request
import re

#%%
def timetostring():
    now = datetime.now()
    return '{}_{}_{}__{}_{}'.format(now.year, now.month, now.day, now.hour, now.minute)

#%%
    
downloads_folder = 'E:\Video'
download_every = 300 # seconds
check_every = 10 # seconds
index = 0

cam_ids = [ ('web0', 4311),
            ('web1', 1986),
            ('web2', 42),
            ('web3', 334),
            ('web4', 5601),
            ('web5', 5457),
            ('web6', 5271),
            ('web7', 5436),
            ('web8', 40),
            ('web9', 43),
            ('web10', 62),
            ('web11', 57),
            ('web12', 621),
            ('web13', 345), 
            ('web14', 354), 
            ('web15', 589),
            ('web16', 1226),
            ('web17', 4747),
            ('web18', 27),
            ('web19', 366),
            ('web20', 371)
          ]

prev_time = 0

request_prefix_url = 'https://www.autostrade.it/autostrade-gis/popupVideocam.do?tlc='
request_suffix_url = '&cq=LQM4&tipo=V'

if not os.path.isdir(downloads_folder):
    os.mkdir(downloads_folder)
    #os.makedirs(downloads_folder)

while True:
    t = time.time()
    if t >= prev_time + download_every:
        prev_time = t
        print('\n{}'.format(datetime.now()))

        n = 0
        for cam_id in cam_ids:
            resource_url = '{}{}{}'.format(request_prefix_url, cam_id[1], request_suffix_url)
            response = urllib.request.urlopen(resource_url)
            html = str(response.read())

            results = re.findall('(?<=<source src=")http://video\.autostrade\.it.*?(?=")',str(html), re.IGNORECASE)
            if len(results) > 0:
                video_url = results[0]
                folder_to_save = '{}/{}'.format(downloads_folder, cam_id[0])
                index_extended = '{0:04}'.format(index)
                name = 'video'+index_extended
                video_name = '{}.mp4'.format(name)
                if not os.path.isdir(folder_to_save):
                    os.mkdir(folder_to_save)
                path_to_save = '{}/{}'.format(folder_to_save, video_name)

                print('({}/{}) Downloading {} (cam_id: {})...'.format(n,len(cam_ids), cam_id[1], cam_id[0]), end='\t')
                urllib.request.urlretrieve(video_url, filename=path_to_save)
                print('ok')
            else:
                print('Cannot get video url from html:\n{}'.format(html))

            n+= 1
        print('Next download at {}'.format(datetime.fromtimestamp(t+download_every)))
        index += 1
    else:
        time.sleep(check_every)

