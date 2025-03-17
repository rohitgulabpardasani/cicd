import yaml
from netmiko import ConnectHandler

def load_devices():
    """Loads device credentials from devices.yaml."""
    with open("devices.yaml", "r") as file:
        return yaml.safe_load(file)["devices"]

def check_ios_version(device):
    """
    Connects to a Cisco IOS-XE device and retrieves the version.

    Args:
        device (dict): Device connection details.

    Returns:
        str: IOS-XE version.
    """
    connection = ConnectHandler(
        device_type="cisco_ios",
        host=device["host"],
        username=device["username"],
        password=device["password"],
        port=device["port"]
    )
    output = connection.send_command("show version | include Cisco IOS XE Software")
    connection.disconnect()
    return output.strip()

if __name__ == "__main__":
    devices = load_devices()
    for device in devices:
        version_output = check_ios_version(device)
        print(f"{device['name']} - IOS-XE Version: {version_output}")

