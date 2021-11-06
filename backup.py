from pathlib import Path
import shutil
import filecmp

from settings import Settings


class Copy:
    """
    Compare files and directories in two directories.
    Copy files not found and modified from source to destiny directory.
    """

    def __init__(self):
        """Initialize root source and destiny directories."""
        self.settings = Settings()

        self.src = Path(self.settings.src)
        self.dst = Path(self.settings.dst)

        self.copied_paths = []

    def copy(self):
        """Compare the directories and copy new or modified files."""

        self.cmp = self.compare_dir(self.src, self.dst)

        self.copy_left(self.cmp)
        self.copy_modified(self.cmp)
        self.copy_subdir(self.cmp)

    def recursive_copy(self):
        n_copied_paths = len(self.copied_paths)
        self.copy()
        if len(self.copied_paths) > n_copied_paths:
            self.recursive_copy()

    def compare_dir(self, src, dst):
        """Compare directories."""
        cmp = filecmp.dircmp(src, dst)
        return cmp

    def copy_left(self, cmp):
        """Copy files or directories only found in source"""

        if not cmp.left_only:
            return
        for path in cmp.left_only:

            src = Path(cmp.left) / path
            dst = Path(cmp.right) / path

            self.copy_file_dir(src, dst)

    def copy_file_dir(self, src, dst):
        """Check if source is directory or file and copy to destiny."""

        if src.is_dir():
            Path(dst).mkdir()
            # print("Directory copied:", src)
            self.copied_paths.append(dst)
        elif src.is_file():
            shutil.copy2(src, dst)
            # print("File copied:", src.name)
            self.copied_paths.append(dst)

    def copy_modified(self, cmp):
        """Check for modified files in source and copy them."""

        if not cmp.diff_files:
            return

        diff_files = cmp.diff_files
        for f in diff_files:
            src = Path(cmp.left) / f
            dst = Path(cmp.right) / f
            self.copy_file_dir(src, dst)

    def copy_subdir(self, cmp):
        """Recursive copy of subdirectories."""
        if not cmp.subdirs:
            # print("No subdirectories in:", cmp.left)
            return

        for _, dircmp in cmp.subdirs.items():
            src = Path(dircmp.left)
            dst = Path(dircmp.right)
            subcmp = self.compare_dir(src, dst)

            self.copy_left(subcmp)
            self.copy_modified(subcmp)
            if subcmp.subdirs:
                self.copy_subdir(subcmp)

    def write_copied_paths(self):
        """Write copied paths in file."""
        file_backup = Path(self.settings.filename_backup)
        # Creates the file if it doesn't exists
        file_backup.touch(exist_ok=True)
        # Append copied paths in file
        with open(file_backup, "a") as filehandle:
            for path in sorted(self.copied_paths):
                filehandle.write(f"{path}\n")


if __name__ == "__main__":
    copy = Copy()
    copy.recursive_copy()
    copy.write_copied_paths()
