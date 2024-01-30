# AWS S3 Utility Script

This script provides a set of utilities for interacting with AWS S3, including functionalities to list S3 buckets, create express S3 buckets, download files from S3 to a local directory, and upload files from a local directory to S3. It is designed for users who need to manage S3 resources programmatically and serves as an educational tool for those learning to interact with AWS services using Python.

## Features

- **List Buckets**: Retrieve and display a list of all S3 buckets in your AWS account.
- **Create Express Bucket**: Create a new S3 express bucket with specific configurations in a specified availability zone.
- **Download from S3**: Download files from a specified S3 bucket and directory to a local directory, supporting both standard and express S3 buckets.
- **Upload to S3**: Upload files from a specified local directory to a specified S3 bucket and directory.

## Prerequisites

Before using this script, ensure you have the following:

- Python 3.8 or higher installed on your system.
- AWS CLI configured with your AWS credentials.
- `boto3` library installed, which can be done via pip:
  ```
  pip install boto3
  ```
- Appropriate AWS IAM permissions set for the operations you intend to perform (e.g., `s3:ListBucket`, `s3:GetObject`, `s3:PutObject`, `s3express:CreateBucket`).

## Installation

To start using this script:

1. Clone the repository or download the script file to your local machine:
  ```
  git clone https://github.com/anuj-sadani-infrrd/aws-s3-express-bucket.git
  ```
2. Navigate to the script directory.

## Configuration

Configure the script with your AWS credentials and desired region by setting the following variables at the beginning of the script:

- `aws_access_key_id`
- `aws_secret_access_key`
- `region`

Alternatively, you can configure your AWS CLI with default credentials and region, and the script will use these settings.

## Usage

To execute the script, run the following command in your terminal:
  ```
  python s3_utility_script.py
  ```

The script will perform the operations as defined in the main section, including listing buckets, creating an express bucket, downloading from, and uploading to S3.

## Contributing

Contributions to this project are welcome. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Commit your changes.
4. Push your branch and open a pull request.

Please ensure your code adheres to the Python coding standards (use `black`/`flake8`)

## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details.
