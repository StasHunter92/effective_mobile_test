import math
import os

from prettytable.colortable import ColorTable, Theme

from app.classes.phonebook import PhoneBook
from app.settings import CONTACTS_ON_PAGE, FILL_WIDTH


# ----------------------------------------------------------------------------------------------------------------------
# Create classes
class UiInterface:
    """
    Console interface class for the phone book
    """

    def __init__(self, phonebook: PhoneBook, theme: Theme):
        self.phonebook = phonebook
        self.theme = theme

    # --------------------------------------------------------------------------
    def get_all_contacts(self, page_number: int = 1) -> None:
        """
        Render all contacts in the phone book using page pagination
        Args:
            page_number: Integer number of page
        Returns:
            None
        """
        os.system('clear||cls')

        # Settings
        all_users = self.phonebook.get_all_contacts()
        last_rendered_page = page_number
        contacts_on_page: int = CONTACTS_ON_PAGE
        start: int = (page_number - 1) * contacts_on_page
        end: int = start + contacts_on_page
        pages_count: int = math.ceil(len(all_users) / contacts_on_page)

        # Create table
        table = ColorTable(theme=self.theme, min_table_width=100)
        table.field_names = [
            'ID',
            'Фамилия',
            'Имя',
            'Отчество',
            'Организация',
            'Телефон организации',
            'Личный телефон'
        ]

        # Data preparation
        for user in all_users:
            table.add_row(
                [
                    user.id,
                    user.last_name,
                    user.first_name,
                    user.patronymic,
                    user.organization,
                    user.organization_phone_number,
                    user.phone_number
                ]
            )

        # Render table
        print(' СПИСОК КОНТАКТОВ '.center(FILL_WIDTH, '*'))
        print(table.get_string(start=start, end=end))
        print(f'Страница {page_number} из {pages_count if pages_count else 1}')

        # Wait for user input
        select: str = input('Введите номер страницы или нажмите ENTER для возврата в меню: ')

        # Input processing
        if select == '':
            pass
        else:
            try:
                page_number: int = int(select)
                if 0 < page_number <= pages_count:
                    self.get_all_contacts(page_number)
                else:
                    os.system('clear||cls')

                    print(' СПИСОК КОНТАКТОВ '.center(FILL_WIDTH, '*'))
                    print(f'ОШИБКА! Некорректный номер страницы!')
                    input('Нажмите ENTER, чтобы вернуться назад ')

                    self.get_all_contacts(last_rendered_page)
            except ValueError:
                os.system('clear||cls')

                print(' СПИСОК КОНТАКТОВ '.center(FILL_WIDTH, '*'))
                print(f'ОШИБКА! Номер страницы должен быть целым числом!')
                input('Нажмите ENTER, чтобы вернуться назад ')

                self.get_all_contacts(last_rendered_page)

    # --------------------------------------------------------------------------
    def search_contact(self) -> None:
        """
        Search contact in the phone book by one or more criteria
        and render result
        Returns:
            None
        """
        os.system('clear||cls')

        # Create table
        table = ColorTable(theme=self.theme, min_table_width=100)
        table.field_names = [
            'ID',
            'Фамилия',
            'Имя',
            'Отчество',
            'Организация',
            'Телефон организации',
            'Личный телефон'
        ]

        # Render search field
        print(' ПОИСК КОНТАКТА '.center(FILL_WIDTH, '*'))
        request = input('Введите данные для поиска: ')
        result = self.phonebook.global_search(request)

        # Data preparation
        for user in result:
            table.add_row(
                [
                    user.id,
                    user.last_name,
                    user.first_name,
                    user.patronymic,
                    user.organization,
                    user.organization_phone_number,
                    user.phone_number
                ]
            )

        # Render result
        print(table)
        input('Нажмите ENTER для возврата в меню ')

    # --------------------------------------------------------------------------
    def add_contact(self) -> None:
        """
        Add a contact to the phonebook
        Returns:
            None
        """
        os.system('clear||cls')

        # Render input fields
        print(' ДОБАВЛЕНИЕ КОНТАКТА '.center(FILL_WIDTH, '*'))
        new_user_data: dict[str, str] = {
            'last_name': input('Фамилия: '),
            'first_name': input('Имя: '),
            'patronymic': input('Отчество: '),
            'organization': input('Организация: '),
            'organization_phone_number': input('Телефон организации: '),
            'phone_number': input('Личный телефон: '),
        }

        # Save user data
        self.phonebook.add_contact(new_user_data)

    # --------------------------------------------------------------------------
    def edit_contact(self) -> None:
        """
        Edit contact information in selected field
        Returns:
             None
        """
        table = ColorTable(theme=self.theme, min_table_width=100)
        os.system('clear||cls')

        # Render input field
        print(' ИЗМЕНЕНИЕ КОНТАКТА '.center(FILL_WIDTH, '*'))
        request: str = input('Введите ID пользователя: ')

        try:
            uid: int = int(request)
            all_users, selected_user = self.phonebook.search_contact_by_id(uid)
            table.add_column(
                f'Вы выбрали изменить данные контакта: '
                f'{selected_user.last_name} '
                f'{selected_user.first_name} '
                f'{selected_user.patronymic}',
                [
                    '1) Изменить имя'.ljust(96),
                    '2) Изменить фамилию'.ljust(96),
                    '3) Изменить отчество'.ljust(96),
                    '4) Изменить организацию'.ljust(96),
                    '5) Изменить телефон организации'.ljust(96),
                    '6) Изменить личный телефон'.ljust(96)
                ]
            )

            # Render edit choices
            os.system('clear||cls')
            print(' ИЗМЕНЕНИЕ КОНТАКТА '.center(FILL_WIDTH, '*'))
            print(table)

            # Field choice
            fields: dict = {
                '1': lambda: setattr(
                    selected_user,
                    'first_name',
                    input('Введите новое имя: ')
                ),
                '2': lambda: setattr(
                    selected_user,
                    'last_name',
                    input('Введите новую фамилию: ')
                ),
                '3': lambda: setattr(
                    selected_user,
                    'patronymic',
                    input('Введите новое отчество: ')
                ),
                '4': lambda: setattr(
                    selected_user,
                    'organization',
                    input('Введите новую организацию: ')
                ),
                '5': lambda: setattr(
                    selected_user,
                    'organization_phone_number',
                    input('Введите новый телефон организации: ')
                ),
                '6': lambda: setattr(
                    selected_user,
                    'phone_number',
                    input('Введите новый личный телефон: ')
                ),
            }

            # Wait for user input
            select: str = input('Выберите данные для изменения: ')

            if select in fields:
                fields[select]()

                # Save changes
                self.phonebook.edit_contact(all_users)
            else:
                os.system('clear||cls')

                print(' ИЗМЕНЕНИЕ КОНТАКТА '.center(FILL_WIDTH, '*'))
                print(f'ОШИБКА! Выбранного пункта не существует!')
                input('Нажмите ENTER для возврата в меню: ')

        except (ValueError, IndexError):
            os.system('clear||cls')

            print(' ИЗМЕНЕНИЕ КОНТАКТА '.center(FILL_WIDTH, '*'))
            print(f'ОШИБКА! Выбранного контакта не существует!')
            input('Нажмите ENTER для возврата в меню: ')

    # --------------------------------------------------------------------------
    def main_menu(self) -> None:
        """
        Render main menu of the phone book
        Returns:
             None
        """
        os.system('clear||cls')

        # Create table
        table = ColorTable(theme=self.theme)
        table.add_column(
            'ГЛАВНОЕ МЕНЮ',
            [
                '1) Показать все контакты'.ljust(96),
                '2) Поиск по контактам'.ljust(96),
                '3) Добавить контакт'.ljust(96),
                '4) Изменить контакт'.ljust(96),
                'Q) Выйти из приложения'.ljust(96)
            ]
        )

        # Create options
        options: dict = {
            '1': self.get_all_contacts,
            '2': self.search_contact,
            '3': self.add_contact,
            '4': self.edit_contact,
            'Q': exit,
        }

        # Render main menu
        print(' ТЕЛЕФОННЫЙ СПРАВОЧНИК '.center(FILL_WIDTH, '*'))
        print(table)

        # Wait for user input
        select = input('Выберите действие: ')

        # Select option
        if select in options:
            options[select]()
