
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

#=====================================================================================

def GetText():
  
  """Returns text of the lesson."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lessons/'+LESSON+'/text/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Request data
  r = requests.get(url = URL, headers = headers)
  
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

def ChangeLingQStatus(idlingq,status,extended_status):
  
  """Takes LingQ id and a status, changes status remotely."""
  
  # Set the URL for this task
  URL = 'https://www.lingq.com/api/languages/'+LANGUAGE+'/lingqs/'+str(idlingq)+'/'
  
  # Authorisation stuff
  headers = {'Authorization': 'Token {}'.format(API_KEY)}
  
  # Params for changing the LingQ
  params = {'status':status,'extended_status':extended_status}
  
  # Function for put
  def put():
    r = requests.put(url = URL, data=params, headers = headers)
  
  # Make change without waiting for it to finish
  p = mp.Process(target=put)
  p.daemon = True
  p.start()
  
  return

#=====================================================================================
