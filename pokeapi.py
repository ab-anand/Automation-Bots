import requests

# Documentation of pokedata:
# http://pokeapi.co/docsv2/#pokemon-section

def poke_request(pokemon):
    url = "http://pokeapi.co/api/v2/pokemon/"
    response  = requests.get(url + pokemon)
    poke_data = {}

    if response.ok:
        data = response.json()
        poke_data['Name'] = data['name'][0].upper() + data['name'][1:]
        poke_data['ID'] = data['id']
        poke_data['Height'] = str(data['height']/10) + " m"
        poke_data['Weight'] = str(data['weight']/10) + " kg"
        img_url = data['forms'][0]['url']
        poke_data['img'] = image_request(img_url)

        # if poke_data:
        #     for key in poke_data.keys():
        #         print("{}: {}".format(key, poke_data[key]))
        return poke_data

    else:
        print("Bad conection, try again later.")
        return None

def image_request(url):
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data['sprites']['front_default']

if __name__ == '__main__':
    # This is a test:
    pokemon = "pikachu"
    pd = poke_request(pokemon)
    print(pd)
