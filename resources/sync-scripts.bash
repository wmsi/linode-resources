#/usr/bin/env bash
set -e

# This script syncs any changes between github scripts
# and system-wide scripts so that updates can easily be
# synced.

# Mckenna Cisler <mckennacisler@gmail.com>

BACKUP_DIR="home/webpics/script-backup/"
RSYNC_ARGS="-av --backup-dir $BACKUP_DIR"

read -p "Proceed with syncing all changes between all config scripts? 
(the newest changes will be the ones kept) [y/n] " answer
if [ "$answer" == "Y" ] || [ "$answer" == "y" ]; then

    rsync $RSYNC_ARGS uploader/move-uploads.py /home/webpics/uploads/move-uploads.py
    rsync $RSYNC_ARGS uploader/update-all-galleries.py /home/webpics/uploads/update-all-galleries.py
    rsync $RSYNC_ARGS uploader/thumbsup-global-config.json /home/webpics/uploads/thumbsup-global-config.json
    
    # this one may never be done; it's a general purpose script
    #rsync $RSYNC_ARGS uploader/make-dir.py /var/www/html/wmsinh.org/public_html/make-dir.py
    
    echo "Finished"
    echo "(If something went wrong copying, check out $BACKUP_DIR)"
    
else 
    echo "Aborting..."
fi
