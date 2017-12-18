#!/bin/bash
# this script will eventually be executed regularly by cron
# Move uploaded images into the right subdomain and build/ update a gallery for them

# iterate over directories in the uploads folder

# split each one around the '-' to get a pair of subdomain and Album Name

# move each album into the gallery-source folder of the correct subdomain

# if the subdomain doesn't exist either create it or keep the files here

# build a gallery with the images in gallery-source