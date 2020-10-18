
"""
Wikipedia module for LingQ reader.
"""

import wikipedia as wiki
import LingQapi as lingqapi
import numpy as np
import sys

wiki.set_lang("de") 

MAX_WORD_LESSON = 1750

# Collection to upload lessons to
DEFAULT_COLLECTION = 713861
#=====================================================================================

def SetupWikiArticle(article):
  
  # Get article 
  page = GetWikiArticle(article)
  
  # Get title
  title = page.title
  
  # Get content of lesson
  text = page.content
  
  # Fix missing paragraph issue
  text = text.replace('. ','AAAAA')
  text = text.replace('.','\n')
  text = text.replace('AAAAA','. ')
  
  # Remove a couple of things not needed
  text = text.replace('&lt;\p&gt;','')
  
  # Split the lesson
  text_lessons = SplitText(text)
  
  # Get titles for each lesson
  if len(text_lessons) > 1:
    titles = []
    for i in range(0,len(text_lessons)):
      titles.append(title+' ('+str(i)+')')
  else:
    titles = [title]
  
  # Upload to LingQ
  for i in range(0,len(text_lessons)):
    contentId = lingqapi.UploadLesson(titles[i],text_lessons[i],DEFAULT_COLLECTION)
  
  # Open the lesson
  lingqapi.open_lesson(contentId)
  
  return contentId

#=====================================================================================

def SplitText(text):
  
  # Split lesson text by paragraph
  paragraphs = text.split('\n')
  nParagraphs = len(paragraphs)
  
  # Make list for holding lesson strings
  text_lessons = []
  
  # Loop over paragraphs and add them to the text for each lesson
  text_lesson = ''
  nWords = 0
  for paragraph in paragraphs:
    
    # Get paragraph split by word
    paragraphSplit = paragraph.split()
    
    # If this paragraph is longer than the word limit, output error
    if len(paragraphSplit) > MAX_WORD_LESSON:
      print("PARAGRAPH TOO LONG - FIND SOLUTION")
      print(len(paragraph.split()))
      sys.exit()
    
    # If adding this paragraph does not cause length of lesson to be too long
    # then add it, otherwise move onto next lesson
    if ( nWords+len(paragraphSplit) <= MAX_WORD_LESSON ):
      text_lesson += '<p>' + paragraph+' <\p> '
      nWords += len(paragraphSplit)
    else:
      if not text_lesson == '':
        text_lessons.append(text_lesson)
      text_lesson = ''
      nWords = 0
  
  return text_lessons

#=====================================================================================

def GetWikiArticle(article):
  return wiki.page(article)

#=====================================================================================
