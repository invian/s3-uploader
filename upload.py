import os
import argparse
import boto3
from botocore.client import Config
import mimetypes

def upload_files_to_s3(folder_path, bucket_name, s3_client):
    # Mapping of common file extensions to MIME types
    mime_types = {
        '.js': 'application/javascript',
        '.css': 'text/css',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.woff': 'font/woff',
        '.woff2': 'font/woff2',
        '.ttf': 'font/ttf',
        '.otf': 'font/otf',
        '.eot': 'application/vnd.ms-fontobject',
        '.svg': 'image/svg+xml',
        '.jpeg': 'image/jpeg',
        '.jpg': 'image/jpeg',
        '.png': 'image/png'
    }

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, folder_path)
            s3_path = relative_path.replace("\\", "/")

            # Determine the MIME type
            ext = os.path.splitext(file)[1]
            content_type = mime_types.get(ext, mimetypes.guess_type(local_path)[0])

            if not content_type:
                content_type = 'application/octet-stream'  # Default MIME type

            try:
                # Upload the file with the specified MIME type
                s3_client.upload_file(
                    local_path, bucket_name, s3_path,
                    ExtraArgs={'ContentType': content_type}
                )
                print(f'Successfully uploaded {local_path} to {s3_path}')
            except Exception as e:
                print(f'Failed to upload {local_path}: {e}')

def main():
    # Command line arguments setup
    parser = argparse.ArgumentParser(description='Upload folder to S3')
    parser.add_argument('folder_path', type=str, help='Path to the folder to upload')
    parser.add_argument('bucket_name', type=str, help='S3 bucket name')
    parser.add_argument('--endpoint_url', type=str, default='https://storage.yandexcloud.net', help='Yandex Object Storage endpoint URL')

    args = parser.parse_args()

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise Exception('AWS Credentials are not specified')

    # Create a session and S3 client
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url=args.endpoint_url,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
    )

    # Call the upload function
    upload_files_to_s3(args.folder_path, args.bucket_name, s3_client)

if __name__ == '__main__':
    main()
