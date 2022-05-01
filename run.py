#!/bin/python3

import os
import sys
import subprocess
import argparse
import configparser
import requests
import getch
import github
import datetime
import pwd
import json
from time import sleep, time
from colorama import Fore, Style

VERBOSE = False

TUX_CREDITS = f"""
{Fore.YELLOW}Tux{Fore.CYAN}Hurt{Fore.GREEN} is brought to you by:{Style.RESET_ALL}

{Fore.GREEN}- {Fore.MAGENTA}(Emilia) dsf001#1337 : {Fore.GREEN}Python scripts, Wine configuration{Style.RESET_ALL}
{Fore.GREEN}- {Fore.MAGENTA}(Cy) Cy#0730 : {Fore.GREEN}Injector, GitHub{Style.RESET_ALL}
{Fore.GREEN}- {Fore.MAGENTA}(Millie) woffle#1337 : {Fore.GREEN}Minor contributions{Style.RESET_ALL}
{Fore.YELLOW}And of course:{Style.RESET_ALL}")
{Fore.GREEN}- {Fore.MAGENTA}You! : {Fore.GREEN}Using SirHurt and our scripts!{Style.RESET_ALL}

{Fore.GREEN}Thank you for using {Fore.YELLOW}Tux{Fore.CYAN}Hurt{Fore.GREEN}. We hope you have a great time exploiting!{Style.RESET_ALL}

{Fore.YELLOW}Tux{Fore.CYAN}Hurt{Fore.BLUE} Discord:{Style.RESET_ALL} https://discord.gg/b8PGgMHpYX"
{Fore.YELLOW}Tux{Fore.CYAN}Hurt{Fore.WHITE} GitHub:{Style.RESET_ALL} https://github.com/TuxHurt/
"""

TUX_LICENSE = f"""{Fore.GREEN}
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License along with this program. If not,
"see <https://www.gnu.org/licenses/>.
{Style.RESET_ALL}
"""

print_yellow = lambda *_, **__: print(f"{Fore.YELLOW}{' '.join(_)}{Style.RESET_ALL}", **__)
print_green  = lambda *_, **__: print(f"{Fore.GREEN }{' '.join(_)}{Style.RESET_ALL}", **__)
print_red    = lambda *_, **__: print(f"{Fore.RED   }{' '.join(_)}{Style.RESET_ALL}", **__)

def get_user():
    """
    Get the user name of system
    """
    try:
        user = os.getlogin()
    except:
        user = pwd.getpwuid(os.geteuid())[0]
    return user

def check_packages():
    """
    Checks if you have all the required packages to run
    TuxHurt
    """
    print_yellow("Checking required packages...")
    required_packages = {"wine": False, "winetricks": False, "wget": False, "unzip": False}
    for i in required_packages:
        return_code = subprocess.run(i + " --version", shell=True, capture_output=True).returncode
        required_packages[i] = return_code == 10 or return_code == 0
    for package, installed in required_packages.items():
        if not installed:
            print_red(f"[NOT INSTALLED] {package}")
        else:
            print_green(f"[INSTALLED]     {package}")
    if sum(required_packages.values()) < len(required_packages):
        print_red("You don't have all the required packages to run TuxHurt, aborting.")
        exit(-1)

def print_credits():
    print(TUX_CREDITS)
    exit(0)

def print_license():
    print(TUX_LICENSE)
    exit(0)

def kill_wine_server():
    config = configparser.ConfigParser()
    config.read("sirhurt/TuxHurtConfig.ini")
    wine_path = config.get("DEFAULT", "wine_path")
    grapejuice_prefix_path = configparser.get("DEFAULT", "grapejuiceprefix")
    print_yellow("Killing the wineserver...")
    subprocess.Popen(
        [
            "env",
            f"WINEPREFIX={os.getcwd()}/sirhurt/prefix"
            f"{wine_path}/wineserver",
            "-k"
        ],
        stdout = sys.stdout if VERBOSE else subprocess.DEVNULL,
        stderr = sys.stderr if VERBOSE else subprocess.DEVNULL
    )
    subprocess.Popen(
        [
            "env",
            f"WINEPREFIX={grapejuice_prefix_path}"
            f"{wine_path}/wineserver",
            "-k"
        ],
        stdout = sys.stdout if VERBOSE else subprocess.DEVNULL,
        stderr = sys.stderr if VERBOSE else subprocess.DEVNULL
    )

