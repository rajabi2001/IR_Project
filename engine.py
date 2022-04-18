

import json
from hazm import *


with open("IR_data_news_10.json") as f:
    data = f.read()
jsondata = json.loads(data)
