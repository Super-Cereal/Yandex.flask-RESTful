from requests import get, post, delete


# правильный зaпрос
print(get('http://127.0.0.1:8000/api/jobs/2').json())
print('\033[32m--------\033[0m')
# запрос к несуществующей работе

print(get('http://127.0.0.1:8000/api/jobs/99').json())
print('\033[32m--------\033[0m')
# правильный запрос ко всем работам
print(get('http://127.0.0.1:8000/api/jobs').json())
print('\033[32m--------\033[0m')
# правильный запрос
print(post('http://127.0.0.1:8000/api/jobs',
      json={
           'job': 'job',
           'team_leader': '3',
           'work_size': '123',
           'collaborators': '1, 2, 3',
           'is_finished': False
           }).json())

print('\033[32m--------\033[0m')
# запрос без обязательных значенией
print(post('http://127.0.0.1:8000/api/jobs',
      json={
           'job': 'job',
           'work_size': 123,
           'collaborators': '1, 2, 3',
           'is_finished': False
           }).json())
print('\033[32m--------\033[0m')
# правильноее удаление работы
print(delete('http://127.0.0.1:8000/api/jobs/4').json())
print('\033[32m--------\033[0m')
