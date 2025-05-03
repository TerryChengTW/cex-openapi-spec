import os
import sys
import yaml
import json
import re
from pathlib import Path
from copy import deepcopy

def ensure_dir(path):
    """Ensure directory exists, create if it doesn't"""
    if not os.path.exists(path):
        os.makedirs(path)

def save_yaml(data, file_path):
    """Save YAML data to file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

def save_json(data, file_path):
    """Save JSON data to file"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def fix_ref_paths(data, current_component_type):
    """Fix $ref to use relative paths"""
    if isinstance(data, dict):
        for key, value in list(data.items()):
            if key == '$ref' and isinstance(value, str) and value.startswith('#/components/'):
                parts = value.strip('#/').split('/')
                if len(parts) == 3:
                    # e.g. ['components', 'schemas', 'Ticker']
                    _, ref_type, ref_name = parts
                    if ref_type == 'schemas':
                        data[key] = f"../schemas/{ref_name}.yaml"
                    else:
                        data[key] = f"../components/{ref_type}/{ref_name}.yaml"
            else:
                fix_ref_paths(value, current_component_type)
    elif isinstance(data, list):
        for item in data:
            fix_ref_paths(item, current_component_type)
    return data

def get_path_filename_from_url(path):
    """Generate filename from API path"""
    # Handle path format, e.g. /api/v3/ping -> ping_v3
    match = re.match(r'/api/v(\d+)/(.+)', path)
    if match:
        version = match.group(1)
        route = match.group(2)
        # Replace slashes with underscores
        route = route.replace('/', '_')
        # Replace curly braces
        route = route.replace('{', '').replace('}', '')
        # Final format: route_v{version}
        return f"{route}_v{version}"
    else:
        # Handle other path formats
        # Remove leading slash
        clean_path = path.strip('/')
        
        # Check if there's a version number
        version_match = re.search(r'v(\d+)', clean_path)
        if version_match:
            # Extract version number
            version = version_match.group(1)
            # Remove version part to avoid duplication
            clean_path = re.sub(r'/v\d+/?', '/', clean_path)
            # Replace slashes with underscores
            clean_path = clean_path.replace('/', '_')
            # Remove curly braces
            clean_path = clean_path.replace('{', '').replace('}', '')
            return f"{clean_path}_v{version}"
        else:
            # No version number, just process the path
            clean_path = clean_path.replace('/', '_').replace('{', '').replace('}', '')
            return clean_path

def process_path_responses(path_url, responses, output_dir):
    """Process path responses, create standalone files and return references"""
    # Get path name (for naming response files)
    path_name = get_path_filename_from_url(path_url)
    new_responses = {}
    
    for status_code, response in responses.items():
        # Create response filename
        response_name = f"{path_name}_{status_code}"
        
        # Fix reference paths
        response = fix_ref_paths(response, "responses")
        
        # Save response to standalone file
        response_path = os.path.join(output_dir, 'components', 'responses', f"{response_name}.yaml")
        save_yaml(response, response_path)
        
        # Update with reference
        new_responses[status_code] = {'$ref': f"../components/responses/{response_name}.yaml"}
    
    return new_responses

def process_path(path_url, path_object, output_dir):
    """Process API path, create standalone file and return reference"""
    # Deep copy to avoid modifying original object
    path_object_copy = deepcopy(path_object)
    
    # Process each HTTP method
    for method, operation in path_object_copy.items():
        if method in ['get', 'post', 'put', 'delete', 'patch', 'options', 'head']:
            # If operation contains responses
            if 'responses' in operation:
                # Process responses and replace with references
                operation['responses'] = process_path_responses(path_url, operation['responses'], output_dir)
    
    # Fix other reference paths
    path_object_copy = fix_ref_paths(path_object_copy, "paths")
    
    # Generate filename using new naming format
    filename = get_path_filename_from_url(path_url)
    file_path = os.path.join(output_dir, 'paths', f"{filename}.yaml")
    
    # Save path object
    save_yaml(path_object_copy, file_path)
    
    # Return reference
    return {'$ref': f"./paths/{filename}.yaml"}

