import requests

url = "http://web.jarvisoj.com:32774/"
headers = {
    'x-forwarded-for': '127.0.0.1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}
r = requests.get(url, headers=headers)
print r.text
