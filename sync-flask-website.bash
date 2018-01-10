#/usr/bin/env bash
set -e

# This script copies changes made to the deployed
# flask application into this git repo.
# This allows developers to modify the website on the
# fly and then pull those changes back to this git repo
# so they can be committed. 

# This script is a companion to ./deploy-flask-website.bash, 
# which updates (deploys) the production version from this git repo.

# Mckenna Cisler <mckennacisler@gmail.com>

DEPLOY_DIREC="/var/www/html/wmsinh.org/public_html/flask"

echo "######################## !!! WARNING !!! #########################"
echo "This script will overwrite any changes to the github website!"
echo "Make sure you commit, stash, or branch those changes if you want "
echo "to keep them later!"
echo "######################## !!! WARNING !!! #########################"
echo


echo "Deploy directory to copy here: $DEPLOY_DIREC"
echo

read -p "Proceed with overwriting github site with deployed version? [y/n] " answer
if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then

    echo "Copying deploy location to ./flask ..."
    echo "cp -a $DEPLOY_DIREC/* ./flask/"
    cp -a $DEPLOY_DIREC/* ./flask/
    
    echo "Finished"
    
else 
    echo "Aborting..."
fi
