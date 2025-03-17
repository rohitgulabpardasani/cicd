import yaml
from netmiko import ConnectHandler

def load_devices():
    """
    Loads device credentials from devices.yaml.

    Returns:
        list: List of devices from the YAML file.
    """
    try:
        with open("devices.yaml", "r") as file:
            data = yaml.safe_load(file)
            if "devices" not in data:
                raise KeyError("Missing 'devices' key in YAML file")
            return data["devices"]
    except yaml.YAMLError as e:
        print(f"❌ YAML Parsing Error: {e}")
        exit(1)
    except FileNotFoundError:
        print("❌ Error: devices.yaml file not found.")
        exit(1)

def get_device_version(device):
    """
    Connects to a Cisco IOS-XE or IOS-XR device and retrieves the version.

    Args:
        device (dict): Device connection details.

    Returns:
        str: IOS-XE or IOS-XR version, or an error message if unreachable.
    """
    try:
        if "os_type" not in device:
            raise KeyError(f"❌ Missing 'os_type' for device {device.get('name', 'Unknown Device')}")

        os_type = device["os_type"]
        if os_type == "ios-xe":
            device_type = "cisco_ios"
            command = "show version | include Cisco IOS XE Software"
        elif os_type == "ios-xr":
            device_type = "cisco_xr"
            command = "show version | include Cisco IOS XR Software"
        else:
            raise ValueError(f"❌ Unsupported OS type: {os_type}")

        connection = ConnectHandler(
            device_type=device_type,
            host=device["host"],
            username=device["username"],
            password=device["password"],
            port=device.get("port", 22)  # Default SSH port is 22
        )
        output = connection.send_command(command)
        connection.disconnect()

        return output.strip() if output else "❌ No version info retrieved"

    except KeyError as e:
        return f"❌ Missing Key: {e}"
    except ValueError as e:
        return f"❌ Configuration Error: {e}"
    except Exception as e:
        return f"❌ Connection Failed: {device['host']} - {e}"

if __name__ == "__main__":
    devices = load_devices()
    print("\n🔍 Checking Cisco IOS Versions...\n")
    
    for device in devices:
        version_output = get_device_version(device)
        print(f"📡 {device['name']} ({device['host']}) - {device['os_type'].upper()} Version: {version_output}")

    print("\n✅ Version Check Completed.\n")
