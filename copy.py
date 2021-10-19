from pathlib import Path
import shutil
import filecmp


class Copy:
    """
    Compare files and directories in two directories.
    Copy files not found and modified from source to destiny directory.
    """

    def __init__(self, src, dst):
        """Initialize root source and destiny directories."""

        self.src = src
        self.dst = dst

    def copy(self):
        """Compare the directories and copy new or modified files."""

        self.cmp = self.compare_dir(self.src, self.dst)

        self.copy_left(self.cmp)
        self.copy_modified(self.cmp)
        self.copy_subdir(self.cmp)

    def compare_dir(self, src, dst):
        """Compare directories."""
        print("comparing", src)
        cmp = filecmp.dircmp(src, dst)
        return cmp

    def copy_left(self, cmp):
        """Copy files or directories only found in source"""

        if not cmp.left_only:
            return
        print(cmp.left)
        for path in cmp.left_only:
            src = cmp.left / path
            dst = cmp.right / path

            self.copy_file_dir(src, dst)

    def copy_file_dir(self, src, dst):
        """Check if source is directory or file and copy to destiny."""

        if src.is_dir():
            shutil.copytree(src, dst)
            print("Directory copied:", src)
        elif src.is_file():
            shutil.copy2(src, dst)
            print("File copied:", src)

    def copy_modified(self, cmp):
        """Check for modified files in source and copy them."""

        if not cmp.diff_files:
            return

        diff_files = cmp.diff_files
        for f in diff_files:
            src = cmp.left / f
            dst = cmp.right / f
            self.copy_file_dir(src, dst)

    def copy_subdir(self, cmp):
        """Recursive copy of subdirectories."""
        if not cmp.subdirs:
            print("No subdirectories in:", cmp.left)
            return

        for _, dircmp in cmp.subdirs.items():
            src = dircmp.left
            dst = dircmp.right
            subcmp = self.compare_dir(src, dst)

            self.copy_left(subcmp)
            self.copy_modified(subcmp)
            if subcmp.subdirs:
                self.copy_subdir(subcmp)


if __name__ == "__main__":

    src = Path.cwd() / "test/PUCP/"
    dst = Path.cwd() / "test/PUCP2/"

    copy = Copy(src, dst)
    copy.copy()
