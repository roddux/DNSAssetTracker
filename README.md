# DNS Asset Tracker

## What?
Track assets using DNS, a python script using DNSLib and responding to requests
based on an inbuilt asset list.

## Why?
"Also it's a pain trying to work out who's laptop Nessus has scanned"

## How?
Run the server:

    $ python DNSAssetTracker.py &> assetRequests.log &

Test the server:

    $ dig @asset.tracker.server "abox" +short

Use the server easily:

    $ alias whohas='dig @asset.tracker.server +short'
