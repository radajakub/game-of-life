""" Module for managing paths to the database. """

from pathlib import Path

from game_of_life.config import DB_ROOT, DB_BOARD_DIR, DB_PATTERN_DIR


class PathManager:
    """
    Class abstraction to wrap the creation and reading of paths to pattern database.
    """

    def __init__(self, root: str = '.') -> None:
        """
        Initialize the path manager with the given root directory.

        Args:
            root: the root directory to use for the database
        """

        self.root = Path(root)

        self.db_root = self._make_dir(self.root, DB_ROOT)
        self.db_board_dir = self._make_dir(self.db_root, DB_BOARD_DIR)
        self.db_pattern_dir = self._make_dir(self.db_root, DB_PATTERN_DIR)

    def _make_dir(self, parent: Path, dirname: str) -> Path:
        """
        Make the directory if it doesn't exist and return it as Path object.

        Args:
            parent: the parent directory
            dirname: the name of the directory to make
        """

        directory = parent / dirname

        if not directory.exists():
            directory.mkdir(parents=True)

        return directory

    def _extend(self, path: Path, extension: str = ".pkl") -> Path:
        """
        Extend the path with the given extension.

        Args:
            path: the path to extend
            extension: the extension to add
        """

        return path.with_suffix(extension)

    def get_pattern_path(self, pattern_name: str) -> str:
        """
        Get the path to the pattern with the given name in the pattern database.

        Args:
            pattern_name: the name of the pattern
        """

        return self._extend(self.db_pattern_dir / pattern_name.lower().replace(" ", "_"))

    def get_all_patterns(self) -> list[str]:
        """
        Get all the patterns in the pattern database.
        """

        return self.db_pattern_dir.glob("*.pkl")
