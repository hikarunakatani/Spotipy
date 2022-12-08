import spotipy
import spotipy.util as util
import common
import argparse
import random

username = 'Hikaru'


def diggin_in_the_crate(num_tracks=30):
    """Executes searching completely random songs.


    Args:
        num_tracks (int, optional): A number of tracks to add to playlist. Defaults to 30.
    """

    sp = common.authenticate()

    playlist_id = '07bihVSXGsycvuii4zNuMu'

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
    track_name = ''
    track_artists = []

    print("Start searching...")

    # Add songs
    while len(track_ids) < num_tracks:

        random_market = country_codes[random.randint(0, country_num - 1)]

        query = common.get_random_search()

        randomOffset = random.randint(0, 999)

        results = sp.search(type='track', offset=randomOffset,
                            limit=1, q=query, market=[random_market])

        if results is None:
            print('NoneType')

        else:
            if len(results['tracks']['items']) >= 1:
                track_name = results['tracks']['items'][0]['name']

                # When there are multiple artists
                if len(results['tracks']['items'][0]['artists']) >= 2:
                    for artist in results['tracks']['items'][0]['artists']:
                        track_artists.append(artist['name'])
                else:
                    track_artists.append(
                        results['tracks']['items'][0]['artists'][0]['name'])

                # idを格納
                track_ids.append((results['tracks']['items'][0]['id']))
                print('Added {} - {} to the playlist.'.format(track_name,
                      ','.join(track_artists)))
                track_artists.clear()

            else:
                pass

    sp.user_playlist_add_tracks(username, playlist_id, track_ids)
    print("Updated playlist.")


def playback_song(song_name):
    sp = common.authenticate()

    devices = sp.devices()
    for device in devices['devices']:
        if device['name'] == 'LAPTOP-Q6UU6C1V':
            device_id = device['id']

    songname = song_name

    results = sp.search(type='track',
                        limit=1, q=songname)

    track_uri = results['tracks']['items'][0]['uri']
    sp.start_playback(device_id, uris=[track_uri])


def invoked_process():
    """Fucntion to execute when invoked from lambda handler
    """
    diggin_in_the_crate(1)


def main():
    """ main function for local testing
    """

    parser = argparse.ArgumentParser(
        description='This program is for manipulating Spotify using SpotifyAPI.')

    parser.add_argument('function', help='specify a function to use')

    parser.add_argument('--num_tracks', type=int,
                        help='a number of songs to add')

    parser.add_argument('--song_name', type=str,
                        help='a name of song to seach')

    args = parser.parse_args()

    if args.function == 'ditc':
        if args.num_tracks:
            diggin_in_the_crate(args.num_tracks)
        else:
            diggin_in_the_crate()

    elif args.function == 'playback_song' and args.song_name:
        playback_song(args.song_name)

    else:
        print("please specify the fucntion name properly.")
    # todo


if __name__ == '__main__':
    main()
