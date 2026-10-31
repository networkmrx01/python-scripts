import subprocess
import argparse
import re

def get_arguments():
    parser = argparse.ArgumentParser(description="A script to change the MAC address of a network interface.")
    parser.add_argument("-i", "--interface", dest="interface", required=True, help="Interface name (e.g., eth0, wlan0)")
    parser.add_argument("-m", "--mac", dest="new_mac", required=True, help="New MAC address (e.g., 00:11:22:33:44:55)")
    return parser.parse_args()

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    
    # Disable the interface
    subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
    # Change the hardware/ethernet address
    subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac], check=True)
    # Re-enable the interface
    subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)

def verify_mac(interface):
    ifconfig_result = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
    # Search for standard MAC address patterns in the output
    mac_address_search = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", ifconfig_result.stdout)
    
    if mac_address_search:
        return mac_address_search.group(0)
    else:
        print("[-] Could not read the MAC address.")
        return None

if __name__ == "__main__":
    args = get_arguments()
    
    current_mac = verify_mac(args.interface)
    print(f"[*] Current MAC: {current_mac}")
    
    try:
        change_mac(args.interface, args.new_mac)
    except subprocess.CalledProcessError:
        print("[-] Failed to change MAC address. Make sure you have sudo privileges.")
        exit(1)
        
    updated_mac = verify_mac(args.interface)
    if updated_mac == args.new_mac:
        print(f"[+] MAC address successfully changed to {updated_mac}")
    else:
        print("[-] MAC address did not change.")
