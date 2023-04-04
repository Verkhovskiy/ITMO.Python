D = {'food': 'Apple', 'quantity': 4, 'color': 'Red'}

print(D['food'])

D['quantity'] += 10
print(D['quantity'])

dp = {}
dp.update({'name': input('Input your name -> ')})
dp.update({'age': input('Input your age -> ')})
print(dp)

rec = {'name': {'firstname': 'Bob', 'lastname': 'Smith'},
    'job': ['dev', 'mgr'],
    'age': 25}
rec['job'].append('janitor')

print("""
***** {} {} *****
Age: {}
""".format(rec['name']['firstname'], rec['name']['lastname'], rec['age']))