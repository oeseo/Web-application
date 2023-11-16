import requests


HOST_URL = 'http://localhost:8081'
FIELDS_FOR_FIND = [{'new_email': 'ali301194@me.com',
                    'email': 'ali301194@me.com'},

                   {'new_email': 'ali301194@me.com',
                    'email': 'ali301194@me.com',
                    'first_name': 'Alexander',},
                   {'new_email': 'ali301194@me.com',
                    'email': 'ali301194@me.com',
                    'first_name': 'Alexander',
                    'date':'30.11.1994'},
                   {},
                   {'empty':'Sometimes not empty',
                    'lazy_day': '2023-11-16'}
                   ]


def get_form(field_for_find):
    print(field_for_find)
    response2 = requests.post(f'{HOST_URL}/get_form', data=field_for_find)
    print(response2.content.decode('utf-8'))


if __name__ == '__main__':
    response = requests.get(HOST_URL)

    if response.status_code == 200:

        print('Список шаблонов в базе данных',
              response.content.decode('utf-8').replace('</br>', '\n'),
              'Сервер успешно открыт, направляем POST запрос ',
              sep='\n')

        for n in range(len(FIELDS_FOR_FIND)):
            print(f'\n№{n+1}')
            get_form(FIELDS_FOR_FIND[n])
    else:
        print('Сервер отключен')
