import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

BUCKET = os.getenv("AWS_BUCKET_NAME")

def upload_to_s3(file_content: bytes, file_key: str, content_type: str) -> str:
    s3_client.put_object(
        Bucket=BUCKET,
        Key=file_key,
        Body=file_content,
        ContentType=content_type,
        ACL="public-read"
    )
    return f"https://{BUCKET}.s3.amazonaws.com/{file_key}"