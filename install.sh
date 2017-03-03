# Set up ScaleIoT service
sudo cp scaleiot /etc/init.d/
sudo chmod +x /etc/init.d/scaleiot
sudo update-rc.d scaleiot defaults

# Remove data and keys from git tracking
git update-index --assume-unchanged web/data.json
git update-index --assume-unchanged src/ifttt.py

# Set up cron backup of data.json (just in case)
mkdir /home/pi/Backup
cronline="0 0 * * * cp /home/pi/ScaleIoT/web/data.json /home/pi/Backup"
(crontab -l; echo "$cronline" ) | crontab -
