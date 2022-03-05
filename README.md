# TuxHurt
  ![Github licence](https://upload.wikimedia.org/wikipedia/commons/9/93/GPLv3_Logo.svg)

  
  ## Description 
  <a href="https://github.com/orgs/TuxHurt/TuxHurt/main/">
    <img src="readmeassets/TuxHurtLogo.png" alt="Logo" width="160" height="120">
  </a>
  TuxHurt is the project that aims to run Sirhurt on GNU/Linux with 0 effort.

  ## Table of Contents
  * [Installation](#installation)
  * [Usage](#usage)
  * [Injector](#injector)
  * [License](#license)
  * [Questions](#questions)
  * [Requirements](#requirements)
  * [Creators](#creators)
  
  ## Installation 
  Clone the repository with `git clone https://github.com/TuxHut/TuxHurt`
  Install the requirements with `pip3 -r requirements.txt`
  Download Sirhurt from the website and put the .zip archive next to run and setup scripts(The archive must be named "SirHurt V4.zip").
  Run the run.py script. This may take a while for the first time.

  ## Usage 
  You can simply use the `run.py` to run Sirhurt. It will automatically check updates for you too.
  `python3 run.py -u` to force update.
  `python3 run.py -c` to remove Sirhurt. This may be a bit buggy so if it breaks, just delete the `sirhurt` directory by hand.
  `python3 run.py -f` to fix Unexpected Client Behavior in Roblox.
  
  ## Injector 
  TuxHurt uses an Injector called TuxHut that is made by the Owners of TuxHurt. It is a big part of TuxHurt's 0 effort goal. Read more about the Injector here:       https://github.com/TuxHut/TuxHut

  ## License 
  This project is licensed under GNU GPLv3

  ## Questions
  If you have any questions about this project, please contact us directly on [Discord](https://discord.gg/b8PGgMHpYX).
  
  ## Requirements
  Apart from the requirements.txt, this script makes heavy use of UNIX commands. Here are what you need:
  * wget
  * unzip
  * winetricks
  
  (If you're using a beginner distro like Ubuntu, there's a high chance you already have those)
  
  ## Creators
  * Emilia(Python scripts, Wine research)
  * Cy#0730(Injector, Designs)
  
