import yaml

def validate_yaml(file_path):
    """
    Validates the formatting of a YAML file.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        bool: True if valid, False if formatting is incorrect.
    """
    try:
        with open(file_path, "r") as file:
            yaml.safe_load(file)
        print("✅ YAML Formatting: Valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ YAML Formatting Error: {e}")
        return False

if __name__ == "__main__":
    if not validate_yaml("devices.yaml"):
        exit(1)  # Exit with error if formatting is incorrect

