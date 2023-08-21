from app.database.utils import DatabaseController
from app.models.users import User


# ----------------------------------------------------------------------------------------------------------------------
# Create classes
class PhoneBook:
    """
    Service class between the database and the interface
    """

    def __init__(self, file_path: str):
        self.database = DatabaseController(file_path)
        self.cached_data = self.database.get_data()

    def get_all_contacts(self) -> list:
        """
        Get all contacts from the database
        Returns:
             list with contacts
        """
        data: list = self.cached_data
        all_contacts: list = [User(**user_data) for user_data in data]

        return all_contacts

    def add_contact(self, data: dict) -> None:
        """
        Save a new contact to the database and update the cache
        Args:
            data: dictionary with new contact data
        Returns:
            None
        """
        try:
            last_uid: int = self.cached_data[-1]['id']
        except IndexError:
            last_uid = 0

        new_uid: int = last_uid + 1

        user: User = User(
            id=new_uid,
            **data
        )

        self.database.add_data(user.model_dump())
        self.cached_data = self.database.get_data()

    def edit_contact(self, all_users: list) -> None:
        """
        Save edited data to the database
        Args:
            all_users: list with updated data
        Returns:
             None
        """
        new_all_users: list = [user.model_dump() for user in all_users]

        self.database.save_data(new_all_users)
        self.cached_data = self.database.get_data()

    def search_contact_by_id(self, uid: int) -> tuple[list[User], User]:
        """
        Search single contact in the database by given uid
        Args:
            uid: uid of contact
        Returns:
            - list with all contacts
            - founded single contact instance
        """
        all_users: list[User] = [User(**user_data) for user_data in self.cached_data]
        selected_user: User = list(filter(lambda user: user.id == uid, all_users))[0]

        return all_users, selected_user

    def global_search(self, request: str) -> list:
        """
        Searches for all matches of the input string
        Args:
            request: string to search
        Returns:
            list with all matches
        """
        all_contacts: list = [User(**user_data) for user_data in self.cached_data]
        result: list = []

        for contact in all_contacts:
            flags: list = []

            for word in request.split():
                if word.strip() in contact.model_dump().values():
                    flags.append(True)
                else:
                    flags.append(False)

            if all(flags):
                result.append(contact)

        return result
