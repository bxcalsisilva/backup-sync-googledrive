from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pathlib import Path

import httplib2

from settings import Settings


class Upload:
    def __init__(self):
        gauth = GoogleAuth()
        gauth.CommandLineAuth()
        self.drive = GoogleDrive(gauth)

        self.settings = Settings()

        self.copied_paths = []
        self.uploadad_paths = []

    def upload_paths(self):
        """Uploads copied paths."""

        for path in self.copied_paths:
            # Path relative to the destiny directory
            # Similar structure as in GoogleDrive
            path = Path(path)
            dir = path.relative_to(self.settings.dst)

            # parent title and id of final path to upload
            parent = self.get_parent(dir)

            file1 = self.create_file(path, parent["id"])

            self._upload(file1)

    def get_parent(self, dir):
        """
        Iterates inversely from root directory (GoogleDrive) to get the parent title and id.
        Start from root folder in source path (backup folder).
        """
        # The last parent is always the root in GoogleDrive from Settings.py
        parent = self.settings.root
        # Reverse iteration
        # [-2::-1] skips the last item on the list (root already initialized)
        for dir in list(dir.parents)[-2::-1]:
            title = dir.name
            id = self.get_id(title, parent["id"])

            if id is None:
                # Unable to connect to server (GoogleDrive)
                return

            # Update parent info for next iteration
            # Navigates deep in GoogleDrive folder
            parent = {"title": title, "id": id}

        return parent

    def get_id(self, title: str, parent_id: str):
        """Returns id of a path. Needs name (title) and id of parent."""

        q = f"title = '{title}' and '{parent_id}' in parents and trashed=false"
        try:
            dir = self.drive.ListFile({"q": q}).GetList()
        except httplib2.error.ServerNotFoundError:
            # No connection to internet.
            # Request didn't went trough
            print("Unable to get List.")
            return

        try:
            return dir[0]["id"]
        except IndexError:
            # File not found
            return

    def _upload(self, file1):
        try:
            file1.Upload()
            self.uploadad_paths.append(str(dir))
        except httplib2.error.ServerNotFoundError:
            print("Server connection error")
        except:
            print("Unable to upload", file1["title"])

    def create_file(self, path, parent_id):
        """Creates file type (GoogleDrive API)."""
        mimetype = self._mimetype(path)
        file1 = self.drive.CreateFile(
            {"title": path.name, "mimeType": mimetype, "parents": [{"id": parent_id}]}
        )

        file1 = self._add_id(file1)
        file1 = self._set_content(file1, path)

        return file1

    def _add_id(self, file1):
        """Adds id in case the file is already in GoogleDrive."""

        name = file1["title"]
        parent_id = file1["parents"][0]["id"]
        id = self.get_id(name, parent_id)

        # Set the id if the file exists
        # Prevents duplicates files
        if id != None:
            file1["id"] = id

        return file1

    def _set_content(self, file1, path):
        """Set the content if file is csv."""

        if path.suffix == ".csv":
            file1.SetContentFile(path)

        return file1

    def _type(self, path):
        """Returns type of path"""
        # Read suffix type of path.
        suffix = Path(path).suffix
        if not suffix:  # directories don't have suffix
            type = "folder"
        elif suffix == ".csv":
            type = "csv"
        else:
            print(f"path {path} not a directory or csv file")
            return
        return type

    def _mimetype(self, dir):
        """Returns mimeType of path ('file' types in GoogleDrive API)."""
        type = self._type(dir)

        if type is None:
            return

        mimetype = self.settings.mimetypes[type]
        return mimetype

    def update_backup(self):
        """Update backup_paths.txt, removes uploaded paths."""
        with open(self.settings.filename_backup, "w") as file:
            not_uploaded = set(self.copied_paths) - set(self.uploadad_paths)
            not_uploaded = sorted(list(not_uploaded))
            # Writes paths not uploaded in the process.
            # Empty in case all files were uploadad succesfully.
            for path in not_uploaded:
                file.write(f"{path}\n")

    def read_copied_paths(self):
        """Read file of copied paths from source to destiny."""

        with open(self.settings.filename_backup, "r") as filehandle:
            for line in filehandle:
                dir = line[:-1]
                self.copied_paths.append(dir)

        # Remove duplicates
        self.copied_paths = list(dict.fromkeys(self.copied_paths))
        # Sort
        self.copied_paths.sort()


if __name__ == "__main__":
    upload = Upload()
    upload.read_copied_paths()
    upload.upload_paths()
    upload.update_backup()
