class Camera:
    """Класс, отвечающий за создание камеры, привязанной к рециркулятору по id"""
    id: int
    size_of_room: int

    def __init__(self, number, size_of_room):
        self.id = number
        self.size_of_room = size_of_room