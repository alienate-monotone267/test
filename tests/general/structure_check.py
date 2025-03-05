import yaml
import re
import sys
from urllib.parse import urlparse

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    
    expected_schema = {
        "title": str,
        "severity": str,
        "description": str,
        "author": str,
        "version": str,
        "documentation": "url",
        "query": str,
        "deploy_to": list,
        "active": bool
    }
    
    errors = []
    
    for key, expected_type in expected_schema.items():
        if key not in data:
            errors.append(f"Missing field: {key}")
            continue
        
        value = data[key]
        
        if expected_type == "url":
            if not isinstance(value, str) or not is_valid_url(value):
                errors.append(f"Invalid URL format for field: {key}")
        elif expected_type == list:
            if not isinstance(value, list) or not all(isinstance(i, str) for i in value):
                errors.append(f"Field '{key}' should be a list of strings.")
        elif not isinstance(value, expected_type):
            errors.append(f"Field '{key}' should be of type {expected_type.__name__}.")
    
    if errors:
        print("Validation failed with the following errors:")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    else:
        print("YAML validation passed successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_yaml.py <file.yaml>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    validate_yaml(yaml_file)
