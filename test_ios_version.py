import yaml
from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException

def load_devices():
    """Loads device credentials from devices.yaml."""
    try:
        with open("devices.yaml", "r") as file:
            data = yaml.safe_load(file)
            if "devices" not in data:
                raise KeyError("Missing 'devices' key in YAML file")
            return data["devices"]
    except yaml.YAMLError as e:
        print(f"❌ YAML Parsing Error: {e}")
        exit(1)

def check_ios_version(device):
    """
    Connects to a Cisco IOS-XE or IOS-XR device and retrieves the version.

    Args:
        device (dict): Device connection details.

    Returns:
        str: Device OS version or error message.
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

        return output.strip() if output else "Version information not found."

    except NetMikoTimeoutException:
        return "❌ ERROR: Device unreachable (Timeout)"
    except NetMikoAuthenticationException:
        return "❌ ERROR: Authentication failed"
    except KeyError as e:
        return f"❌ ERROR: Missing key in device config: {e}"
    except ValueError as e:
        return f"❌ ERROR: {e}"
    except Exception as e:
        return f"❌ ERROR: {e}"

if __name__ == "__main__":
    devices = load_devices()
    for device in devices:
        version_output = check_ios_version(device)
        print(f"{device['name']} ({device['os_type'].upper()}) - Version: {version_output}")
