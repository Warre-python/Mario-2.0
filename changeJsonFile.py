import json

old_path = 'levels/Warre.json'
new_path = 'levels/WarreNew.json'

with open(old_path, 'r') as file:
    data = json.load(file)
    