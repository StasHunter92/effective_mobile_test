from app.classes.interface import UiInterface
from app.classes.phonebook import PhoneBook
from app.settings import my_theme

# ----------------------------------------------------------------------------------------------------------------------
# Create instances
phonebook = PhoneBook('app/database/book.json')
interface = UiInterface(phonebook, my_theme)
