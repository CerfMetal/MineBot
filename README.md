#####
![Build](https://img.shields.io/badge/Build-passing-brightgreen)
![Version](https://img.shields.io/badge/Version-1.1-red)
[![License: GPL-3.0-License](https://img.shields.io/badge/License-GPL--3.0--License-yellow)](https://opensource.org/licenses/GPL-3.0)
[![Download : setup.sh](https://img.shields.io/badge/Download-setup.sh-blue)](https://github.com/CerfMetal/Minecraft-Discord-Bot/archive/refs/heads/setup.zip)

# MineBot

MineBot is a Python Discord bot made to control and give information on your Minecraft server on linux or macOS.

## Installation

Download the [```setup.sh```](https://github.com/CerfMetal/Minecraft-Discord-Bot/tree/setup) shell script and run it using these commands :
```shell
chmod a+x setup.sh
./setup.sh
```
(You might need to use sudo for both commands)
#####
This script will download all the necessary packages and python modules in addtion to the discord bot.
#####

## Discord bot

To create your discord bot, you can follow this link to the [discord.py documentation](https://discordpy.readthedocs.io/en/latest/discord.html).
#####
Then add the discord bot to your discord server.

## Usage

You'll need to edit the config.yaml file to customise your discord bot.
#####
Copy your bot's token and paste it after ```DiscordToken :```.
#####
In the ```server.properties``` file, set ```enable-query``` to true .
#####
You can then run the python script using ```screen -S MineBot -d -m python3 MineBot.py```.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU General Public License v3.0](https://opensource.org/licenses/GPL-3.0)

## Download
[Download the setup.sh script](https://github.com/CerfMetal/Minecraft-Discord-Bot/archive/refs/heads/setup.zip)
#####
[Download the discord bot](https://github.com/CerfMetal/Minecraft-Discord-Bot/archive/refs/heads/main.zip)

## More info on GNU Screen
[Screen](https://www.gnu.org/software/screen/) is a full-screen window manager that multiplexes a physical terminal between several processes, typically interactive shells.

MineBot uses this software to create "virtual terminals" that will each run a certain process (minecraft server, ip tunnel...).
#####
To access the minecraft server console, you'll need to perform this command : 
```shell
screen -r <ScreenPrefix>
```
Where you replace ```ScreenPrefix``` by the ScreenPrefix's value in the config.yaml file.
