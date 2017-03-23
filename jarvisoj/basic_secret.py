import requests

r = requests.get('http://web.jarvisoj.com:32776/')

print r.headers['secret']
