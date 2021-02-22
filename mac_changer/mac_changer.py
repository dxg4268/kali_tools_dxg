"""Importing all the modules required"""
import optparse   #to accept command-line args
import subprocess #to run commands in terminal
import os         #to check for root access
import re         #to read output

#Creating object for OPT_PARSE class
parser = optparse.OptionParser()

#Check if User == ROOT
def check_root():
    if os.geteuid() != 0:
        return False
    else:
        return True

#Get info from $USER what they want from the program
def get_info():
    parser.add_option('-i', "--interface", dest="interface", help="Interface to change MAC Address.")
    parser.add_option('-m', "--mac", dest="new_mac", help="New MAC Address for the Interface.")

    (opt, arg) = parser.parse_args()

    interface = opt.interface
    new_mac = opt.new_mac
    if not interface:
        parser.error("[!]  => Please provide a Interface, use --help for more info...")
    elif not new_mac:
        parser.error("[!]  => Please provide a new MAC, use --help for more info...")
    else:
        return interface, new_mac

#This is the actual processing of the program
def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    # subprocess.call(["ifconfig", interface,])

#Execute Functions
def exec_program():
    root = check_root()
    if not root:
        exit("Err : ROOT Access required! Use 'ROOT' or 'sudo' program to run.\n[!] Exiting...")
    
    print("\n[+] ROOT Access granted!\n")

    interface, new_mac = get_info()

    current_mac = get_mac(interface, new_mac)
    print("[+] Current MAC => " + str(current_mac))

    print(f"\n[+] Changing MAC Address of {interface} to {new_mac}...\n")

    try:
        change_mac(interface, new_mac)
        # print("[+] Success!")
    except Exception as e:
        print("[!] Error Occured => " + e + "  :-(")

    current_mac = get_mac(interface, new_mac)
    if current_mac == new_mac:
        print("[+] MAC Changed Successfully to " + current_mac)
    else:
        print("[!] Sorry! Failed to Change MAC Address...     :-(")

def get_mac(interface, new_mac):

    mac_result_ifconfig = subprocess.check_output(["ifconfig", interface])
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(mac_result_ifconfig))

    if mac_result:
        return mac_result.group(0)
    else:
        print("[!] ERR => Could not read MAC! Exiting...")


#Start of the Program
exec_program()
