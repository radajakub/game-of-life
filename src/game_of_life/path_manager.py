from pathlib import Path

from config import DB_ROOT, DB_BOARD_DIR, DB_PATTERN_DIR


class PathManager:
    def __init__(self, root: str = '.') -> None:
        self.root = Path(root)

        self.db_root = self._make_dir(self.root, DB_ROOT)
        self.db_board_dir = self._make_dir(self.db_root, DB_BOARD_DIR)
        self.db_pattern_dir = self._make_dir(self.db_root, DB_PATTERN_DIR)

    def _make_dir(self, parent: Path, dirname: str) -> Path:
        directory = parent / dirname

        if not directory.exists():
            directory.mkdir(parents=True)

        return directory

    def _extend(self, path: Path, extension: str = ".pkl") -> Path:
        return path.with_suffix(extension)

    def get_pattern_path(self, pattern_name: str) -> str:
        return self._extend(self.db_pattern_dir / pattern_name.lower().replace(" ", "_"))
