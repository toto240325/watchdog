import requests
r = requests.get('https://github.com/timeline.json')
print(r.text)
 
# The Requests library also comes with a built-in JSON decoder,
# just in case you have to deal with JSON data
 
import requests
r = requests.get('https://github.com/timeline.json')
print(r.json)
