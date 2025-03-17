import yaml
from netmiko import ConnectHandler

def load_devices():
    """Loads device credentials from devices.yaml."""
    with open("devices.yaml", "r") as file:
        return yaml.safe_load(file)["devices"]

def check_ssh(device):
    """
    Connects to a Cisco IOS-XE device via SSH.

    Args:
        device (dict): Device connection details.

    Returns:
        bool: True if SSH is successful, False otherwise.
    """
    try:
        connection = ConnectHandler(
            device_type="cisco_ios",
            host=device["host"],
            username=device["username"],
            password=device["password"],
            port=device["port"]
        )
        connection.disconnect()
        return True
    except Exception as e:
        print(f"SSH Connection Failed: {e}")
        return False

if __name__ == "__main__":
    devices = load_devices()
    for device in devices:
        if check_ssh(device):
            print(f"{device['name']} - SSH Connectivity: ✅ SUCCESS")
        else:
            print(f"{device['name']} - SSH Connectivity: ❌ FAILED")

