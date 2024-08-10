'''
Library for interacting with the PokeAPI.
https://pokeapi.co/
'''
import requests
import os
import image_lib

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    # Test out the get_pokemon_into() function
    # Use breakpoints to view returned dictionary
    poke_info = get_pokemon_info("Rockruff")
    download_pokemon_artwork('dugtrio', r'C:\temp')
    return

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    # Clean the Pokemon name parameter by:
    # - Converting to a string object,
    # - Removing leading and trailing whitespace, and
    # - Converting to all lowercase letters
    pokemon = str(pokemon).strip().lower()

    # Check if Pokemon name is an empty string
    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return

    # Send GET request for Pokemon info
    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    # Check if request was successful
    if resp_msg.status_code == requests.codes.ok:
        print('success')
        # Return dictionary of Pokemon info
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')

# TODO: Define function that gets a list of all Pokemon names from the PokeAPI
def get_pokemon_names(limit=100000, offset=0):
    print(f'Getting list of Pokemon names....', end='')
    params = {
        'limit': limit,
        'offset': offset
    }
    resp_msg = requests.get(POKE_API_URL, params=params)
    if resp_msg.status_code == requests.codes.ok:
        print('Success')
        resp_dict = resp_msg.json()
        return [p['name'] for p in resp_dict['results']]
    else:
        print('Failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')

def get_pokemon_image_url(pokemon_name):
    resp = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/')
    data = resp.json()
    image_url = data['sprites']['other']['official-artwork']['front_default']
    return image_url

# TODO: Define function that downloads and saves Pokemon artwork
def download_pokemon_artwork(pokemon_name, folder_path='.'):
    poke_info = get_pokemon_info(pokemon_name)
    if poke_info is None:
        return

    # Extract the artwork URL from the info dictionary
    artwork_url = poke_info['sprites']['other']['official-artwork']['front_default']
    if artwork_url is None:
        print(f"No artwork available for {pokemon_name.capitalize()}.")
        return

    # Determine the image file path
    file_ext = artwork_url.split('.')[-1]
    image_path = os.path.join(folder_path, f'{pokemon_name}.{file_ext}')

    # Don't download Pokemon artwork if there already exists one
    if os.path.exists(image_path):
        print(f"Artwork for {pokemon_name.capitalize()} already exists.")
        return image_path

    print(f'Downloading artwork for {pokemon_name.capitalize()}...', end='')
    image_data = image_lib.download_image(artwork_url)
    if image_data is None:
        return

    # Save the image file
    if image_lib.save_image_file(image_data, image_path):
        return image_path

if __name__ == '__main__':
    main()