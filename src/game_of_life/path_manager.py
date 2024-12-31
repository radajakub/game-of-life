from pathlib import Path

from game_of_life.config import SERIALIZED_DIR_NAME


class PathManager:
    def __init__(self, root: str = '.') -> None:
        self.root = Path(root)

        self.serialized_dir = self._make_dir(SERIALIZED_DIR_NAME)

    def _make_dir(self, *name: str) -> Path:
        directory = self.root
        for n in name:
            directory = directory / n

        if not directory.exists():
            directory.mkdir(parents=True)

        return directory
