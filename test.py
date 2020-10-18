

import requests

headers = {'Authorization': 'Token 408fa561d040f932be1f3303e50e426794fda139' }
#headers = {'Authorization': 'Token 408fa561d040f932be1f3303e50e426794fda139' , 'Content-Type':'application/json' }

URL = 'https://www.lingq.com/en/learn/de/import/collections/'
#URL = 'https://www.lingq.com/api/languages/de/collections/'
#URL = 'https://www.lingq.com/api/languages/de/collection/'
#URL = 'https://www.lingq.com/api/languages/de/courses/'
#URL = 'https://www.lingq.com/api/languages/de/course/'
#URL = 'https://www.lingq.com/api/v2/de/collections/'


#params = {'title': 'this is my test2', 
          #'lessonsCount':"0", 'sharedByName':"Colin", 
          #'level':"3", 'completedTimes':"0", 
          #'provider':'Colin'}
params = {'title': 'this is my test2'}

r = requests.post( url=URL , headers=headers , data=params )
#r = requests.post( url=URL , headers=headers , json=params )

print(r)
print(r.json())
#print(r.text)