def remove_sirhurt():
    """
    Removes the SirHurt directory created by TuxHurt
    """
    print_yellow("Removing SirHurt...")
    try:
        os.system("rm -rf sirhurt")
    except Exception as e:
        print_red("There was an error with the directory removal")
        if VERBOSE:
            print(e)

def fix_client():
    """
    Prevents the Roblox Client from running into unexpected issues
    caused by Exploiting
    """
    print_yellow("Fixing the Roblox Client...")
    config = configparser.ConfigParser()
    config.read("sirhurt/TuxHurtConfig.ini")
    grapejuice_prefix_path = config.get("DEFAULT", "grapejuiceprefix")
    try:
        os.remove(f"{grapejuice_prefix_path}/drive_c/users/{os.getlogin()}/AppData/Local/Roblox/GlobalBasicSettings_13.xml")
        print_green("Successfully removed GlobalBasicSettings_13.xml!")
    except Exception as e:
        print_red("Couldn't remove GlobalBasicSettings_13.xml")
        if VERBOSE:
            print(e)

def update_sirhurt():
    """
    Updates Sirhurt
    """
    print_yellow("Updating SirHurt...")
    config = configparser.ConfigParser()
    config.read("TuxHurtConfig.ini")
    try:
        response = requests.get("https://sirhurt.net/asshurt/update/v4/fetch_version.php")
        latest_version_name = requests.get("https://sirhurt.net/asshurt/update/v4/fetch_sirhurt_version.php")
        if response.status_code == 200:
            latest_version = response.text
            print_green("Got the URL")
            subprocess.run(["wget", "-O", "'SirHurt.dll'", str(latest_version), "-q", ">", "/dev/null", "2>&1"])
            if VERBOSE:
                print(f"Latest version: {latest_version_name.text}")
            config.set("DEFAULT", "currentversion", latest_version_name.text)
            with open("TuxHurtConfig.ini", "w") as configfile:
                config.write(configfile)
            print_green("SirHurt updated successfully!")
        else:
            raise Exception("Error while fetching the latest version!")
    except Exception as e:
        print_red("Could not connect to the Sirhurt server! Please report this to TuxHurt owners.")
        if VERBOSE:
            print(e)

def update_bootstrapper():
    """
    Updates using the bootstrapper
    """
    print_yellow("Updating SirHurt using bootstrapper")
    config = configparser.ConfigParser()
    config.read("TuxHurtConfig.ini")
    if VERBOSE:
        print(f"Current version: {config.get('DEFAULT', 'currentversion')}")
    try:
        wine_path = config.get("DEFAULT", "wine_path")
        sirhurt_prefix_path = config.get("DEFAULT", "sirhurtpath")
        subprocess.call(["env", f"WINEPREFIX={sirhurt_prefix_path}", f"{wine_path + '/wine'}", "Sirhurt V4 Bootstrapper.exe"],
            stdout = sys.stdout if VERBOSE else subprocess.DEVNULL,
            stderr = sys.stderr if VERBOSE else subprocess.DEVNULL)
        print_green("Successfully ran Bootstrapper! Please re-run the script.")
    except Exception as e:
        print_red("Could not run the Bootstrapper. Please report this incident to TuxHurt owners.")
        if VERBOSE:
            print(e)

def check_updates():
    """
    Checks if there are any SirHurt updates
    """
    print_yellow("Checking for SirHurt updates...")
    config = configparser.ConfigParser()
    config.read("sirhurt/TuxHurtConfig.ini")
    current_version = config.get("DEFAULT", "currentversion")
    latest_version = requests.get("https://sirhurt.net/asshurt/update/v4/fetch_sirhurt_version.php").text
    if current_version != latest_version:
        print_yellow("A Sirhurt update is detected, would you like to update? [Y/n]: ", end="", flush=True)
        update = getch.getche().lower()
        if update == "n":
            print_yellow("Skipping the update. SirHurt may not work with your current install.")
        else:
            update_sirhurt()
    
