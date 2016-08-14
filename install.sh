sudo cp scaleiot /etc/init.d/
sudo chmod +x /etc/init.d/scaleiot
sudo update-rc.d scaleiot defaults

git update-index --assume-unchanged web/data.json
