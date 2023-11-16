from pymongo import MongoClient
from datetime import datetime
from itertools import combinations
from ..web_db.settings import DATABASES


def get_db_handle():
    client = MongoClient(
        host=DATABASES['host'],
        port=DATABASES['port'],
        username=DATABASES['user'],
        password=DATABASES['password']
    )
    db_handle = client[DATABASES['db_name']]
    return db_handle


class ValidForm:
    def __init__(self, value):
        self.value = value
        self.type_form = self.valid_date()

    def valid_date(self):
        try:
            datetime.strptime(self.value, '%Y-%m-%d')
            return 'date'
        except ValueError:
            try:
                datetime.strptime(self.value, '%d.%m.%Y')
                return 'date'
            except ValueError:
                return self.valid_phone()

    def valid_phone(self):
        if (self.value.startswith('+7') and len(self.value) ==
                12 and self.value[2:].isdigit()):
            return 'phone'
        return self.valid_email()

    def valid_email(self):
        parts = self.value.split('@')
        if len(parts) == 2 and '.' in parts[1]:
            return 'email'
        return 'text'


def find_forms(db, request):
    result = []
    if request:
        for count_field_in_find in range(1, len(request) + 1):
            iter_find = combinations(request.items(), count_field_in_find)
            iter_find = map(dict, iter_find)
            for comb in iter_find:
                list_form = db.find(comb, {'_id': 0})
                result += (filter(lambda x: len(x) == count_field_in_find + 1,
                                  list_form))
    return result
