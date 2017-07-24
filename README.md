# Panda project

Panda is a collection of python scripts for reading Spotify playlists
and the creating YouTube playlists from those.

## Why?

I wanted to learn python and I wanted to watch music videos of my Spotify
playlists, so what better way then creating a couple of small scripts to
do just that.

There isn't anything spectacular here, both the YouTube and Spotify scripts
are based heavilly on the the example documentation provided by both sites.

## Setup

You will need to create Spotify and YouTube developer accounts to obtain
the required developer credentials to make these scripts work.

### Spotify

You will need the following libraries to use this script,
1. unicodecsv
2. spotipy

See [Spotify](https://developer.spotify.com/my-applications/#!/applications)
for information on how to create your developer account and assign an ID to
this script for use.

Then you will need to set,
~~~~
  SPOTIPY_CLIENT_ID=''
  SPOTIPY_CLIENT_SECRET=''
  SPOTIPY_REDIRECT_URI=''
~~~~
on the command line to match what is set in your developer details for this
application.

### YouTube

You will need the following libraries to use this script,
1. httplib2
2. unicodecsv

You will also need to authorise the YouTube python script to have access to
your account. See [YouTube Authorization](https://developers.google.com/youtube/v3/guides/authentication) for more information.

You will also need to create a project via the Google Cloud Platform and
add the YouTube API to that project.

From there, you will be able to download the client_secrets.json file from the
Credentials page and place it into the same directory as the youtube.py
script.

## Usage

### Spotify

If configured correctly, running,

~~~~
$> python spotify.py your_spotify_username
~~~~

will open a browser window for you to allow access to your account for this
script. If you proceed, you will be redirected to a URL. It won't matter that
the URL will fail to load, you simply need to paste that URL into the console
where you run the spotify.py script from.

After a few moments there will be CSV files in that directory containing
all of your spotify playlists. These can then be copied over to the youtube
directory for processing by that script.

### Youtube

If configured correctly, running,

~~~~
$> python youtube.py --playlist name_of_playlist.csv
~~~~

will result in output showing which video files were found and added to the
new playlist.

