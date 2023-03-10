import allure
import pytest
from jsonschema import validate
import variables
from utils.api import Library_api
from utils.checking import Checking
from utils.schemas.post import POST_SCHEMA


@allure.epic("Test crate new book")
class Test_create_book:
    """Класс для тестирования API"""

    @pytest.mark.development
    @allure.description("Test crate, update, delete new book")
    def test_create_new_book(self):
        """Тест на создание, изменение и удаление новой книги, все поля заполнены и валидны"""

        print('Method POST - метод создание новой книги')

        result_post = Library_api.create_new_book(variables.json_all_valid_param)
        check_post = result_post.json()
        book_id = str(check_post.get("book")["id"])  # получаем id новой книги
        Checking.check_status_code(result_post, 201)
        Checking.check_json_token(result_post, ['book'])
        validate(check_post, POST_SCHEMA)

        print("Method GET after POST - метод для проверки создания новой книги")

        result_get = Library_api.get_new_book(book_id)
        check_get = result_get.json()
        list_check_value = list(check_get.get("book"))  # получаем список значений словаря "book"
        Checking.check_status_code(result_get, 200)
        Checking.check_value(list_check_value, 'name')

        print("Method PUT - метод для изменения новой книги")

        result_put = Library_api.put_new_book(variables.json_all_valid_param_4)
        check_put = result_put.json().get("book")["name"]  # получаем значение обязательного поля "name"
        Checking.check_status_code(result_put, 200)
        Checking.check_name_value(check_put, 'Евгений Онегин')

        print("Method GET after PUT - метод для проверки изменения инфы о новой книге")

        result_get = Library_api.get_new_book(book_id)
        check_get = result_get.json().get("book")["name"]
        Checking.check_status_code(result_get, 200)
        Checking.check_name_value(check_get, "Евгений Онегин")

        print("Method DELETE - метод для удаления новой книги")

        result_delete = Library_api.delete_book_with_book_id(book_id)
        Checking.check_status_code(result_delete, 200)
        Checking.check_json_value_token(result_delete, 'result', True)

        print("Method GET after DELETE - метод для проверки удаления новой книги")

        result_get = Library_api.get_new_book(book_id)
        Checking.check_status_code(result_get, 404)
        Checking.check_json_value_token(result_get, 'error', 'Book with id ' + book_id + ' not found')

        print("Тест на создание, изменение и удаление книги прошел успешно!")