def process_schema(schema, name, output_dir):
    """Process schema definition, create standalone file and return reference"""
    # Fix reference paths
    schema = fix_ref_paths(schema, "schemas")
    
    # Create file for schema
    schema_path = os.path.join(output_dir, 'components', 'schemas', f"{name}.yaml")
    save_yaml(schema, schema_path)
    
    # Return reference
    return {'$ref': f"./components/schemas/{name}.yaml"}

def process_parameter(parameter, name, output_dir):
    """Process parameter definition, create standalone file and return reference"""
    # Fix reference paths
    parameter = fix_ref_paths(parameter, "parameters")
    
    # Create file for parameter
    param_path = os.path.join(output_dir, 'components', 'parameters', f"{name}.yaml")
    save_yaml(parameter, param_path)
    
    # Return reference
    return {'$ref': f"./components/parameters/{name}.yaml"}

def process_response(response, name, output_dir):
    """Process response definition, create standalone file and return reference"""
    # Fix reference paths
    response = fix_ref_paths(response, "responses")
    
    # Create file for response
    response_path = os.path.join(output_dir, 'components', 'responses', f"{name}.yaml")
    save_yaml(response, response_path)
    
    # Return reference
    return {'$ref': f"./components/responses/{name}.yaml"}

def split_openapi(yaml_file, output_dir, max_endpoints=1):
    """Split OpenAPI YAML file and replace content with references"""
    # Load YAML file
    with open(yaml_file, 'r', encoding='utf-8') as f:
        api_spec = yaml.safe_load(f)
    
    # Create output directories
    ensure_dir(output_dir)
    ensure_dir(os.path.join(output_dir, 'paths'))
    ensure_dir(os.path.join(output_dir, 'components', 'schemas'))
    ensure_dir(os.path.join(output_dir, 'components', 'responses'))
    ensure_dir(os.path.join(output_dir, 'components', 'parameters'))
    
    # Process components section
    if 'components' in api_spec:
        # Process schemas
        if 'schemas' in api_spec['components']:
            new_schemas = {}
            for schema_name, schema in api_spec['components']['schemas'].items():
                new_schemas[schema_name] = process_schema(schema, schema_name, output_dir)
            api_spec['components']['schemas'] = new_schemas
        
        # Process parameters
        if 'parameters' in api_spec['components']:
            new_parameters = {}
            for param_name, param in api_spec['components']['parameters'].items():
                new_parameters[param_name] = process_parameter(param, param_name, output_dir)
            api_spec['components']['parameters'] = new_parameters
            
        # Process responses (if exists)
        if 'responses' in api_spec['components']:
            new_responses = {}
            for resp_name, response in api_spec['components']['responses'].items():
                new_responses[resp_name] = process_response(response, resp_name, output_dir)
            api_spec['components']['responses'] = new_responses
    
    # Process paths
    if 'paths' in api_spec:
        new_paths = {}
        endpoint_count = 0
        
        for path, path_item in api_spec['paths'].items():
            endpoint_count += 1
            if max_endpoints > 0 and endpoint_count > max_endpoints:
                break
                
            # Process entire path object
            new_paths[path] = process_path(path, path_item, output_dir)
        
        api_spec['paths'] = new_paths
    
    # Save main OpenAPI file
    main_output = os.path.join(output_dir, 'openapi.yaml')
    save_yaml(api_spec, main_output)
    
    print(f"Successfully split OpenAPI spec into {output_dir} directory")
    print(f"Processed a total of {endpoint_count} endpoints")
    return api_spec

def main():
    # Set variables directly, no need to read from command line
    input_file = './vendor/openapi/binance-api-swagger/spot_api.yaml'
    output_dir = './openapi/binance'
    max_endpoints = 0  # Set to 0 to process all endpoints
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)
    
    split_openapi(input_file, output_dir, max_endpoints)

if __name__ == "__main__":
    main() 