import json

def lambda_handler(event, context):
    tasks = [
        {"id": 1, "title": "Learn CloudFormation"},
        {"id": 2, "title": "Build a CI/CD pipeline"}
    ]
    return {
        "statusCode": 200,
        "body": json.dumps({"tasks": tasks})
    }