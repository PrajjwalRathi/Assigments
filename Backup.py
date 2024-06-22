import os
import shutil
from datetime import datetime
import paramiko
import boto3
from botocore.exceptions import ClientError

# Function to backup directory to a remote server via SSH
def backup_to_remote_server(local_dir, remote_host, remote_user, remote_dir):
    # Generate a timestamp for the backup
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_dir_name = os.path.basename(local_dir) + '_' + timestamp
    backup_dir_path = os.path.join('/tmp', backup_dir_name)

    try:
        # Create a temporary directory for storing the backup
        shutil.copytree(local_dir, backup_dir_path)

        # Connect to the remote server via SSH
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(remote_host, username=remote_user)

        # SCP the backup directory to the remote server
        scp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        remote_backup_dir = os.path.join(remote_dir, backup_dir_name)
        scp.put(backup_dir_path, remote_backup_dir)

        # Cleanup local temporary directory
        shutil.rmtree(backup_dir_path)

        # Close SSH connection
        scp.close()
        ssh.close()

        return True, f"Backup successfully transferred to {remote_host}:{remote_backup_dir}"
    
    except Exception as e:
        return False, f"Backup failed: {str(e)}"

# Function to backup directory to AWS S3
def backup_to_aws_s3(local_dir, bucket_name, s3_key_prefix=''):
    # Generate a timestamp for the backup
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_dir_name = os.path.basename(local_dir) + '_' + timestamp

    try:
        # Upload directory to S3 bucket
        s3_client = boto3.client('s3')
        for root, dirs, files in os.walk(local_dir):
            for file in files:
                local_path = os.path.join(root, file)
                s3_key = os.path.join(s3_key_prefix, backup_dir_name, os.path.relpath(local_path, local_dir))
                s3_client.upload_file(local_path, bucket_name, s3_key)

        return True, f"Backup successfully uploaded to AWS S3 bucket: {bucket_name}/{s3_key_prefix}/{backup_dir_name}"
    
    except ClientError as e:
        return False, f"Backup failed: {e}"

# Example usage
if __name__ == "__main__":
    # Example parameters
    local_directory = '/path/to/your/local/directory'
    remote_server = 'example.com'
    remote_username = 'your_username'
    remote_directory = '/path/to/remote/directory'

    aws_bucket_name = 'your-aws-s3-bucket-name'
    aws_s3_key_prefix = 'backup'

    # Perform backup to remote server
    success, message = backup_to_remote_server(local_directory, remote_server, remote_username, remote_directory)
    print(message)

    # Perform backup to AWS S3
    success, message = backup_to_aws_s3(local_directory, aws_bucket_name, aws_s3_key_prefix)
    print(message)
