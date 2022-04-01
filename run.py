import os
import subprocess
from time import sleep
import argparse
from setup import setupEnvironment, updateSirhurt, fixClient, removeSirhurt, checkUpdates, updateConfig
from colorama import Fore, Style
import configparser
import time
import asyncio
from update import checkTuxUpdate

def checkPackages():
    print(Fore.YELLOW + "Checking required packages..." + Style.RESET_ALL)
    required_packages = {"wine":False, "winetricks":False, "wget":False, "unzip":False}
    for i in required_packages:
        o = subprocess.run(i + " --version", shell=True, capture_output=True)
        required_packages[i] = str(o.returncode) in "10"
    need_packages = False
    for i in required_packages:
        if not required_packages[i]:
            need_packages = True
            print(Fore.RED + f"Package '{i}' [NOT INSTALLED]", Style.RESET_ALL)
        else:
            print(Fore.GREEN + f"Package '{i}' [INSTALLED]", Style.RESET_ALL)
    if need_packages:
        print(Fore.RED + "You need all the above packages for TuxHurt to run, please install them using your os' package manager." + Style.RESET_ALL)
        quit()

config = configparser.ConfigParser()
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--update", required=False, help="Update Sirhurt's DLL", action="store_true")
ap.add_argument("-c", "--clear", required=False, help="Remove Sirhurt", action="store_true")
ap.add_argument("-f", "--fixclient", required=False, help="Fix Unexpected Client Error", action="store_true")
ap.add_argument("-v", "--verbose", required=False, help="Spits out everything in an annoying way like Asia in DxD", action="store_true")
ap.add_argument("-r", "--repository", nargs=1, required=False, help="Changes the repository where updates are pulled from")

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
    checkPackages()
    print(Fore.RED + "SirHurt not found! Getting into configuration mode..." + Style.RESET_ALL)
    if verbose:
        setupEnvironment(verbose=True)
    else:
        setupEnvironment()

if args["repository"]:
    config.set("DEFAULT", "repo", args["repository"][0])
    with open("TuxHurtConfig.ini", "w") as f:
        config.write(f)

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
    print(Fore.GREEN + "Started listening to Sirhurt events" + Style.RESET_ALL)
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
    # Check for required packages
    checkPackages()
    # Check for updates
    checkUpdates()
    # Check for TuxHurt updates
    checkTuxUpdate()
    # Run Sirhurt
    runSirhurt()
