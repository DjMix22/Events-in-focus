import json
from pathlib import Path

from src.domain.errors import DuplicateValueError


class UserRepo:
    def __init__(self, user_id: int, file_path: Path):
        self.user_id = user_id
        self.file_path = file_path

    def id_in_db(self, list_save: str) -> bool:
        with open(self.file_path, 'r') as file_users:
            data = json.load(file_users)

        if self.user_id in data[list_save]:
            return True
        return False

    def save(self, list_save: str) -> None:
        with open(self.file_path, 'r') as file_users:
            data = json.load(file_users)

        if self.user_id in data[list_save]:
            raise DuplicateValueError(f'ID {self.user_id} is already in the database!')
        data[list_save].append(self.user_id)

        with open(self.file_path, 'w') as file_users:
            json.dump(data, file_users, indent=4)
