import os
import sys
import configparser
from subprocess import call
import requests
import json

SETTINGS_INI = "check_seafile.ini"

parent_dir = os.path.dirname(__file__)

config_file = os.path.join(parent_dir, SETTINGS_INI)
if(not os.path.exists(config_file)):
    sys.exit("Could not find config file \"{}\"".format(config_file))
parser = configparser.ConfigParser()
parser.read(config_file)
seafile_user = parser.get("seafile", "seafile_user")
seafile_root_dir = parser.get("seafile", "seafile_root_dir")
if (not os.path.isdir(seafile_root_dir)):
    sys.exit("Could not find seafile installation under standard path \"{}\". Please supply the value in \"{}\"".format(SETTINGS_INI, config_file))
hass_token = parser.get("hass", "hass_token")
hass_url = parser.get("hass", "hass_url")


def setHassSensor(value, token, url):
    """Set the value of the Homeassistant Sensor"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"state": value}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(response)
    if response.status_code in [200, 201]:
        return True
    else:
        return False

if __name__ == "__main__":
    fsck_result_file = os.path.join(parent_dir, 'seafile_fsck_result.txt')
    # Execute seaf-fsck and save the output to fsck_result_file
    call("su " + seafile_user + " -c '" + seafile_root_dir + "/seafile-server-latest/seaf-fsck.sh'>" + fsck_result_file, shell=True)
    # If there is the word "commit" in the file it means some library is corrupted.
    # ->Send a notification and upload the file
    if 'commit' in open(fsck_result_file).read():
        success = setHassSensor("off", hass_token, hass_url)
        if not success:
            print("Failed to set Hass Sensor")
    else:
        success = setHassSensor("on", hass_token, hass_url)
        if not success:
            print("Failed to set Hass Sensor")
