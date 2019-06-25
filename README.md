# serverless

For the task were used:

    Python3.6
    
    AWS - Lambda, DynamoDB, API Gateway, CloudWatch.
    
    Serverless framework.

Python3.6:

    Used native python3.6 without frameworks.

Serverless framework:

    Used for deploying project to AWS.

AWS:

    Lambda - used for api handlers (create, delete, update, etc.)
    
    DynamoDB - storing data. But for this task DynamoDB is not correct and I can't implement sorting task by size, height. Would be better to use RDS and work with GROUP BY.
    
    Api Gateway - used for REST API. Describe endpoints.
    
    CloudWatch - used for logging request to API.