def update_script(script):
    """
    Updates a script from a specified repository
    """
    print(f"Updating {script}.py...", end="")
    os.system(f"mv {script}.py {script}.py.backup")
    output = subprocess.run(f"wget -o {script}.py https://raw.githubusercontent.com/TuxHurt/TuxHurt/main/{script}.py".split(" "), capture_output=True)
    if output.stderr != b'SSL_INIT\n':
        print(Fore.RED + "There was an error while fetching the " + script + ".py script.\nReverting changes..." + Style.RESET_ALL)
        os.system(f"mv {script}.py.backup {script}.py")
        os.remove(f"{script}.py.1")
    else:
        os.remove(f"{script}.py.backup")
        os.system(f"mv {script}.py.1 {script}.py")
        print(Fore.GREEN + "Success" + Style.RESET_ALL)

def check_tuxhurt_updates():
    """
    Checks if there are any changes made to the TuxHurt scripts
    """
    config = configparser.ConfigParser()
    config.read("sirhurt/TuxHurtConfig.ini")
    try:
        repo = config.get("DEFAULT", "repo")
    except Exception as e:
        config.set("DEFAULT", "repo", "TuxHurt/TuxHurt")
        repo = "TuxHurt/TuxHurt"
        if VERBOSE:
            print(e)
    print_yellow("Checking for TuxHurt updates...")
    g = github.Github()
    repo = g.get_repo(repo)
    try:
        last_update = datetime.datetime.strptime(config.get("DEFAULT", "lastupdate")[2:], '%y-%m-%d %H:%M:%S')
    except Exception as e:
        last_update = repo.pushed_at
        if VERBOSE:
            print(e)
    config.set("DEFAULT", "lastupdate", str(repo.pushed_at))
    update = False
    if repo.pushed_at > last_update:
        print_green("A new version of TuxHurt has been detected, would you like to update? [Y/n]: ", end="", flush=True)
        update = getch.getche().lower()
        if update == "n":
            print("\nSkipping update...")
        update = update == "" or update != "n"
    elif repo.pushed_at == last_update:
        print_green("You're running the latest version!")
    if update:
        update_script("run")
    with open("sirhurt/TuxHurtConfig.ini", "w") as configfile:
        config.write(configfile)

def check_grapejuice_config():
    """
    idfk this shit's needed to run
    """
    wine_path = ""
    with open(f"/home/{get_user()}/.config/brinkervii/grapejuice/user_settings.json") as f:
        grapejuice_user_config = json.loads(f.read())
    
    for prefix in grapejuice_user_config["wineprefixes"]:
        if prefix["name_on_disk"] == "player":
            wine_path = prefix["wine_home"] + "/bin/"
            print_green(f"Found: {wine_path}")
            return wine_path
    
    while wine_path == "":
        temp_path = input(f"{Fore.RED}Couldn't locate Wine installation direcory, please enter it manually: {Style.RESET_ALL}")
        print_yellow("Testing the wine path...")
        if os.path.isdir(temp_path) and os.path.isfile(temp_path + "/bin/wine") and os.path.isfile(temp_path + "/bin/wineserver"):
            print_green("Valid wine path!")
            return temp_path + "/bin/"
        else:
            print_red("Invalid wine path, try again.")

def inject_sirhurt(grapejuice_prefix_path, wine_path):
    """
    Injects SirHurt
    """
    print_green("Detected attach. Injecting SirHurt...")
    subprocess.Popen(["env", f"WINEPREFIX={grapejuice_prefix_path}", f"{wine_path + '/wine'}", "sirhurt/TuxHutInjector.exe"],
                      stdout = sys.stdout if VERBOSE else subprocess.DEVNULL,
                      stderr = sys.stderr if VERBOSE else subprocess.DEVNULL)

