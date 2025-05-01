#!/usr/bin/env python
import os
import yaml
import json
import re
import shutil
from pathlib import Path
import copy
import sys

# 獲取腳本的絕對路徑
script_path = os.path.dirname(os.path.abspath(__file__))
# 獲取項目根目錄 (腳本目錄的父目錄)
root_path = os.path.dirname(script_path)

# Define target directories relative to root
OUTPUT_DIR = os.path.join(root_path, "openapi/binance")
SCHEMAS_DIR = os.path.join(OUTPUT_DIR, "schemas")
PATHS_DIR = os.path.join(OUTPUT_DIR, "paths", "spot")
RESPONSES_DIR = os.path.join(OUTPUT_DIR, "responses")
PARAMETERS_DIR = os.path.join(OUTPUT_DIR, "parameters")

# Set the number of endpoints to process
MAX_ENDPOINTS = 1

def ensure_directory(directory_path):
    """Ensure directory exists, create if it doesn't"""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def load_yaml_file(file_path):
    """Load YAML file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def save_yaml_file(data, file_path):
    """Save YAML file"""
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, sort_keys=False, default_flow_style=False)

def split_openapi_spec(spec_file, max_endpoints=MAX_ENDPOINTS):
    """Split OpenAPI specification file"""
    # Clean up previous output directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    
    # Load specification file
    spec = load_yaml_file(spec_file)
    
    # Ensure target directories exist
    ensure_directory(OUTPUT_DIR)
    ensure_directory(SCHEMAS_DIR)
    ensure_directory(PATHS_DIR)
    ensure_directory(RESPONSES_DIR)
    ensure_directory(PARAMETERS_DIR)
    
    # Extract the first x endpoints from paths
    if 'paths' not in spec:
        print("Error: No paths found in specification")
        return

    all_endpoints = list(spec['paths'].keys())
    target_endpoints = all_endpoints[:max_endpoints]
    
    if not target_endpoints:
        print("Error: No endpoints found")
        return

    print(f"Processing the following {len(target_endpoints)} endpoints:")
    for endpoint in target_endpoints:
        print(f"- {endpoint}")

    # Create a new spec with only selected endpoints, excluding components
    new_spec = {
        'openapi': spec['openapi'],
        'info': spec['info'],
        'servers': spec.get('servers', [])
    }
    
    # Preserve all tags
    if 'tags' in spec:
        new_spec['tags'] = spec['tags']
    
    # Process each endpoint
    new_spec['paths'] = {}
    
    # Extract and save all parameter definitions
    if 'components' in spec and 'parameters' in spec['components']:
        for param_name, param_def in spec['components']['parameters'].items():
            param_file = os.path.join(PARAMETERS_DIR, f"{param_name}.yaml")
            save_yaml_file(param_def, param_file)
            print(f"Saved parameter: {param_name}")

    # Extract and save all schema definitions
    if 'components' in spec and 'schemas' in spec['components']:
        for schema_name, schema_def in spec['components']['schemas'].items():
            schema_file = os.path.join(SCHEMAS_DIR, f"{schema_name}.yaml")
            save_yaml_file(schema_def, schema_file)
            print(f"Saved schema: {schema_name}")
    
    # Create separate files for all responses, instead of placing them in the main spec
    for endpoint in target_endpoints:
        endpoint_name = endpoint.strip('/').split('/')[-1]
        
        # Copy endpoint data for modification
        endpoint_data = copy.deepcopy(spec['paths'][endpoint])
        
        # Process responses and parameters in each method
        for method, method_data in endpoint_data.items():
            # Process responses
            if 'responses' in method_data:
                # Process each status code response separately
                for status_code, response in method_data['responses'].items():
                    # Create a unique identifier for each status code
                    response_id = f"{endpoint_name}_{method}_{status_code}"
                    
                    # Save to a separate file
                    response_file = os.path.join(RESPONSES_DIR, f"{response_id}.yaml")
                    save_yaml_file(response, response_file)
                
                # Use relative paths to reference external files in endpoint data
                new_responses = {}
                for status_code in method_data['responses'].keys():
                    response_id = f"{endpoint_name}_{method}_{status_code}"
                    rel_path = os.path.relpath(RESPONSES_DIR, PATHS_DIR)
                    new_responses[status_code] = {
                        '$ref': f'{rel_path}/{response_id}.yaml'
                    }
                
                # Replace original responses
                method_data['responses'] = new_responses
            
            # Process parameters
            if 'parameters' in method_data:
                new_params = []
                for param in method_data['parameters']:
                    if isinstance(param, dict) and '$ref' in param:
                        # Extract parameter name
                        ref_path = param['$ref']
                        param_name = ref_path.split('/')[-1]
                        
                        # Use relative path reference
                        rel_path = os.path.relpath(PARAMETERS_DIR, PATHS_DIR)
                        new_params.append({
                            '$ref': f'{rel_path}/{param_name}.yaml'
                        })
                    else:
                        new_params.append(param)
                
                # Replace original parameters
                method_data['parameters'] = new_params
        
        # Save endpoint to a separate file
        endpoint_file = os.path.join(PATHS_DIR, f"{endpoint_name}.yaml")
        
        # Create YAML structure containing the entire endpoint path
        path_yaml = {'paths': {endpoint: endpoint_data}}
        save_yaml_file(path_yaml, endpoint_file)
        
        # Reference the file in the main spec
        new_spec['paths'][endpoint] = {'$ref': f'./paths/spot/{endpoint_name}.yaml#/paths{endpoint}'}
        
        print(f"Finished processing endpoint {endpoint}")
    
    # Save the main OpenAPI file
    save_yaml_file(new_spec, os.path.join(OUTPUT_DIR, 'openapi.yaml'))
    
    print(f"Completed processing all {len(target_endpoints)} endpoints")
    
if __name__ == "__main__":
    # Specify the path to the Binance Spot API specification file
    spec_file = os.path.join(root_path, "vendor/openapi/binance-api-swagger/spot_api.yaml")
    
    if os.path.exists(spec_file):
        # You can modify the number here to process different quantities of endpoints
        split_openapi_spec(spec_file, max_endpoints=1000)  # For example, process the first 5 endpoints
    else:
        print(f"Error: File not found {spec_file}")
