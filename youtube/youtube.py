#!/usr/bin/env python

#
# Reads a csv file of artist,title pairs and then hunts through
# YouTube looking for those videos. If it finds them, it adds them
# to a custom playlist.
#
# Useful for making video playlists from your spotify playlists.
#
# Based on the Google provided sample code for creating a playlist.
#

import httplib2
import os
import unicodecsv
import sys
import re

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

def youtube_create_playlist(options):
  playlists_insert_response=youtube.playlists().insert(
    part="snippet,status",
    body=dict(
      snippet=dict(
        title=options.playlistName,
        description="Playlist automatically generated by panda"
       ),
      status=dict(
        privacyStatus="private"
       )
     )
   ).execute()
  
  return playlists_insert_response["id"]

def youtube_add_to_playlist(playlistId, videoId):
  add_video_response = youtube.playlistItems().insert(
    part="snippet",
    body=dict(
      snippet=dict(
        playlistId=playlistId,
        resourceId=dict(
          kind="youtube#video",
          videoId=videoId
        )
      )
    )
  ).execute()

  return add_video_response

def youtube_search(options):
  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.query,
    part="id,snippet",
    maxResults=1,
    type="video",
    order="relevance"
  ).execute()

  videos = []

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"], search_result["id"]["videoId"]))
      return search_result["id"]["videoId"]

  return ""

#
# Main
#

if __name__ == "__main__":
  argparser.add_argument("--playlist", help="Playlist to import", default="Starred.csv")
  args = argparser.parse_args()

  try:
    playlistName = re.search ('^(.*).csv$', args.playlist).group(1)
    playlistName = "Spotify - " + playlistName
  except AttributeError:
    print "Couldn't determinate playlist name from %s\n" % args.playlist

  print "Using '%s' as playlist name for YouTube\n" % playlistName
  args.playlistName = playlistName
  
  try:
    playlistId = youtube_create_playlist(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
    sys.exit (1)
    
  try:
    # Read all of the videos we have from our source file,
    # search for them and if we find a match then add it to
    # our list of video ids.
    videoIds = []
    with open(args.playlist, 'rb') as sources:
      reader = unicodecsv.DictReader(sources)
      for row in reader:
        args.query = row['Artist'] + " " + row['Title']
        vid = youtube_search(args)
        if vid:
          videoIds.append ("%s" % vid)
          print "Found video %s (%s)" % (args.query, vid)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

  # Now loop through all of our video ids we've saved
  # and add them to the our playlist
  for videoId in videoIds:
    try:
      success = youtube_add_to_playlist(playlistId, videoId)['kind'] == 'youtube#playlistItem'
      print "Added video %s to playlist %s" % (videoId, playlistId)
    except Exception as e:
      print "Failed to add %s to playlist" % videoId
