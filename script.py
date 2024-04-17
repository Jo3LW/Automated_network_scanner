import subprocess 
import socket
import ipaddress
import getpass

# ANSI escape codes for colors
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def generate_banner():
    banner = f"""
{Color.HEADER}               *******************************************************
               *                                                     *
               *{Color.BLUE}        Welcome to ScaNet (Network Scanner) !        {Color.HEADER}*
               *                                                     *
               *{Color.WARNING}    Warning: This tool is intended for educational   {Color.HEADER}*
               *{Color.WARNING}                    purposes only!                   {Color.HEADER}*
               *                                                     *
               *{Color.BLUE}  https://github.com/Jo3LW/Automated_network_scanner {Color.HEADER}*
               *                                                     *
               *******************************************************{Color.ENDC}
"""
    print(banner)


def initial_scanning_options(network_range, sudo_password):

    while True:
        option = input(f"{Color.BLUE}Please choose an option for network scanning:\n" + 
                f"{Color.GREEN}1) Discover devices in the sub-network (Device name, IP Address, MAC Address)\n" +
                f"{Color.GREEN}2) Discover devices in the sub-network (Device name, IP Address, MAC Address, Open Ports)\n" +
                f"{Color.GREEN}3) Discover devices in the sub-network (Device name, IP Address, MAC Address, Operating System)\n" +
                f"{Color.GREEN}4) Discover devices in the sub-network (Device name, IP Address, MAC Address, Open Ports and services)\n" +
                f"{Color.FAIL}5) Exit\n" +
                f"\nEnter your choice: {Color.ENDC}")

        if option == "1":
            print(f"{Color.GREEN}Option 1 selected\n{Color.ENDC}")
            scan_network(network_range, sudo_password, 1)
        elif option == "2":
            print(f"{Color.GREEN}Option 2 selected{Color.ENDC}")
            scan_network(network_range, sudo_password, 2)
        elif option == "3":
            print(f"{Color.GREEN}Option 3 selected{Color.ENDC}")
            scan_network(network_range, sudo_password, 3)
        elif option == "4":
            print(f"{Color.GREEN}Option 4 selected{Color.ENDC}")
            scan_network(network_range, sudo_password, 4)
        elif option == "5":
            print(f"{Color.FAIL}Exiting the program{Color.ENDC}")
            return
        else:
            print(f"{Color.FAIL}Invalid option selected{Color.ENDC}")
            initial_scanning_options(network_range, sudo_password)


def find_subnet_range(ip, subnet_mask="24"):
    network_obj = ipaddress.ip_network(f"{ip}/{subnet_mask}", strict=False)
    return network_obj


def scan_network(network_range, sudo_password, case):
    result = None

    if case == 1:
        command = f"echo '{sudo_password}' | sudo -S nmap -sn {network_range}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if case == 2:
        command = f"echo '{sudo_password}' | sudo nmap -p- {network_range}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if case == 3:
        command = f"echo '{sudo_password}' | sudo nmap -O {network_range}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if case == 4:
        command = f"echo '{sudo_password}' | sudo nmap -sV {network_range}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    print (result.stdout)


def main():
    generate_banner()

    sudo_password = ""
    ip_address = None
    device_name = socket.gethostname()
    try: 
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        ip_address = local_ip
    except Exception as error:
        print("Error:", error)
        return

    print(f"{Color.BLUE}Your Device Name: {device_name}")
    print(f"Your IP Address: {ip_address}{Color.ENDC}")
    print("\n")



    # Hide the password input
    sudo_password = getpass.getpass(prompt=f"{Color.GREEN}Please enter your sudo password: {Color.ENDC}")


    network_range = find_subnet_range(ip_address)
    initial_scanning_options(network_range, sudo_password)


if __name__ == "__main__":
    main()
