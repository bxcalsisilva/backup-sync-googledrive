# Backup and Sync (GoogleDrive)

Recursive backup of folder to a different folder (second Disk recommended).
Uploads new and changed files (.csv).

- Prevents duplicates file creation or same filename in GoogleDrive.
- Records no updated files on unavailable internet connection.

## Requirements

- GoogleDrive API token:
    - client_secrets.json
- To avoid permision each run create a `settings.yaml` file

### settings.yaml

```
    client_config_backend: file
    client_config:
        client_id: <your_client_id>
        client_secret: <your_client_secret>

    save_credentials: True
    save_credentials_backend: file
    save_credentials_file: creds.json

    get_refresh_token: True

    oauth_scope:
        - https://www.googleapis.com/auth/drive
        - https://www.googleapis.com/auth/drive.install
```
Insert your `client_id` and `client_secret` from `client_secrets.json` file.