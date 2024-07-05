# youtube-malicious-link-finder

<p align="center">
    <a href="" target="_blank"> 
        <img alt="license" src="https://img.shields.io/github/license/williamwith4ms/youtube-malicious-link-finder" />
    </a>
</p>

*** 
A tool for locating malicious links

## Features

- custom search terms
- automatic link extraction
- views both video descriptions and comments for links
- can ignore links that are deemed safe 

and more if i feel like adding it

## Quickstart guide 

First you need to get an api key for youtube. See https://developers.google.com/youtube/v3/getting-started

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

## Current planned features

- [x] inbuilt database querying
- [x] make usage guide
- [ ] improved processing
- [ ] easy way to add more links to the safe list
- [ ] lower false positive rate

these features are things i intend on adding, but i make no promises.