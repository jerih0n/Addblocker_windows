import requests
import re
import subprocess, ctypes, sys
import uuid
from datetime import datetime

IP_ADDRESSES_GET_URL_ADDRESS = "https://pgl.yoyo.org/adservers/iplist.php"
IP_PATTERN = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'  # Regular expression for matching IPv4 addresses


def print_welcome():
        print("""" /~'$$$$$$$$$$$$$$$$$$$$$$\
    (    "$$$$$$$$$k\;\&j$$$$$$)
     |     "$$$$$$$,'    `^<$$$
     $$,     "$$$;' __n,    `;$
     $$$$,     "$$jT$$$$i. ,$$$
     '$$$$$,     "$$$$$$$;J$$$'
      $$$$$$$,     "$$$$$$$$$$
      '$$$$$$$$,     "$$$$$$$'
       '$$$$$$$$$,     "$$$$'
        '$$$$$$$$$$,     "$'
         '$$$$$$$$$$$,   /
          '$$$$$$$$$$$$/
            "$$$$$$$$$"
             '$$$$$$$'
               '"$$"
         Block those Adds!
         """)

def get_latest_ip_addresses() -> (bool, str):

    response = requests.get(IP_ADDRESSES_GET_URL_ADDRESS)
    try:
        if response.status_code != 200:
            print(f"Fetching IP address was NOT successful! \n Error Code: {response.status_code} \n Error Message: {response.text}")
            return False, ""
        return True, response.text

    except requests.RequestException as e:
        print(e)


def extract_ip_addresses(text_list) -> []:
    matches = re.findall(IP_PATTERN, text_list)
    return matches


def force_admin_mode():
    """ Force to start application with admin rights """
    try:
        isAdmin = ctypes.windll.shell32.IsUserAnAdmin()
    except AttributeError:
        isAdmin = False
    if not isAdmin:
        ctypes.windll.shell32.ShellExecuteW(None,
                                            "runas",
                                            sys.executable,
                                            __file__,
                                            None,
                                            1)

def is_rule_exist(rule_name) -> bool:
    find_command = f'netsh advfirewall firewall show rule name="{rule_name}"'
    try:
        result = subprocess.run(find_command, check=True, shell=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False


def create_firewall_setting_backup() -> True:
    try:
        new_guid = uuid.uuid4()
        guid = str(new_guid)
        current_datetime = datetime.now()
        command = f'netsh advfirewall export "FirewallSettings_backup_{guid}.wfw"'
        subprocess.run(command, check=True, shell=True)
        print("Firewall settings successfully created")
        return True

    except Exception as e:
        print("Firewall Settings Backup not created!")
        print(e)
        return  False


def add_firewall_restrictions(ip_addresses):

    if not create_firewall_setting_backup():
        return

    counter = 0
    for ip in ip_addresses:
        rule_name = f"addblocker-{ip}"

        try:
            if not is_rule_exist(rule_name):
                command = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip}'
                subprocess.run(command, check=True, shell=True)

                print(f"firewall rule {rule_name} blocking incoming traffic from {ip} created")

        except Exception as e:
            print(e)
            print(f"fire wall rule {rule_name} NOT created")

        counter = counter + 1
    print(f"Total {counter} new rules were created")

if __name__ == '__main__':
    print_welcome()
    force_admin_mode()
    isSuccess, context = get_latest_ip_addresses()

    if isSuccess:
        ip_addresses = extract_ip_addresses(context)
        add_firewall_restrictions(ip_addresses)


