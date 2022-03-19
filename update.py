import subprocess
import os
import configparser
import argparse
import github
from colorama import Fore, Style
import datetime

config = configparser.ConfigParser()
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--force", required=False, help="Will force update even if you're running the latest version", action="store_true")
args = vars(ap.parse_args())

def updateScript(script):
    os.system(f"mv {script}.py {script}.py.backup")
    output = subprocess.run(f"wget -o {script}.py https://raw.githubusercontent.com/TuxHurt/TuxHurt/main/{script}.py".split(" "), capture_output=True)
    if output.stderr != b'SSL_INIT\n':
        print(Fore.RED + "There was an error while fetching the " + script + ".py script.\nReverting changes..." + Style.RESET_ALL)
        os.system(f"mv {script}.py.backup {script}.py")
    else:
        os.remove(f"{script}.py.backup")
        os.system(f"mv {script}.py.1 {script}.py")

def checkTuxUpdate(force=False):
    print(Fore.YELLOW + "Checking for TuxHurt updates..." + Style.RESET_ALL)
    g = github.Github()
    repo = g.get_repo("TuxHurt/TuxHurt")
    try:
        last_update = datetime.strptime(config.get("DEFAULT", "lastupdate"), '%d/%m/%y %H:%M:%S')
    except Exception:
        last_update = repo.pushed_at
        config.set("DEFAULT", "lastupdate", str(last_update))
    update = False
    if not force and repo.pushed_at > last_update:
        update = input(Fore.GREEN + "A new version of TuxHurt has been detected, would you like to update? [Y/n]: " + Style.RESET_ALL) not in 'no'
    elif repo.pushed_at == last_update:
        print(Fore.GREEN + "You're running the latest version!" + Style.RESET_ALL)
        if force:
            print(Fore.YELLOW + "Updating due to force flag..." + Style.RESET_ALL)
    if force:
        update = True
    if update:
        updateScript("run")
        updateScript("setup")

if __name__ == "__main__":
    checkTuxUpdate(args["force"])