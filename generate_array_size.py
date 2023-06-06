"""AWS Lambda that determines the array sizes of different JSON files and 
assigns them to Confluence modules.

Determines the array size from each JSON file:
1. Loads JSON data and determines size the number of arrays.
2. Returns JSON that relates array size to a particular module.
"""

# Standard imports
import json
import pathlib

# Third-party imports
import boto3
import botocore

# Constants
EFS_DIR = pathlib.Path("/mnt/data/array_test")
JSON_FILE_LIST = ["basin.json", "hivdisets.json", "metrosets.json", "reaches.json", "sicsets.json"]

# Functions
def generate_array_size_handler(event, context):
    """Handles events from Step Function state machine transition."""
    
    print(f"Event - {event}")
    print(f"Context - {context}")
    
    # Track different levels and associated array sizes
    data_dict = {
        "basin": 0,
        "reaches": 0,
        "hivdisets": 0,
        "metrosets": 0,
        "sicsets": 0     
    }
    
    # Get array size for each type of level
    for json_name in JSON_FILE_LIST:
        json_file = EFS_DIR.joinpath(json_name)
        with open(json_file) as jf:
            data = json.load(jf)
            data_dict[json_file.name.split('.')[0]] = len(data)
    print("Located and determined array sizes.")
            
    # Send success response
    sf = boto3.client("stepfunctions")
    try:
        response = sf.send_task_success(
            taskToken=event["token"],
            output=json.dumps(data_dict)
        )
        print("Sent task success.")
    
    except botocore.exceptions.ClientError as err:
        response = sf.send_task_failure(
            taskToken=event["token"],
            error=err.response['Error']['Code'],
            cause=err.response['Error']['Message']
        )
        print("Sent task failure.")
