# TuxHurt
  ![Github licence](https://img.shields.io/badge/license-GPLv3-green?style=flat-square)
  ![Platform](https://img.shields.io/badge/platform-GNU%2FLinux-green?style=flat-square)
  [![Discord](https://img.shields.io/badge/Discord-TuxHurt-blue?style=flat-square)](https://discord.gg/b8PGgMHpYX)
  
  ## Description 
  TuxHurt is the project that aims to run Sirhurt on GNU/Linux with 0 effort.

  ## Table of Contents
  * [Requirements](#requirements)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Injector](#injector)
  * [How to run SirHurt on GNU/Linux without TuxHurt](#how-to-run-sirhurt-on-gnulinux-without-tuxhurt)
  * [Security](#security)
  * [License](#license)
  * [Questions](#questions)
  * [Creators](#creators)
    
  ## Requirements
  Apart from the requirements.txt, this script makes heavy use of UNIX commands. Here are what you need:
  * A Valid SirHurt License
  * wget
  * unzip
  * winetricks
  
  (If you're using a beginner distro like Ubuntu, there's a high chance you already have those, except a SirHurt License of course.)
  
  ## Installation 
  Clone the repository with `git clone https://github.com/TuxHut/TuxHurt`<br/>
  Install the requirements with `pip3 install -r requirements.txt`<br/>
  Download Sirhurt from the website and put the .zip archive next to run and setup scripts(The archive must be named "SirHurt V4.zip").<br/>
  Run the run.py script. This may take a while for the first time.<br/>
  Note: The "SirHurt V4.zip" must look like [this](readmeassets/sirhurtzip.png). To get this zip file, use the mirror link from SirHurt's website(onedrive). <br/>

  ## Usage 
  You can simply use the `run.py` to run Sirhurt. It will automatically check updates for you too.<br/>
  `python3 run.py -h` to show help.<br/>
  `python3 run.py -u` to force update.<br/>
  `python3 run.py -uu` to update using Sirhurt Bootstrapper(Experimental).<br/>
  `python3 run.py -c` to remove Sirhurt. This may be a bit buggy so if it breaks, just delete the `sirhurt` directory by hand.<br/>
  `python3 run.py -f` to fix Unexpected Client Behavior in Roblox.<br/>
  `python3 run.py -k` to kill Roblox and Sirhurt.<br/>
  `python3 run.py -v` for verbose output. This is helpful when asking for help or diagnosing issues.<br/>
  `python3 run.py -r REPOSITORY` for changing the repository the script will update from. This is useful for forks.<br/>
  `python3 run.py --credits` for showing the credits.<br/>
  `python3 run.py --license` for showing the license of TuxHurt.<br/>
  
  ## Injector 
  TuxHurt uses an Injector called TuxHut that is made by the Owners of TuxHurt. It is a big part of TuxHurt's 0 effort goal.<br/>
  Read more about the Injector [here](https://github.com/TuxHurt/TuxHut)
  
  ## How to run SirHurt on GNU/Linux without TuxHurt
  If you would like to run SirHurt on GNU/Linux without TuxHurt, read a guide created by us [here](https://hentai.dsf001.site/notes/sirhurt.html).<br/>
  It's recommended to run SirHurt on GNU/Linux with TuxHurt.

  ## Security
  Cy found out that Roblox has some checks for Wine and GNU/Linux specifically. For this reason, we coded it in a way that it does not mess with Roblox and its Wine prefix. TuxHurt does not install itself to any directory except the project root and uninstalling the software is done by just deleting a directory.

  ## License 
  This project is licensed under GNU GPLv3

  ## Questions
  If you have any questions about this project, please contact us directly on [Discord](https://discord.gg/b8PGgMHpYX).

  ## Creators
  * Emilia "dsf001#1337" (Python scripts, Wine research)
  * Cy#0730 (Injector, Designs)
  * Millie "Millie<3#1337" (Updater)
  
<a href="https://github.com/orgs/TuxHurt/TuxHurt/main/">
    <img src="readmeassets/TuxHurtLogo.png" alt="Logo" width="160" height="140">
</a>
  
