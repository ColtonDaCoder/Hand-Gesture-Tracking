import json
with open('gestures.json', 'w') as file:
    json.dump([{"name": "run", "landmarks": {1: [0, 0, 0]}}], file, indent=4, separators=(',',': '))