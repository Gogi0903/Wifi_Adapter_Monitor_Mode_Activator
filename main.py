import re
import subprocess
import argparse


def change(interface):
    print(f"[+] {interface} módjának megváltoztatása monitor mode-ra.")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["airmon-ng", "check", "kill"])
    print(f"[+] Internet hozzáférés deaktiválva")
    subprocess.call(["iwconfig", interface, "mode", "monitor"])
    subprocess.call(["ifconfig", interface, "up"])


def get_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', dest='interface', help='Ez a wifi adapter lesz monitor mode-ba állítva.')
    option = parser.parse_args()
    if not option.interface:
        parser.error('[-] Az interface deklarálása kötelező.')
    return option


def get_current_mode(interface):
    iwconfig_result = subprocess.check_output(["iwconfig", interface])
    pattern = "Mode:Monitor"
    adapter_search_result = re.search(pattern, iwconfig_result.decode('utf-8'))
    if adapter_search_result:
        return adapter_search_result.group(0)
    else:
        return 'Mode:Managed'


argument = get_argument()

try:
    current_mode = get_current_mode(argument.interface)
    print(f"Jelenlegi mód: {current_mode}")
    change(argument.interface)
    current_mode = get_current_mode(argument.interface)

    if "Monitor" in current_mode:
        print(f'[+] Az adapter mode sikeresen megváltozott Monitor-ra.\nJelenlegi mód: {current_mode}')
    else:
        print('[-] Monitor mode aktiválása sikertelen.')
except subprocess.CalledProcessError:
    print("[-] Nem létező adapter.")
