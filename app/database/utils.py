import json
import os.path
from json import JSONDecodeError


# ----------------------------------------------------------------------------------------------------------------------
# Create classes
class DatabaseController:
    """
    IO controller for the database
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def _read_file(self) -> list:
        """
        Open file and read data from it
        Returns:
             list with data
        """
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as file:
                file.write('[]')

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data

        except JSONDecodeError:
            print('ОШИБКА ЧТЕНИЯ ФАЙЛА!')
            exit()

    def _write_file(self, data: list) -> None:
        """
        Open file and read data from it
        Args:
            data: list with data
        Returns:
             None
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def get_data(self) -> list:
        """
        Get list with all data in database
        Returns:
             list with result
        """
        return self._read_file()

    def save_data(self, data: list) -> None:
        """
        Save data to the database
        Args:
            data: list with all data to save
        Returns:
             None
        """
        return self._write_file(data)

    def add_data(self, data: dict) -> None:
        """
        Add a new data to the database
        Args:
            data: dictionary with new data
        Returns:
             None
        """
        file: list = self._read_file()
        file.append(data)
        self._write_file(file)
