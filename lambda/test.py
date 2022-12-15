import spotipy
import spotipy.util as util
import common
import argparse
import random
import time
import threading



unhit_query_list = []

def get_random_search():
    """Get a random character of unicode.
    """

    rand_char = ''

    while rand_char == '':
        rand_char = chr(random.randint(0, 111411))

    random_search = ''

    if random.randint(0, 2) == 0:
        random_search = rand_char + '%'
    elif random.randint(0, 2) == 1:
        random_search = '%' + rand_char + '%'
    else:
        random_search = '%' + rand_char

    return random_search

def diggin_in_the_crate(num_tracks=10):
    """Search completely random songs.


    Args:
        num_tracks (int, optional): A number of tracks to add to playlist. Defaults to 30.
    """
    
    #secret = common.get_secret()
    username = "Hikaru"
    playlist_id = "07bihVSXGsycvuii4zNuMu"
    
    token = util.prompt_for_user_token(
        "Hikaru", 'playlist-read-private playlist-modify-public', "26c29a28d4dd4ded8990fc7ba06c7c57", "f408bc5e1d474a67a8c950ccb75c10f7", "http://localhost:8888/callback/")

    sp = spotipy.Spotify(auth=token)
    current_items = sp.playlist_items(playlist_id)

    if current_items['items']:
        remove_items = []

        for items in current_items['items']:
            remove_items.append(items['track']['uri'])

        sp.playlist_remove_all_occurrences_of_items(playlist_id, remove_items)
        print("Removed current songs.")

    # Get a list of country codes
    country_codes = sp.country_codes
    country_num = len(country_codes)

    track_ids = []
    count = 0
    query = ""

    print("Start searching...")

    # Add songs
    #while len(track_ids) < num_tracks:
    while count < 10:

        random_market = country_codes[random.randint(0, country_num - 1)]


        """Get a random character of unicode.
        """
        while True:
            query = get_random_search()
            if query in unhit_query_list:
                print("regenerate char")
            else: 
                break
     
        random_offset = random.randint(0, 999)

        results = sp.search(type='track', offset=random_offset,
                            limit=1, q=query, market=[random_market])

        if results is not None:
            if len(results['tracks']['items']) >= 1:
                print("song found!")
                count += 1
                pass

            else:
                print(query)
                unhit_query_list.append(query)
                print(len(unhit_query_list))
                diggin_in_the_crate()
            

    #f = open('output.txt', 'w', encoding='UTF-8')
    #f.writelines(unhit_query_list)
    #f.close()

    
def main():
    #thread = []
    #for i in range(1):
    #    thread.append(threading.Thread(target=diggin_in_the_crate))
    #    thread[i].start()
    diggin_in_the_crate()
    # todo


if __name__ == '__main__':
    main()
