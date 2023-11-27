"""AWS Lambda that determines the array sizes of different JSON files and 
assigns them to Confluence modules.

Determines the array size from each JSON file:
1. Loads JSON data and determines size the number of arrays.
2. Returns JSON that relates array size to a particular module.
"""

# Standard imports
import glob
import json
import pathlib

# Third-party imports
import boto3
import botocore

# Constants
EFS_DIR = pathlib.Path("/mnt/data")
JSON_FILE_LIST = ["basin.json", "hivdisets.json", "metrosets.json", "reaches.json", "sicsets.json"]

# Functions
def generate_array_size_handler(event, context):
    """Handles events from Step Function state machine transition."""
    
    print(f"Event - {event}")
    print(f"Context - {context}")
    
    # Track different levels and associated array sizes
    data_dict = {
        "continent": 0,
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
    print("Located and determined array sizes for basin, reach, and sets.")
    
    # Determine if any continents were left out, adjust continent.json, and send result back
    get_continent_data(data_dict)
    print("Located and determined continent array sizes.")
            
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

def get_continent_data(data_dict):
    """Determine how the continents present in SWOT data."""
    
    continent_dict = {
        "af": {"af" : [1]},
        "as": {"as" : [4, 3]},
        "eu": {"eu" : [2]},
        "na": {"na" : [7, 8, 9]},
        "oc": {"oc" : [5]},
        "sa": {"sa" : [6]}
    }
    
    # Grab datagen JSON files
    json_files = glob.glob(f"{EFS_DIR}/*.json")
    
    # Parse the files and determine continents
    c = []
    for json_file in json_files:
        for key in continent_dict.keys():
            if key in json_file and continent_dict[key] not in c:
                c.append(continent_dict[key])
    
    # Create new continent file
    with open(f"{EFS_DIR}/continent.json", 'w') as jf:
        json.dump(c, jf, indent=2)
    
    # Store number of continents
    data_dict["continent"] = len(c)
