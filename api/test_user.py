from requests import get, post, delete
from pprint import pprint


# правильный зaпрос
pprint(get('http://127.0.0.1:8000/api/users/2').json())
print('\033[32m!!!!!!!!!!!!!!!!\033[0m')
# запрос к несуществующему пользователю
pprint(get('http://127.0.0.1:8000/api/users/99').json())
print('\033[32m!!!!!!!!!!!!!!!!\033[0m')
# правильный запрос ко всем пользователям
pprint(get('http://127.0.0.1:8000/api/users').json())
print('\033[32m!!!!!!!!!!!!!!!!\033[0m')
# правльный запрос
pprint(post('http://127.0.0.1:8000/api/users',
       json={
            'surname': 'sur',
            'name': 'nam',
            'age': 1,
            'hometown': 'larisa',
            'position': 'pos',
            'speciality': 'spec',
            'address': 'add',
            'email': 'em@mail',
            'password': 'pas'
            }).json())
print('\033[32m!!!!!!!!!!!!!!!!\033[0m')

print('\033[32m!!!!!!!!!!!!!!!!\033[0m')
# запрос без обязательных значенией
pprint(post('http://127.0.0.1:8000/api/users',
       json={
            'surname': 'sur',
            'name': 'nam',
            'age': 1,
            'hometown': 'larisa',
            'email': 'em@mail',
            'password': 'pas'
            }).json())
print('\033[32m!!!!!!!!!!!!!!!!\033[0m')

pprint(delete('http://127.0.0.1:8000/api/users/7').json())
print('\033[32m!!!!!!!!!!!!!!!!\033[0m')
