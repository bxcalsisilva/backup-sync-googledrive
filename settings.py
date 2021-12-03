class Settings:
    def __init__(self) -> None:
        # Source folder to backup
        self.src = "/home/bcalsi/github/backup-sync-googledrive/test/pc1/PUCP"
        # Destiny folder to copy files to
        self.dst = "/home/bcalsi/github/backup-sync-googledrive/test/pc2/PUCP"

        # File to write backuped files and which to upload
        # Don't change the filename
        self.filename_backup = "backup_paths.txt"

        # Root title and id of file in GoogleDrive
        # Information on where the folder is to be uploaded
        self.root = {"title": "test", "id": "1SxGcZiei7xkC4SF-GpLMg5Z2bdyp7RK4"}

        # Mimetypes equivalents of GoogleDriveAPI
        self.mimetypes = {
            "folder": "application/vnd.google-apps.folder",
            "csv": "text/plain",
        }