def setup_environment():
    """
    Sets everything up and creates config files
    """
    grapejuice_prefix_path = ""

    print_yellow("Searching the wine installation directory...")
    wine_path = check_grapejuice_config()

    if os.path.exists(f"/home/{get_user()}/.local/share/grapejuice/prefixes/player"):
        grapejuice_prefix_path = f"/home/{get_user()}/.local/share/grapejuice/prefixes/player"
    else:
        while True:
            grapejuice_prefix_path = input("Grapejuice prefix not found! Please enter the prefix manually: ")
            if not os.path.exists(grapejuice_prefix_path + "/drive_c"):
                print("The prefix you entered is invalid! Please enter a valid prefix!")
            else:
                break

    try:
        os.system("rm -rf sirhurt/*")
        if not os.path.exists("sirhurt"):
            os.mkdir("sirhurt")
    except Exception as e:
        print_red("There was an error with File System!")
        if VERBOSE:
            print(e)
        exit(-1)

    if not os.path.isfile("SirHurt V4.zip"):
        print_red("Sirhurt not found! Due to some problems with getting links and Sirhurt's TOS, you need to download the zip file yourself and put it here.")
        os.system("rm -rf sirhurt")
        exit(-1)
    
    print_yellow("Extracting SirHurt...")
    os.system("unzip 'SirHurt V4.zip' -d sirhurt" + ("" if VERBOSE else "> /dev/null 2>&1"))

    print_green("Downloading the injector...")
    os.system("wget -O sirhurt/TuxHutInjector.exe https://github.com/TuxHut/TuxHut/blob/main/TuxHutInjector.exe?raw=true" + ("" if VERBOSE else "> /dev/null 2>&1"))

    config = configparser.ConfigParser()
    config.read("sirhurt/TuxHurtConfig.ini")

    config.set("DEFAULT", "wine_path", wine_path)
    config.set("DEFAULT", "sirhurtpath", os.getcwd() + "/sirhurt")
    config.set("DEFAULT", "grapejuiceprefix", grapejuice_prefix_path)
    config.set("DEFAULT", "currentversion", requests.get("https://sirhurt.net/asshurt/update/v4/fetch_sirhurt_version.php").text)

    with open("sirhurt/TuxHurtConfig.ini", "w") as configfile:
        config.write(configfile)

    print_yellow("Creating the prefix now, please wait a while...")
    subprocess.call(["env", f"WINEPREFIX={os.getcwd()}/sirhurt/prefix", f"{wine_path}/wine", "wineboot"],
                     stdout = sys.stdout if VERBOSE else subprocess.DEVNULL,
                     stderr = sys.stderr if VERBOSE else subprocess.DEVNULL)

    print_yellow("Killing wineserver...")
    subprocess.Popen(["env", f"WINEPREFIX={os.getcwd()}/sirhurt/prefix", f"{wine_path + '/wineserver'}", "-k"],
                      stdout = sys.stdout if VERBOSE else subprocess.DEVNULL,
                      stderr = sys.stderr if VERBOSE else subprocess.DEVNULL)
    
    print_green("Installing redist...")
    subprocess.call(["env", f"WINEPREFIX={os.getcwd()}/sirhurt/prefix", "winetricks", "vcrun2015"],
                     stdout = sys.stdout if VERBOSE else subprocess.DEVNULL,
                     stderr = sys.stderr if VERBOSE else subprocess.DEVNULL)

