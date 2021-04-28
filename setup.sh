#setup.sh
sudo apt-get update  # Install the latest package lists
sudo apt-get install python3.6 -y # Install python 3
sudo apt-get install python3-pip -y # Install PIP for python3
sudo apt-get install screen -y # Install the screen package (used to create virtual terminals)
sudo apt-get install wget -y # Install the wget package (used to download the MineBot)
sudo apt-get install unzip -y # Install the unzip package (used to unzip the MineBot)

# Install all the necessary package for the minecraft discord bot
pip3 install discord.py
pip3 install asyncio
pip3 install mcstatus
pip3 install pyyaml 
pip3 install spontit
pip3 install requests

wget https://github.com/CerfMetal/Minecraft-Discord-Bot/archive/refs/heads/main.zip # Download the discord bot's files
unzip main.zip
rm main.zip

