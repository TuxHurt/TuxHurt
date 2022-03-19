import os
import subprocess
from time import sleep
import argparse
from setup import setupEnvironment, updateSirhurt, fixClient, removeSirhurt, checkUpdates, updateConfig
from colorama import Fore, Style
import configparser
import time
import asyncio

config = configparser.ConfigParser()
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--update", required=False, help="Update Sirhurt's DLL", action="store_true")
ap.add_argument("-c", "--clear", required=False, help="Remove Sirhurt", action="store_true")
ap.add_argument("-f", "--fixclient", required=False, help="Fix Unexpected Client Error", action="store_true")
ap.add_argument("-v", "--verbose", required=False, help="Spits out everything in an annoying way like Asia in DxD",
                action="store_true")

args = vars(ap.parse_args())
verbose = args["verbose"]
if args["clear"]:
    removeSirhurt()
    exit()

if args["fixclient"]:
    fixClient()
    exit()

try:
    os.chdir("sirhurt")
    config.read("TuxHurtConfig.ini")
except:
    print(Fore.RED + "SirHurt not found! Getting into configuration mode..." + Style.RESET_ALL)
    if verbose:
        setupEnvironment(verbose=True)
    else:
        setupEnvironment()

if args["update"]:
    if verbose:
        updateSirhurt(verbose=True)
    else:
        updateSirhurt()
    os.chdir("..")
    updateConfig()
    exit()


# Run the injector
def injectSirhurt():
    print(Fore.GREEN + "Detected attach. Injecting SirHurt..." + Style.RESET_ALL)
    if verbose:
        subprocess.Popen(["env", f"WINEPREFIX={grapejuicePrefixPath}", f"{winePath + '/wine'}", "TuxHutInjector.exe"])
    else:
        subprocess.Popen(["env", f"WINEPREFIX={grapejuicePrefixPath}", f"{winePath + '/wine'}", "TuxHutInjector.exe"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


lastOutputTime = time.time()


async def checkLastOutput():
    global lastOutputTime
    if time.time() - lastOutputTime > 5:
        return True


def runSirhurt():
    # Set up the global paths
    global winePath
    global sirhurtPrefixPath
    global sirhurtPath
    global grapejuicePrefixPath
    global lastOutputTime
    winePath = config.get("DEFAULT", "winepath")
    sirhurtPrefixPath = config.get("DEFAULT", "sirhurtpath") + "/prefix"
    grapejuicePrefixPath = config.get("DEFAULT", "grapejuiceprefix")
    sirhurtPath = config.get("DEFAULT", "sirhurtpath")

    print(Fore.GREEN + "Running SirHurt..." + Style.RESET_ALL)

    # Kill the wineserver for other Sirhurt processes. This causes a problem when running the script multiple times.
    if verbose:
        subprocess.Popen(["env", f"WINEPREFIX={sirhurtPrefixPath}", f"{winePath + '/wineserver'}", "-k"])
    else:
        subprocess.Popen(["env", f"WINEPREFIX={sirhurtPrefixPath}", f"{winePath + '/wineserver'}", "-k"],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    # Run Sirhurt
    sirhurt_process = subprocess.Popen(["env", f"WINEPREFIX={sirhurtPrefixPath}", f"{winePath + '/wine'}",
                                        "Sirhurt V4_New.exe"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    enableChecks = False
    # Check for the attach output
    print(Fore.GREEN + "Started listening Sirhurt events" + Style.RESET_ALL)
    while True:
        try:
            realtime_output = sirhurt_process.stdout.readline()
            if realtime_output == '' and sirhurt_process.poll() is not None:
                raise KeyboardInterrupt

            if realtime_output:
                output = realtime_output.strip().decode("utf-8")
                if verbose:
                    print(output)

                if 'Attempting to attach' in output:
                    injectSirhurt()
                    sleep(1)

                if "RBX" in output:
                    enableChecks = True
                    lastOutputTime = time.time()

            if enableChecks:
                result = asyncio.run(checkLastOutput())
                if result:
                    print(
                        Fore.RED + "Detected Sirhurt exit." + Style.RESET_ALL)
                    raise KeyboardInterrupt

        except KeyboardInterrupt:
            print(Fore.YELLOW + "Killing wineserver to exit Sirhurt..." + Style.RESET_ALL)
            if verbose:
                subprocess.Popen(["env", f"WINEPREFIX={sirhurtPrefixPath}", f"{winePath + '/wineserver'}", "-k"])
            else:
                subprocess.Popen(["env", f"WINEPREFIX={sirhurtPrefixPath}", f"{winePath + '/wineserver'}", "-k"],
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
            print(Fore.GREEN + "Wineserver killed successfully! Thank you for using TuxHurt." + Style.RESET_ALL)
            exit()


if __name__ == "__main__":
    # Check for updates
    checkUpdates()
    # Run Sirhurt
    runSirhurt()