def run_sirhurt():
    """
    Runs SirHurt
    """
    config = configparser.ConfigParser()
    config.read("sirhurt/TuxHurtConfig.ini")
    wine_path = config.get("DEFAULT", "wine_path")
    sirhurt_prefix_path = config.get("DEFAULT", "sirhurtpath") + "/prefix"
    grapejuice_prefix_path = config.get("DEFAULT", "grapejuiceprefix")
    print_green("Running SirHurt...")

    subprocess.Popen(["env", f"WINEPREFIX={sirhurt_prefix_path}", f"{wine_path + '/wineserver'}", "-k"],
                      stdout = sys.stdout if VERBOSE else subprocess.DEVNULL,
                      stderr = sys.stderr if VERBOSE else subprocess.DEVNULL)

    os.chdir("sirhurt")
    sirhurt_process = subprocess.Popen(["env", f"WINEPREFIX={sirhurt_prefix_path}", f"{wine_path + '/wine'}",
                                        "Sirhurt V4_New.exe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.chdir("..")

    last_output_time = time()

    check_last_output = lambda: time() - last_output_time > 5

    print_green("Started listening to SirHurt events")

    enable_checks = False
    while True:
        try:
            realtime_output = sirhurt_process.stdout.readline()
            if realtime_output == '' and sirhurt_process.poll() is not None:
                raise Exception

            if realtime_output:
                output = realtime_output.strip().decode("utf-8")
                if VERBOSE:
                    print(output)

                if "Attempting to attach" in output:
                    inject_sirhurt(grapejuice_prefix_path, wine_path)
                    sleep(1)

                if "RBX" in output:
                    enable_checks = True
                    last_output_time = time()

            if enable_checks:
                result = check_last_output()
                if result:
                    print_red("Detected Sirhurt exit.")
                    raise Exception
        except:
            print_yellow("Killing wineserver to exit SirHurt")
            subprocess.Popen(["env", f"WINEPREFIX={sirhurt_prefix_path}", f"{wine_path + '/wineserver'}", "-k"],
                             stdout=sys.stdout if VERBOSE else subprocess.DEVNULL,
                             stderr=sys.stderr if VERBOSE else subprocess.DEVNULL)
            print_green("Wineserver killed sucessfully, thanks for using TuxHurt.")
            exit(0)

def check_arguments():
    """
    Checks for any arguments passed to the program
    """
    global VERBOSE
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-u", "--update", required=False, help="Update Sirhurt's DLL", action="store_true")
    arg_parser.add_argument("-uu", "--updatebootstrapper", required=False, help="Update Sirhurt using Bootstrapper", action="store_true")
    arg_parser.add_argument("-c", "--clear", required=False, help="Remove Sirhurt", action="store_true")
    arg_parser.add_argument("-f", "--fixclient", required=False, help="Fix Unexpected Client Error", action="store_true")
    arg_parser.add_argument("-k", "--kill", required=False, help="Kills the wineserver for TuxHurt and Roblox", action="store_true")
    arg_parser.add_argument("-v", "--verbose", required=False, help="Spits out everything in an annoying way like Asia in DxD",  action="store_true")
    arg_parser.add_argument("-r", "--repository", nargs=1, required=False, help="Changes the repository where updates are pulled from")
    arg_parser.add_argument("--credits", required=False, help="Show credits for TuxHurt", action="store_true")
    arg_parser.add_argument("--license", required=False, help="Show the license for TuxHurt", action="store_true")

    args = vars(arg_parser.parse_args())

    VERBOSE = args["verbose"]
    
    if args["credits"]:
        print_credits()
    
    if args["license"]:
        print_license()
    
    if args["kill"]:
        kill_wine_server()

    if args["clear"]:
        remove_sirhurt()

    if args["fixclient"]:
        fix_client()

    if args["repository"]:
        config = configparser.ConfigParser()
        config.read("sirhurt/TuxHurtConfig.ini")
        config.set("DEFAULT", "repo", args["repository"][0])
        with open("TuxHurtConfig.ini", "w") as f:
            config.write(f)

    if args["update"]:
        update_sirhurt()
    
    if args["updatebootstrapper"]:
        update_bootstrapper()

def main():
    """
    Runs all the subfunctions which make up TuxHurt
    """

    if not os.path.exists("sirhurt/TuxHurtConfig.ini"):
        check_packages()
        setup_environment()
        print_green("Successfully set up environment, please re-run")
        exit(0)

    check_arguments()
    check_updates()
    check_tuxhurt_updates()
    run_sirhurt()

if __name__ == "__main__":
    if os.getcwd() != os.path.dirname(os.path.abspath(__file__)):
        # If ran from a different directory, we switch the directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()