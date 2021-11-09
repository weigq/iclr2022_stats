#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
html_data = requests.get('https://openreview.net/group?id=ICLR.cc/2022/Conference', headers=headers)
html_data.encoding = 'utf-8'

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(str(html_data.text))

soup = BeautifulSoup(html_data.text, 'html.parser')
with open('index_.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
