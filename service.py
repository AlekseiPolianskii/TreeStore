from exceptions import IndexDuplicateException, IndexOutOfRangeException


class TreeStore:
    """
    Класс преобразует список словарей в дерево.
    """

    def __init__(self, data: list):
        self._data: list = data
        self.__tree_information: dict = self.__build_tree_information()

    def get_all(self) -> list:
        """
        Возвращает все элементы переданные при инициализации

        :return:
        """
        return self._data

    def get_item(self, id_item: int) -> dict:
        """
        Получение элемента по id

        :param id_item: id требуемого элемента
        :return:
        """
        self.__check_id(id_item)
        return self.__get_element_by_id(id_item)

    def get_all_parents(self, id_item: int) -> list:
        """
        Возвращает рекурсивно всех parent начиная
        с переданного id элемента

        :param id_item: id первого элемента
        :return:
        """
        self.__check_id(id_item)
        result = self.__collect_parents(id_item)
        return result

    def get_children(self, id_item: int) -> list:
        """
        Возвращает все children элементы

        :param id_item: id элемента
        :return:
        """
        self.__check_id(id_item)
        result = []
        for index in self.__tree_information[id_item]["children"]:
            result.append(self._data[index])
        return result

    def __collect_parents(self, id_item) -> list:
        """
        Собирает массив с элементами parent

        :param id_item: id элемента цели
        :return:
        """
        result = []
        for _ in range(len(self._data)):
            item = self.__get_element_by_id(id_item)
            result.append(item)
            if item["parent"] == "root":
                break
            id_item = item["parent"]
        return result

    def __check_id(self, id_item: int) -> None:
        """
        Проверка переданного id

        :param id_item: проверяемый id
        :return:
        """
        if (
                not isinstance(id_item, int)
                or id_item not in self.__tree_information.keys()
        ):
            raise IndexOutOfRangeException(
                f"Element with ID {id_item} is not in the transmitted data"
            )

    def __get_element_by_id(self, id_item) -> dict:
        """
        Получение элемента по id

        :param id_item: id требуемого элемента
        :return:
        """
        index_ = self.__tree_information[id_item]["index"]
        return self._data[index_]

    def __build_tree_information(self) -> dict:
        """
        Функция по переданному массиву формирует словарь с
        информацией для получения данных

        :return:
        """
        information = {
            "root": {"index": None, "parent": None, "children": []}
        }
        for index, item in enumerate(self._data):
            if item["id"] in information.keys():
                raise IndexDuplicateException(
                    f"ID {item['id']} is duplicated in the transmitted data"
                )
            self.__set_index_to_parent(item, index, information)
            self.__add_element_to_information(index, information, item)
        return information

    def __add_element_to_information(
            self, index: int, information: dict, item: dict
    ) -> None:
        """
        Формирует элемент с информацией об элементах

        :param index: index в переданных данных
        :param information: словарь с информацией о данных
        :param item: текущий элемент
        :return:
        """
        item_information = information.get(item["id"], {
            "index": index,
            "parent": None,
            "children": []
        })
        item_information["index"] = index
        item_information["parent"] = self.__get_index_parent(item["parent"])
        information[item["id"]] = item_information

    @staticmethod
    def __set_index_to_parent(item: dict, index: int, information: dict) -> None:
        """
        Добавление index в поле children у parent

        :param item: текущий элемент
        :param index: индекс текущего элемента
        :param information: словарь с информацией о данных
        :return:
        """
        if item["parent"] in information.keys():
            information[item["parent"]]["children"].append(item["id"])
        else:
            information[item["parent"]] = {
                "index": None,
                "parent": None,
                "children": [index]
            }

    def __get_index_parent(self, id_parent: int | str) -> int:
        """
        Получение индекса parent в массиве данных

        :param id_parent: id parent
        :return:
        """
        if id_parent == "root":
            return 0
        for index, item in enumerate(self._data):
            if item["id"] == id_parent:
                return index
        raise IndexDuplicateException(
            f"There is no element with ID {id_parent} in the transmitted data"
        )
