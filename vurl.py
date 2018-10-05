import requests
import argparse

def shortener(link):
    r = requests.get('http://vurl.com/api.php?url={}'.format(link))
    return r.text

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--links",
                        help="Links to shorten.",
                        nargs='+',
                        type=str, required=True)
    args = parser.parse_args()
    for i in args.links:
        try:
            shortened_link = shortener(i)
        except:
            shortened_link = 'ERROR'
        if len(i) > 30:
            print('{:<34} - {}'.format(i[:30]+'...', shortened_link))
        else:
            print('{:<34} - {}'.format(i[:30], shortened_link))
