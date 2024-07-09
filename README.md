# youtube-malicious-link-finder

<p align="center">
    <a href="https://github.com/williamwith4ms/youtube-malicious-link-finder/blob/main/LICENSE" target="_blank"> 
        <img alt="license" src="https://img.shields.io/github/license/williamwith4ms/youtube-malicious-link-finder" />
    </a>
    <a href="https://github.com/williamwith4ms/youtube-malicious-link-finder/releases" target="_blank">
        <img alt="release" src="https://img.shields.io/github/v/release/williamwith4ms/youtube-malicious-link-finder?include_prereleases">
</p>

*** 
A tool for locating malicious links on youtube.com

## Features

- custom search terms
- automatic link extraction
- views both video descriptions and comments for links
- can ignore links that are deemed safe 

And more if I feel like adding it!

## Quickstart guide 

Ensure you have python and pip installed, on linux use the package manager and on windows. See https://www.python.org/downloads/

Then install the requirements 
```
pip install -r requirements.txt
```

Them you need to get an api key for youtube. See https://developers.google.com/youtube/v3/getting-started

Then set the api key as an environment variable

Bash/zsh
```
export YOUTUBE_API_KEY='YOUR KEY HERE'
```
Fish
```
set -x YOUTUBE_API_KEY 'YOUR KEY HERE'
```

you should see your key printed if you run
```
echo $YOUTUBE_API_KEY
```

run run.py and select `4. Create Database` then `1. Automated` to initialize the database

## Cron jobs

The file src/cron.py is a slimed version of run.py that contains only what is needed to run and process a search. At this point in time changing the options requires editing the file manually, However it is quite clear what needs to be changed.

After changing the options run the crontab command

In this example the script will run once every hour 
```
0 * * * * /path/to/python /path/to/cron.py
```

In this example the script will run once every day at 1PM 
```
0 13 * * * /path/to/python /path/to/cron.py
```


## Current planned features / Todo

- [x] inbuilt database querying
- [x] make usage guide
- [ ] improved processing
- [ ] easy way to add more links to the safe list
- [ ] inbuilt way to set up API key 
- [ ] lower false positive rate
- [ ] AUR package

These features are things I intend on adding, but I make no promises.