#/usr/bin/env bash
set -e

# This script deploys the flask web application code to 
# the correct directory on our production linode server.
# This allows developers to easily mess around with the 
# code on their own machines and then log on to the 
# server, pull their changes, and deploy them from here
# to the production location.

# This script is a companion to ./sync-flask-website.bash, 
# which updates this git repo with production changes

# Mckenna Cisler <mckennacisler@gmail.com>

DEPLOY_DIREC="/var/www/html/wmsinh.org/public_html/flask"

echo "######################## !!! WARNING !!! #########################"
echo "This script will overwrite any changes to production website!"
echo "If you want to merge those changes with Github's, create a temp "
echo "branch, run the ./sync-flask-website.bash to pull them over here,"
echo "and then merge that branch with master to merge those changes."
echo "######################## !!! WARNING !!! #########################"
echo

echo "Deploy directory to overwrite: $DEPLOY_DIREC"
echo

read -p "Proceed with overwriting deployed flask site with github version? [y/n] " answer
if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then

    echo "Copying ./flask to deploy location..."
    echo "mkdir -p $DEPLOY_DIREC"
    mkdir -p $DEPLOY_DIREC
    echo "cp -a ./flask/* $DEPLOY_DIREC/"
    cp -a ./flask/* $DEPLOY_DIREC/
    
    echo "Finished"
    
else 
    echo "Aborting..."
    exit 
fi

echo

read -p "Would you like to restart Apache as well? 
(you'll need to have sudo privleges) [y/n] " answer
if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then
    echo "Restarting apache..."
    echo "sudo systemctl restart apache2"
    sudo systemctl restart apache2
else 
    echo "Okay, run 'sudo systemctl restart apache2' if you want to"
fi
