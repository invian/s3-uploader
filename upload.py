import os
import argparse
import boto3
from botocore.client import Config

def upload_files_to_s3(folder_path, bucket_name, s3_client):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, folder_path)
            s3_path = relative_path.replace("\\", "/")
            try:
                s3_client.upload_file(local_path, bucket_name, s3_path)
                print(f'Successfully uploaded {local_path} to {s3_path}')
            except Exception as e:
                print(f'Failed to upload {local_path}: {e}')

def main():
    # Настройка аргументов командной строки
    parser = argparse.ArgumentParser(description='Upload folder S3')
    parser.add_argument('folder_path', type=str, help='Path to the folder to upload')
    parser.add_argument('bucket_name', type=str, help='S3 bucket name')
    parser.add_argument('--endpoint_url', type=str, default='https://storage.yandexcloud.net', help='Yandex Object Storage endpoint URL')

    args = parser.parse_args()

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise Exception('AWS Credentials are not specified')

    # Создайте сессию и клиент S3
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        endpoint_url=args.endpoint_url,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
    )

    # Вызов функции загрузки
    upload_files_to_s3(args.folder_path, args.bucket_name, s3_client)

if __name__ == '__main__':
    main()
