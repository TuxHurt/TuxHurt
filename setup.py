import os
import configparser
import subprocess
from colorama import Fore, Style
import requests


def getUser():
    # Get the user name of system
    user = os.getlogin()
    return user


def setupEnvironment():
    grapejuicePrefixPath = ""
    winepath = ""
    user = getUser()
    # I don't know if there can be multiple wine installations in this location. This may cause errors later but is
    # easy to fix. Please create an issue if this is the case.
    print(Fore.YELLOW + "Searching the wine installation directory..." + Style.RESET_ALL)
    for file in os.listdir(f"/home/{user}/.local/share/grapejuice/user/wine-download/"):
        if file.startswith("wine-tkg"):
            print(Fore.GREEN + "Found: " + Fore.CYAN + file + Style.RESET_ALL)
            winepath = f"/home/{user}/.local/share/grapejuice/user/wine-download/" + file + "/bin/"
        else:
            print("Wine build for Grapejuice not found! Please reinstall Grapejuice!")
            exit()
        break

    if os.path.exists(f"/home/{user}/.local/share/grapejuice/prefixes/player"):
        grapejuicePrefixPath = f"/home/{user}/.local/share/grapejuice/prefixes/player"
    else:
        while True:
            grapejuicePrefixPath = input("Grapejuice prefix not found! Please enter the prefix manually: ")
            # Check if "drive_c" directory exists in grapejuicePrefixPath
            if not os.path.exists(grapejuicePrefixPath + "/drive_c"):
                print("The prefix you entered is not valid! Please enter a valid prefix!")
            else:
                break

    # Delete the "sirhurt" directory in script directory
    try:
        os.system("rm -rf sirhurt/*")
        if not os.path.exists("sirhurt"):
            os.mkdir("sirhurt")
    except:
        print("There was an error with File System!")
        exit()
    # Links here will be changed later
    # Download the injector
    print(Fore.GREEN + "Downloading the files..." + Style.RESET_ALL)
    os.chdir("sirhurt")
    os.system("wget -O TuxHutInjector.exe https://github.com/TuxHut/TuxHut/blob/main/TuxHutInjector.exe?raw=true -q  > /dev/null 2>&1")

    # Check if Sirhurt V4.zip is here
    if not os.path.exists("../SirHurt V4.zip"):
        if not os.path.exists("SirHurt V4.zip"):
            print(Fore.RED + "Sirhurt not found! Due to some problems with getting links and Sirhurt's TOS, "
                             "you need to download the zip file yourself and put it here." + Style.RESET_ALL)
            os.chdir("..")
            os.system("rm -rf sirhurt")
            exit()
    else:
        os.system("mv '../SirHurt V4.zip' 'SirHurt V4.zip'")

    # Unzip Sirhurt
    os.system("unzip 'SirHurt V4.zip' > /dev/null 2>&1")
    # Open TuxHurtConfig.ini
    config = configparser.ConfigParser()
    config.read("TuxHurtConfig.ini")
    # write the necessary values to TuxHurtConfig.ini
    config.set("DEFAULT", "winepath", winepath)
    config.set("DEFAULT", "sirhurtpath", os.getcwd())
    config.set("DEFAULT", "grapejuiceprefix", grapejuicePrefixPath)
    currentVersion = requests.get("https://sirhurt.net/asshurt/update/v4/fetch_sirhurt_version.php").text
    config.set("DEFAULT", "currentversion", currentVersion)
    # Write the config file
    with open("TuxHurtConfig.ini", "w") as configfile:
        config.write(configfile)

    print(Fore.YELLOW + "Creating the prefix now. Please wait a while..." + Style.RESET_ALL)
    # Run wine with environment variable WINEPREFIX
    subprocess.call(["env", f"WINEPREFIX={os.getcwd()}/prefix", f"{winepath}/wine", "wineboot"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)

    # Kill the wineserver to avoid conflicts
    print(Fore.YELLOW + "Killing the wineserver..." + Style.RESET_ALL)
    subprocess.Popen(["env", f"WINEPREFIX={os.getcwd()}/prefix", f"{winepath+'/wineserver'}", "-k"],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)

    print(Fore.GREEN + "Installing redist..." + Style.RESET_ALL)
    subprocess.call(["env", f"WINEPREFIX={os.getcwd()}/prefix", "winetricks", "vcrun2015"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)

    print(Fore.GREEN + "Done! Please re-run the run.py script!" + Style.RESET_ALL)
    exit()


def updateSirhurt():
    print(Fore.YELLOW + "Updating Sirhurt..." + Style.RESET_ALL)
    config = configparser.ConfigParser()
    config.read("TuxHurtConfig.ini")
    # Get the latest DLL version
    try:
        response = requests.get("https://sirhurt.net/asshurt/update/v4/fetch_version.php")
        latestVersionName = requests.get("https://sirhurt.net/asshurt/update/v4/fetch_sirhurt_version.php")
        if response.status_code == 200:
            latestVersion = response.text
            print(Fore.GREEN + "Got the update URL!" + Style.RESET_ALL)
            #os.chdir("sirhurt")
            os.system(f"wget -O 'SirHurt.dll' {latestVersion} -q  > /dev/null 2>&1")
            config.set("DEFAULT", "currentversion", latestVersionName.text)
            # Save the config
            with open("TuxHurtConfig.ini", "w") as configfile:
                config.write(configfile)
            print(Fore.GREEN + "Sirhurt updated successfully!" + Style.RESET_ALL)
        else:
            raise Exception("Error while fetching the latest version!")

    except:
        print(
            Fore.RED + "Could not connect to the Sirhurt server! Please report this to TuxHurt owners." + Style.RESET_ALL)


def removeSirhurt():
    print(Fore.YELLOW + "Removing Sirhurt..." + Style.RESET_ALL)
    # Delete the "sirhurt" directory in script directory
    try:
        os.system("rm -rf sirhurt")
        print(Fore.GREEN + "Sirhurt has been removed successfully! To remove the scripts, simply delete them from "
                           "your file manager." + Style.RESET_ALL)
    except:
        print("There was an error with File System!")
        exit()


def fixClient():
    # The Roblox client fix is easy, simply delete that file.
    os.chdir("sirhurt")
    print(Fore.YELLOW + "Fixing the Roblox client..." + Style.RESET_ALL)
    config = configparser.ConfigParser()
    config.read("TuxHurtConfig.ini")
    grapejuicePrefixPath = config.get("DEFAULT", "grapejuiceprefix")
    try:
        os.system(
            f"rm {grapejuicePrefixPath}/drive_c/users/{os.getlogin()}/AppData/Local/Roblox/GlobalBasicSettings_13.xml")
        print(Fore.GREEN + "Successfully removed GlobalBasicSettings_13.xml!" + Style.RESET_ALL)
    except:
        print(Fore.RED + "Could not remove the GlobalBasicSettings_13.xml file!" + Style.RESET_ALL)


def checkUpdates():
    print(Fore.YELLOW + "Checking for updates..." + Style.RESET_ALL)
    config = configparser.ConfigParser()
    config.read("TuxHurtConfig.ini")
    currentVersion = config.get("DEFAULT", "currentversion")
    # Get the latest version and compare them
    latestVersion = requests.get("https://sirhurt.net/asshurt/update/v4/fetch_sirhurt_version.php").text
    if currentVersion != latestVersion:
        question = input(Fore.YELLOW + "A Sirhurt update is detected. Do you want to perform an update? [Y/n]: " + Style.RESET_ALL).lower()
        no = {'no', 'n'}
        if question in no:
            print(Fore.YELLOW + "Skipping the update. Please note that Sirhurt may not work with your current version." + Style.RESET_ALL)
            return False
        else:
            updateSirhurt()

if __name__ == "__main__":
    print(Fore.RED + "This script is not meant to run from the command line! Please run 'run.py' instead." + Style.RESET_ALL)
    exit()