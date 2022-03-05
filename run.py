import os
import subprocess
from time import sleep
import argparse
from setup import setupEnvironment, updateSirhurt, fixClient, removeSirhurt, checkUpdates
import colorama
from colorama import Fore, Style
import configparser
config = configparser.ConfigParser()
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--update", required=False, help="Update Sirhurt's DLL", action="store_true")
ap.add_argument("-c", "--clear", required=False, help="Remove Sirhurt", action="store_true")
ap.add_argument("-f", "--fixclient", required=False, help="Fix Unexpected Client Error", action="store_true")
args = vars(ap.parse_args())


if args["clear"]:
    removeSirhurt()
    exit()

try:
    os.chdir("sirhurt")
except:
    print(Fore.RED + "SirHurt not found! Getting into configuration mode... " + Style.RESET_ALL)
    setupEnvironment()

try:
    config.read("TuxHurtConfig.ini")
except:
    print(Fore.RED + "Configuration files are corrupted! Getting into configuration mode... " + Style.RESET_ALL)
    setupEnvironment()

if args["fixclient"]:
    fixClient()
    exit()

if args["update"]:
    updateSirhurt()
    exit()

# Check for updates
checkUpdates()

def injectSirhurt():
    print(Fore.GREEN + "Detected attach. Injecting SirHurt..." + Style.RESET_ALL)
    subprocess.Popen(["env", f"WINEPREFIX={grapejuicePrefixPath}", f"{winePath + '/wine'}", "TuxHutInjector.exe"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def runSirhurt():
    # Set up the global paths
    global winePath
    global sirhurtPrefixPath
    global sirhurtPath
    global grapejuicePrefixPath
    winePath = config.get("DEFAULT", "winepath")
    sirhurtPrefixPath = config.get("DEFAULT", "sirhurtpath") + "/prefix"
    grapejuicePrefixPath = config.get("DEFAULT", "grapejuiceprefix")
    sirhurtPath = config.get("DEFAULT", "sirhurtpath")

    print(Fore.GREEN + "Running SirHurt..." + Style.RESET_ALL)
    # Kill the wineserver for other Sirhurt processes. This causes a problem when running the script multiple times.
    subprocess.Popen(["env", f"WINEPREFIX={sirhurtPrefixPath}", f"{winePath + '/wineserver'}", "-k"],
                                                                            stdout=subprocess.DEVNULL,
                                                                            stderr=subprocess.DEVNULL)
    # Run Sirhurt
    sirhurtProcess = subprocess.Popen(["env", f"WINEPREFIX={sirhurtPrefixPath}", f"{winePath + '/wine'}",
                                       "Sirhurt V4_New.exe"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    # Check for the attach output
    while True:
        realtime_output = sirhurtProcess.stdout.readline()
        if realtime_output == '' and sirhurtProcess.poll() is not None:
            break
        if realtime_output:
            if 'Attempting to attach' in realtime_output.strip().decode("utf-8"):
                injectSirhurt()
                sleep(1)

if __name__ == "__main__":
    runSirhurt()
