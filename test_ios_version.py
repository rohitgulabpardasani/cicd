import yaml
from netmiko import ConnectHandler
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

def load_devices():
    """Loads device credentials from devices.yaml."""
    try:
        with open("devices.yaml", "r") as file:
            data = yaml.safe_load(file)
            if "devices" not in data:
                raise KeyError("Missing 'devices' key in YAML file")
            return data["devices"]
    except yaml.YAMLError as e:
        print(Fore.RED + f"❌ YAML Parsing Error: {e}")
        exit(1)

def get_ios_version(device):
    """
    Connects to a Cisco IOS-XE or IOS-XR device and retrieves the version.

    Args:
        device (dict): Device connection details.

    Returns:
        str: IOS version if successful, or an error message.
    """
    try:
        if "os_type" not in device:
            raise KeyError("Missing 'os_type' in device configuration")

        os_type = device["os_type"]
        if os_type == "ios-xe":
            device_type = "cisco_ios"
            command = "show version | include Cisco IOS XE Software"
        elif os_type == "ios-xr":
            device_type = "cisco_xr"
            command = "show version | include Cisco IOS XR Software"
        else:
            raise ValueError(f"Unsupported OS type: {os_type}")

        connection = ConnectHandler(
            device_type=device_type,
            host=device["host"],
            username=device["username"],
            password=device["password"],
            port=device["port"]
        )
        output = connection.send_command(command)
        connection.disconnect()

        if output:
            return Fore.GREEN + f"{device['host']} - {device['name']} - {device['os_type'].upper()} Version: {output.strip()}"
        else:
            return Fore.YELLOW + f"{device['host']} - {device['name']} - {device['os_type'].upper()} Version: No output received"

    except KeyError as e:
        return Fore.RED + f"{device['host']} - {device['name']} ❌ Missing key in device config: {e}"
    except ValueError as e:
        return Fore.RED + f"{device['host']} - {device['name']} ❌ Configuration Error: {e}"
    except Exception as e:
        return Fore.RED + f"{device['host']} - {device['name']} ❌ Connection Failed: {e}"

if __name__ == "__main__":
    devices = load_devices()
    print(Fore.CYAN + "\n🔍 Checking IOS Versions...\n")
    for device in devices:
        print(get_ios_version(device))
