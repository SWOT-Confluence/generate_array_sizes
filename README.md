# generate array size

Generate Array Size is a Lambda function that returns the array size for the following levels of input data:
- basin
- reach
- HiVDI sets
- MetroMan sets
- Sic4dVar sets

The Lambda function accesses the input EFS to load appropriate JSON data and tracks the length of the lists contained within. It sends this data back to the `confluence-workflow` Step Function.

## deployment

There is a script to deploy the Lambda function AWS infrastructure called `deploy.sh`.

REQUIRES:

- AWS CLI (<https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>)
- Terraform (<https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli>)

Command line arguments:

 [1] app_name: Name of application to create a zipped deployment package for
 [2] s3_state_bucket: Name of the S3 bucket to store Terraform state in (no need for s3:// prefix)
 [3] profile: Name of profile used to authenticate AWS CLI commands

# Example usage: `./delpoy-lambda.sh "my-app-name" "s3-state-bucket-name" "confluence-named-profile"`