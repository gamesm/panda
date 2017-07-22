#!/usr/bin/env python

#
# Grabs a user's playlists and their contents.
# Takes the returned data and spits it out into a CSV file
# named after the playlist name.
# Requires authentication via oauth.
#
# Based on Spotify's own example code for retrieving playlists.
#

import unicodecsv
import sys
import os
import spotipy
import spotipy.util as util

def show_tracks(results):
  for i, item in enumerate(tracks['items']):
    track = item['track']
    print("%d %s %s" % (i, track['artists'][0]['name'], track['name']))

def write_tracks (results):
  for i, item in enumerate (tracks['items']):
    track = item['track']

  tracks = sp.next(tracks)
        
if __name__ == '__main__':
  if len(sys.argv) > 1:
    username = sys.argv[1]
  else:
    print("usage: python spotify.py [username]")
    sys.exit()

  token = util.prompt_for_user_token(username)

  if token:
    sp = spotipy.Spotify(auth=token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
      if playlist['owner']['id'] == username:
        name = playlist['name']
        results = sp.user_playlist(username, playlist['id'], fields="tracks,next")
        tracks = results['tracks']

        playlistCsv = open (name.strip() + ".csv", 'wt')

        try:
          writer = unicodecsv.writer (playlistCsv, encoding='utf-8', quoting=unicodecsv.QUOTE_ALL)
          writer.writerow ( ('Artist', 'Title') )
          while True:
            for i, item in enumerate(tracks['items']):
              track = item['track']
              artist = track['artists'][0]['name']
              trackName = track['name']

              writer.writerow ( (artist, trackName) )
              
            if not tracks['next']:
              break
            tracks = sp.next(tracks)
        finally:
          playlistCsv.close()
          
  else:
    print("Can't get token for", username)
