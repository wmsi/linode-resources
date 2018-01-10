#/usr/bin/env bash
set -e

# This script syncs any changes between github scripts
# and system-wide scripts so that updates can easily be
# synced.

# Mckenna Cisler <mckennacisler@gmail.com>

RSYNC_ARGS="-av --backup-dir /home/webpics/script-backup/"

read -p "Proceed with syncing all changes between all config scripts? 
(the newest changes will be the ones kept) [y/n] " answer
if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then

    rsync $RSYNC_ARGS uploader/move-uploads.py /home/webpics/uploads/move-uploads.py
    rsync $RSYNC_ARGS uploader/update-all-galleries.py /home/webpics/uploads/update-all-galleries.py
    
    # this one may never be done; it's a general purpose script
    #rsync $RSYNC_ARGS uploader/make-dir.py /var/www/html/wmsinh.org/public_html/make-dir.py
    
    echo "Finished"
    
else 
    echo "Aborting..."
fi
