import yaml

def validate_yaml(file_path):
    try:
        with open(file_path, "r") as file:
            yaml.safe_load(file)
        print("✅ YAML Formatting: Valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ YAML Formatting Error: {e.problem} at line {e.problem_mark.line+1}, column {e.problem_mark.column+1}")
        return False

if __name__ == "__main__":
    if not validate_yaml("devices.yaml"):
        exit(1)  # Exit with error if formatting is incorrect

