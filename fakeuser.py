import requests

def fake_user():
    r = requests.get('https://api.randomuser.me/')
    return r.json()['results'][0]

def shows(r):
    print('Name:', r['name']['first'], r['name']['last'])
    print('Email:', r['email'])
    print('Username:', r['login']['username'])
    print('Password:', r['login']['password'])

if __name__ == '__main__':
    r = fake_user()
    shows(r)
