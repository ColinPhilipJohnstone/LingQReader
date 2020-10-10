
"""
Functions for using the LingQ API.
"""

import requests
import json
import multiprocessing as mp

# API key for my account
API_KEY = "408fa561d040f932be1f3303e50e426794fda139"

# Language
LANGUAGE = 'de'

# Lesson
#LESSON = '4983458' # longer
#LESSON = '35644' # shorter
LESSON = '5113948' # really short

# Dictionary for saving hints that have already been looked for
unknown_hints = {}

#=====================================================================================

def GetText():
  
  """Returns text of the lesson."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lessons/'+LESSON+'/text/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  print('a')
  r = requests.get( url=URL , headers=headers )
  print('b')
  # Get text
  data = r.json() 
  text = data['text']
  
  # Do a simple replace
  text = text.replace('</p><p>',' </p><p> ')
  
  return text

#=====================================================================================

def GetUnknownWords():
  
  """Get's unknown words from lesson."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lessons/'+LESSON+'/words/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get(url = URL, headers = headers) 
  
  # Get list
  data = r.json()
  data = data['unknown']
  
  # Get dictionary with each term and index in list of LingQ for this term
  unknownList = []
  for word in data:
    unknownList.append(word['word'])
  
  print(unknownList)
  
  return unknownList

#=====================================================================================

def GetLingQs():
  
  """Get's LingQs for a lesson."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lessons/'+LESSON+'/lingqs/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get(url = URL, headers = headers) 
  
  # Get LingQs
  lingqs = r.json()
  
  # Get dictionary with each term and index in list of LingQ for this term
  lingqsDict = {}
  index = 0
  for lingq in lingqs:
    term = lingq['term']
    lingqsDict[term] = index
    index += 1
  
  return lingqsDict , lingqs

#=====================================================================================

def GetLingQHints(word):
  global unknown_hints
  
  """Retrieves hints for a word."""
  
  if word in unknown_hints:
    
    hints = unknown_hints[word]
  
  else:
    
    # Set the URL for this task
    URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/hints/?word='+word
    
    # Authorisation stuff
    headers = {'Authorization': 'Token {}'.format(API_KEY)}
    
    # Request data
    r = requests.get(url = URL, headers = headers) 
    
    # Get list of hints for this word
    hints = r.json()
    hints = hints[word]
    
    # Save these hints so don't have to look again
    unknown_hints[word] = hints
  
  return hints

#=====================================================================================

def GetLingQHintsList(word_list):
  global unknown_hints
  
  """Retrieves hints for all words in a list of words."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/hints/?'
  
  # Loop over words and add each to URL
  for word in word_list:
    URL += 'word='+word + '&'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get(url = URL, headers = headers) 
  
  # Get dictionary with each word
  data = r.json()
  
  # Loop over words and add hint list for each
  for word in word_list:
    unknown_hints[word] = data[word]
  
  return

#=====================================================================================

def put(URL,headers,params):
  """Takes URL, headers, and params, performs requests.put()."""
  r = requests.put(url = URL, data=params, headers = headers)
  return

def post(URL,headers,params):
  """Takes URL, headers, and params, performs requests.put()."""
  r = requests.post(url = URL, json=params, headers = headers)
  return

#=====================================================================================

def ChangeLingQStatus(idlingq,status,extended_status):
  
  """Takes LingQ id and a status, changes status remotely."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lingqs/'+str(idlingq)+'/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Params for changing the LingQ
  params = {'status':status,'extended_status':extended_status}
  
  # Make change without waiting for it to finish
  p = mp.Process(target=put,args=(URL,headers,params))
  p.daemon = True
  p.start()
  
  return

#=====================================================================================

def CreateLingQ(word,hint_text):
  
  """Retrieves hints for all words in a list of words."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lingqs/'
  
  # Authorisation stuff
  headers = { 'Authorization':'Token {}'.format(API_KEY) , 'Content-Type':'application/json' }
  
  # Params for creating the LingQ
  params = { "hints":[{"locale": "en", "text":hint_text}] , "term": word , "lesson":LESSON }
  
  # Do post
  r = requests.post(url=URL, headers=headers, json=params)
  
  # Get id
  data = r.json()
  idlingq = data['id']
  
  # Make change without waiting for it to finish
  #p = mp.Process(target=post,args=(URL,headers,params))
  #p.daemon = True
  #p.start()
  
  return idlingq

#linguist@qa:~ % curl -X POST -d '{"status": 3, "fragment": "siete", \
#"hints": [{"locale": "en", "text": "hour"}], "term": "siete horas"}' \
#'https://www.lingq.com/api/languages/es/lingqs/' -H 'Authorization: Token bd894eabcd4c0' -H "Content-Type: application/json"
#{"id": 4678901}

#curl -X POST -d '{"hints":[{"locale": "en", "text": "a test hint"}], "term": "atestword", "lesson": 5113948}' 
#'https://www.lingq.com/api/languages/de/lingqs/' -H 'Authorization: Token 408fa561d040f932be1f3303e50e426794fda139' -H "Content-Type: application/json"

#=====================================================================================

def IgnoreWord(word):
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/ignored-words/'
  
  # Authorisation stuff
  headers = { 'Authorization':'Token {}'.format(API_KEY) }
  
  # Params for creating the LingQ
  params = { 'word':word }
  
  # Do post
  r = requests.post(url=URL, headers=headers, data=params)
  
  # Make change without waiting for it to finish
  #p = mp.Process(target=post,args=(URL,headers,params))
  #p.daemon = True
  #p.start()
  
  return


#=====================================================================================
