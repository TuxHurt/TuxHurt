import subprocess
import os
import configparser
import argparse
import github
import datetime
import getch
from colorama import Fore, Style

config = configparser.ConfigParser()
config.read("sirhurt/TuxHurtConfig.ini")

def updateScript(script):
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

def checkTuxUpdate(manual=False, force=False):
    if not manual:
        os.chdir("..")
    config.read("sirhurt/TuxHurtConfig.ini")
    try:
        repo = config.get("DEFAULT", "repo")
    except Exception as e:
        config.set("DEFAULT", "repo", "TuxHurt/TuxHurt")
        repo = "TuxHurt/TuxHurt"
    print(Fore.YELLOW + "Checking for TuxHurt updates..." + Style.RESET_ALL)
    g = github.Github()
    repo = g.get_repo(repo)
    try:
        last_update = datetime.datetime.strptime(config.get("DEFAULT", "lastupdate")[2:], '%y-%m-%d %H:%M:%S')
    except Exception as e:
        last_update = repo.pushed_at
    config.set("DEFAULT", "lastupdate", str(repo.pushed_at))
    update = False
    last_update = datetime.datetime(20, 10, 10)
    if not force and repo.pushed_at > last_update:
        print(Fore.GREEN + "A new version of TuxHurt has been detected, would you like to update? [Y/n]: " + Style.RESET_ALL, end="", flush=True)
        update = getch.getche().lower()
        if update == "n":
            print(Fore.YELLOW + "\nSkipping update..." + Style.RESET_ALL)
        update = update == "" or update != "n"
    elif repo.pushed_at == last_update:
        print(Fore.GREEN + "You're running the latest version!" + Style.RESET_ALL)
        if force:
            print(Fore.YELLOW + "Updating due to force flag..." + Style.RESET_ALL)
    if force:
        update = True
    if update:
        updateScript("run")
        updateScript("setup")
        updateScript("update")
    with open("sirhurt/TuxHurtConfig.ini", "w+") as configfile:
        config.write(configfile)
    if not manual:
        os.chdir("sirhurt")

if __name__ == "__main__":
    checkTuxUpdate(True)