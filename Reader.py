
"""
Simple game for learning arcade
"""

import arcade
import numpy as np
import time
import sys
import time
import copy
import requests
import requests
import json
import LingQapi as lingqapi
import multiprocessing as mp

#=====================================================================================


#user32 = ctypes.windll.user32
#SCREEN_WIDTH = user32.GetSystemMetrics(0)
#SCREEN_HEIGHT = user32.GetSystemMetrics(1) 

# Some basic values for the window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Colin's LingQ Reader"
FULLSCREEN = False

# Margins
MARGIN_WIDTH = SCREEN_WIDTH/20.0
MARGIN_HEIGHT = SCREEN_HEIGHT/10.0

# Line spacing and paragraph stuff
LINE_SPACE = 40
PARAGRAPH_SPACE = int(LINE_SPACE*1.5)
PARAGRAPH_STRING = '</p>'
FONT_SIZE = 20

# For additional space around word in highlighting
LINGQ_WIDTH_FACTOR = 1.02
LINGQ_HEIGHT_FACTOR = 1.15

# Bubble properties
BUBBLE_WIDTH = int(SCREEN_WIDTH/1.7)
BUBBLE_HEIGHT = int(BUBBLE_WIDTH/1.8)
BUBBLE_MARGIN = int(BUBBLE_WIDTH/20.0)
FONT_SIZE_BUBBLE_TERM = 20
FONT_SIZE_BUBBLE_HINT = 15
BUBBLE_HINT_SPACING = 30
BUBBLE_STATUS_WIDTH = int(min(50,(BUBBLE_WIDTH-2*BUBBLE_MARGIN)/6.0))
BUBBLE_STATUS_HEIGHT = BUBBLE_STATUS_WIDTH
BUBBLE_MAX_HINTS = 3

# Some HUD properties
EXIT_BUTTON_SCALING = 0.1

# Colors 
LINGQ_HIGHLIGHT_COLOR_1 = (255,255,0,255)
LINGQ_HIGHLIGHT_COLOR_2 = (255,255,0,120)
LINGQ_HIGHLIGHT_COLOR_3 = (255,255,0,55)
LINGQ_HIGHLIGHT_COLOR_4 = (255,255,0,0)
LINGQ_BUBBLE_COLOR = arcade.color.LIGHT_GOLDENROD_YELLOW
LINGQ_BUBBLE_STATUS_COLOR = arcade.color.AZURE_MIST
LINGQ_BUBBLE_STATUS_CURRENT_COLOR = arcade.color.BLUEBERRY
UNKNOWN_HIGHLIGHT_COLOR = arcade.color.BLIZZARD_BLUE
UNKNOWN_BUBBLE_COLOR = arcade.color.ITALIAN_SKY_BLUE
UNKNOWN_HINT_BOX_COLOR = arcade.color.AZURE_MIST
EXIT_BUTTON_COLOR = arcade.color.RED
WORD_SELECT_BOX_COLOR = arcade.color.RED

# Dictionary for saving text images
text_images_save = {}
lingq_images_save = {}
unknown_images_save = {}


#=====================================================================================

class LingQReader(arcade.Window):
  """
  Main class
  """
  
  #---------------------------------------------------------------
  
  def __init__(self):
    
    self.setup_window()
    
    return
  
  #---------------------------------------------------------------
  
  def setup_window(self):
    global SCREEN_WIDTH , SCREEN_HEIGHT
    
    """Sets up the window."""
    
    # Call the parent class initializer
    super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,fullscreen=FULLSCREEN)
    
    # Get new size if fullscreen
    if FULLSCREEN:
      SCREEN_WIDTH, SCREEN_HEIGHT = self.get_size()
  
    # Set background color
    arcade.set_background_color(arcade.color.WHITE)
    
    return
  
  #---------------------------------------------------------------
  
  def setup_lesson(self):
    
    # Load full text
    self.text = lingqapi.GetText()
        
    # Load LingQs in text
    self.lingqsDict , self.lingqs = lingqapi.GetLingQs()
    
    # Load unknown words
    self.unknownList , self.unknownIdDict = lingqapi.GetUnknownWords()
    
    # Get hints for unknown words and for LingQs
    lingqapi.GetLingQHintsList(self.unknownList)
    lingqapi.GetLingQHintsList(dict_to_list(self.lingqsDict))
    
    # Setup text
    self.page_word_list = self.setup_text()
    self.nPages = len(self.page_word_list)
    
    # Setup LingQs and unknown
    self.page_lingq_list = self.setup_lingqs()
    self.page_unknown_list = self.setup_unknown()
    
    # Setup HUD on page
    self.exit_button_list = self.setup_page_hud()
    self.hud_sprite_list , self.hud_shape_list = self.setup_page_hud()
    
    # Start on first page
    self.nPageCurrent = 0
    
    # Assume no bubble to display
    self.displayBubble = None
    
    # Assume not showing the hud
    self.showHud = False
    
    # Assuming not clicking change status button
    self.clickingStatus = False
    
    # Assume no word select box to display 
    self.wordSelectBox = None
    
    return
  
  #---------------------------------------------------------------
  
  def setup_text(self):
    
    # Start list of word lists for each page
    page_word_list = []
    
    # Get list of words
    words = self.text.split()
    
    # Position of first word
    xLeft = MARGIN_WIDTH
    yCenter = SCREEN_HEIGHT-MARGIN_HEIGHT
    
    # Width of page
    space_image = get_text_image(text=' ')
    SPACE_WIDTH = space_image.width
    
    # Make a first word list
    word_list = arcade.SpriteList()
    
    # Start page counter
    nPage = 0
    
    # Loop over all words in the text
    for word in words:
      
      # Check if this word is a paragraph indicator
      if word == PARAGRAPH_STRING:
        xLeft = MARGIN_WIDTH
        yCenter += -PARAGRAPH_SPACE
        continue
      
      # Made image out of word
      image = get_text_image(text=word)
      
      # Make sprite from image
      word_sprite = WordSprite()
      word_sprite.SetWord(word)
      word_sprite._texture = arcade.Texture(word)
      word_sprite.texture.image = image
      word_sprite.width = image.width
      word_sprite.height = image.height
      
      # Check if need to move to next line
      word_right = xLeft + word_sprite.width
      if ( word_right > SCREEN_WIDTH-MARGIN_WIDTH ):
        xLeft = MARGIN_WIDTH
        yCenter += -LINE_SPACE
      
      # Check if need to move to next page
      if yCenter < MARGIN_HEIGHT:
        
        # Save this word list
        page_word_list.append(word_list)
        
        # Start new word list
        word_list = arcade.SpriteList()
        
        # Reset positions for next page
        xLeft = MARGIN_WIDTH
        yCenter = SCREEN_HEIGHT-MARGIN_HEIGHT
      
      # Set position of word
      word_sprite.center_x = xLeft + word_sprite.width / 2
      word_sprite.center_y = yCenter
      
      # Add word to word list
      word_list.append(word_sprite)
      
      # Update x position
      xLeft += word_sprite.width + SPACE_WIDTH
    
    # Add final page
    page_word_list.append(word_list)
    
    return page_word_list
    
  #---------------------------------------------------------------
  
  def setup_lingqs(self):
    
    # Start list for sprite lists
    page_lingq_list = []
    
    # Loop over pages and get linqs on each
    for word_list in self.page_word_list:
      
      # Make sprite list for holding LingQs
      lingq_list = arcade.SpriteList()
      
      # Loop over words in word_list and check each one against LingQs
      for word_sprite in word_list.sprite_list:
        
        # Check if this is a LingQ
        if word_sprite.word in self.lingqsDict:
          
          # Get the LingQ
          index = self.lingqsDict[word_sprite.word]
          lingq = self.lingqs[index]
          
          # Make image for this LingQ
          image = get_lingq_image(text=word_sprite.wordRaw,status=lingq['status'],extended_status=lingq['extended_status'])
          
          # Make sprite for this LingQ
          lingq_sprite = WordSprite()
          lingq_sprite.SetWord(word_sprite.wordRaw)
          lingq_sprite._texture = arcade.Texture(word_sprite.wordRaw)
          lingq_sprite.texture.image = image
          lingq_sprite.width = word_sprite.width*LINGQ_WIDTH_FACTOR
          lingq_sprite.height = word_sprite.height*LINGQ_HEIGHT_FACTOR
          lingq_sprite.center_x = word_sprite.center_x
          lingq_sprite.center_y = word_sprite.center_y
          
          # Add this word as a LingQ
          lingq_list.append(lingq_sprite)
      
      # Append this list to page_lingq_list
      page_lingq_list.append(lingq_list)
    
    return page_lingq_list
  
  #---------------------------------------------------------------
  
  def setup_unknown(self):
    
    # Start list for sprite lists
    page_unknown_list = []
    
    # Loop over pages and get linqs on each
    for word_list in self.page_word_list:
      
      # Make sprite list for holding LingQs
      unknown_list = arcade.SpriteList()
      
      # Loop over words in word_list and check each one against LingQs
      for word_sprite in word_list.sprite_list:
        
        
        # If this is not a real word, move on to next one
        if word_sprite.word == -1:
          continue
        
        # Check if this is a LingQ
        if word_sprite.word in self.unknownList:
          
          # Make image for this LingQ
          image = get_unknown_image(text=word_sprite.wordRaw)
          
          # Make sprite for this LingQ
          unknown_sprite = WordSprite()
          unknown_sprite.SetWord(word_sprite.wordRaw)
          unknown_sprite._texture = arcade.Texture(word_sprite.wordRaw)
          unknown_sprite.texture.image = image
          unknown_sprite.width = word_sprite.width*LINGQ_WIDTH_FACTOR
          unknown_sprite.height = word_sprite.height*LINGQ_HEIGHT_FACTOR
          unknown_sprite.center_x = word_sprite.center_x
          unknown_sprite.center_y = word_sprite.center_y
          
          # Add this word as a LingQ
          unknown_list.append(unknown_sprite)
      
      # Append this list to page_unknown_list
      page_unknown_list.append(unknown_list)
    
    return page_unknown_list
  
  #---------------------------------------------------------------
  
  def setup_page_hud(self):
    
    
    #---------------------------
    
    # Make sprite and shape lists for hud
    hud_sprite_list = arcade.SpriteList()
    hud_shape_list = arcade.ShapeElementList()
    
    #---------------------------
    # Exit button
    
    # Draw explosion
    exit = arcade.Sprite("data/close_icon.png",EXIT_BUTTON_SCALING)
    exit.center_x = MARGIN_WIDTH
    exit.center_y = SCREEN_HEIGHT - 0.5*MARGIN_HEIGHT
    hud_sprite_list.append(exit)
    
    #---------------------------
    
    
    
    return hud_sprite_list , hud_shape_list
  
  #---------------------------------------------------------------
  
  def on_mouse_press(self, x, y, button, modifiers):
    
    """Take mouse click, determine what to do."""
    
    # Assume initially clicked on blank space
    clickObject = None
    
    # If bubble open, check for click in bubble if not found click
    if clickObject is None:
      if not self.displayBubble is None:
        if self.displayBubble.ClickInBox(x,y):
          
          # Set clicked object identifier
          clickObject = 'bubble'
          
          # If in a LingQ bubble do some stuff
          if type(self.displayBubble).__name__ == 'LingQBubble':
            
            # Check if in a status box and get LingQ id to change status if is
            inStatus = self.displayBubble.ClickInStatus(x,y)
            if not inStatus is None:
              
              # Get info for LingQ to change
              idlingq = self.displayBubble.idLingQ()
              termlingq = self.displayBubble.termLingQ()
              
              # Make change
              self.changeLingQstatus(idlingq,termlingq,inStatus)
              
              # Set clicked object identifier
              clickObject = 'bubblestatus'
              
              # Set identifier for closing on click release
              self.clickingStatus = True
          
          elif type(self.displayBubble).__name__ == 'UnknownBubble':
            
            # Check if in a box of some kind
            inStatus = self.displayBubble.ClickInStatus(x,y)
            
            # If in a hint box, do something
            if type(inStatus) == int:
              
              # Get the term and hint
              term = self.displayBubble.term
              hint = self.displayBubble.hints[inStatus]
              
              # Make LingQ
              self.createLingQ(term,hint)
            
            # If in the known box, set it to known
            if inStatus == 'K':
              term = self.displayBubble.term
              self.makeUnknownKnown(term)
            
            # If in the ignore, ignore the word
            if inStatus == 'X':
              term = self.displayBubble.term
              self.ignoreUnknown(term)
            
      
    # Loop over LingQs on screen 
    if clickObject is None:
      for lingq_sprite in self.page_lingq_list[self.nPageCurrent]:
          
          # Check if click in box of word
          if inBoxSprite(x,y,lingq_sprite):
          
            # Get LingQ
            index = self.lingqsDict[lingq_sprite.word]
            lingq = self.lingqs[index]
            
            # Get hints
            hints = lingq['hints']
            
            # Update clickObject to hold LingQ
            clickObject = 'lingq'
            
            # Make display bubble
            self.displayBubble = LingQBubble(lingq_sprite,lingq)
            
            # Setup word select box on this one
            self.wordSelectBox = self.GetWordSelectBox(lingq_sprite)
            
    # Loop over unknown words on screen if not found click
    if clickObject is None:
      for unknown_sprite in self.page_unknown_list[self.nPageCurrent]:
        
        # Check if click in box of word
        if inBoxSprite(x,y,unknown_sprite):
          
          # Get unknown word
          word = unknown_sprite.word
          
          # Update clickObject to hold unknown
          clickObject = 'unknown'
          
          # Get hints for this word
          hints = lingqapi.GetLingQHints(word)
          
          # Make display bubble
          self.displayBubble = UnknownBubble(unknown_sprite,word,hints)
          
          # Setup word select box on this one
          self.wordSelectBox = self.GetWordSelectBox(unknown_sprite)
            
    # Loop over all words on screen if not found click
    if clickObject is None:
      for word_sprite in self.page_word_list[self.nPageCurrent]:
        
        # Check if click in box of word
        if inBoxSprite(x,y,word_sprite):
        
          # Get word
          word = word_sprite.word
          
          # Update clickObject to hold LingQ
          clickObject = 'word'
          
          # Get hints for this word
          hints = lingqapi.GetLingQHints(word)
          
          # Make display bubble
          self.displayBubble = UnknownBubble(word_sprite,word,hints)
          
          # Setup word select box on this one
          self.wordSelectBox = self.GetWordSelectBox(word_sprite)
          
    # Check for clicking buttons
    if clickObject is None:
      
      # Check for exit button
      if clickedOpenHud(x,y):
        clickObject = 'openHud'
        if self.showHud:
          self.showHud = False
        else:
          self.showHud = True
      
      # Check for previous page
      if clickedPreviousPage(x,y):
        if self.nPageCurrent > 0:
          self.wordSelectBox = None
          self.nPageCurrent += -1
          
      # Check for next page
      if clickedNextPage(x,y):
        if self.nPageCurrent < self.nPages-1:
          self.wordSelectBox = None
          self.nPageCurrent += 1
      
      
    # If the click was on nothing, make sure no bubble
    if clickObject is None:
      self.displayBubble = None
    
    # If the click was in a bubble, remove bubble
    if clickObject == 'bubble':
      self.displayBubble = None
    
    # If anywhere but showHud, make sure hud is not shown
    if not clickObject == 'openHud':
      self.showHud = False
    
    return
  
  #---------------------------------------------------------------
  
  def on_mouse_release(self, x, y, button, modifiers):
    
    # If clicking on status change button, remove bubble 
    if self.clickingStatus:
      self.displayBubble = None
      self.clickingStatus = False
    
    return
    
  #---------------------------------------------------------------
  
  def changeLingQstatus(self,idlingq,termlingq,newstatus):
    
    """Takes LingQ id and changes the status."""
    
    # Holds if should delete LingQ
    shouldDelete = False
    
    # Get status and extended status numbers to change LingQ to
    if newstatus == 0:
      new_status = 0
      new_extended_status = 0
    elif newstatus == 1:
      new_status = 1
      new_extended_status = 0
    elif newstatus == 2:
      new_status = 2
      new_extended_status = 0
    elif newstatus == 3:
      new_status = 3
      new_extended_status = 0
    elif newstatus == 4:
      new_status = 3
      new_extended_status = 3
    elif newstatus == 5:
      shouldDelete = True
      new_status = -1
      new_extended_status = -1
    
    if shouldDelete:
      self.ignoreLingQ(termlingq)
      return
    
    # Get index of this LingQ
    index = self.lingqsDict[termlingq]
    
    # Stop if status change not necessary
    if ( self.lingqs[index]['status'] == new_status ) and ( self.lingqs[index]['extended_status'] == new_extended_status ):
      return
    
    # Change the status in LingQ list
    self.lingqs[index]['status'] = new_status
    self.lingqs[index]['extended_status'] = new_extended_status
    
    # Loop over all words and change images in text
    for iPage in range(0,len(self.page_lingq_list)):
      
      # Start a new sprite list for this page
      sprite_list_new = arcade.SpriteList()
      
      # Loop over LingQs on page
      for iLingQ in range(0,len(self.page_lingq_list[iPage].sprite_list)):
        
        # Get Sprite for this LingQ
        lingq_sprite = self.page_lingq_list[iPage].sprite_list[iLingQ]
        
        # Check if this is one that should be changed
        if lingq_sprite.word == termlingq:
          
          # Make a new image for this LingQ
          image = get_lingq_image(lingq_sprite.wordRaw,new_status,new_extended_status)
          
          # Make sprite for this LingQ
          lingq_spriteNew = WordSprite()
          lingq_spriteNew.SetWord(lingq_sprite.wordRaw)
          lingq_spriteNew._texture = arcade.Texture(lingq_sprite.wordRaw+str(new_status)+str(new_extended_status))
          lingq_spriteNew.texture.image = image
          lingq_spriteNew.width = lingq_sprite.width
          lingq_spriteNew.height = lingq_sprite.height
          lingq_spriteNew.center_x = lingq_sprite.center_x
          lingq_spriteNew.center_y = lingq_sprite.center_y
          
          # Add new sprite to list
          sprite_list_new.append(lingq_spriteNew)
        
        else:
          
          # No change needed so add old sprite to list
          sprite_list_new.append(lingq_sprite)
      
      # Save the new sprite list
      self.page_lingq_list[iPage] = sprite_list_new
    
    # Change status on LingQ
    lingqapi.ChangeLingQStatus(idlingq,new_status,new_extended_status)
    
    return
  
  #---------------------------------------------------------------
  
  def createLingQ(self,term,hint):
    
    """Creates LingQ for a given term"""
    
    # Status for new LingQ
    new_status = 0
    new_extended_status = 0
    
    # Loop over all words and change images
    for iPage in range(0,len(self.page_lingq_list)):
      
      # Start new sprite lists for unknown words  on this page
      unknown_sprite_list_new = arcade.SpriteList()
      lingq_sprite_list_new = arcade.SpriteList()
      
      # Loop over all unknown words on page
      foundWord = False
      for iWord in range(0,len(self.page_unknown_list[iPage].sprite_list)):
        
        # Get sprite for this unknown word
        unknown_sprite = self.page_unknown_list[iPage].sprite_list[iWord]
        
        # Only add to unknown list if not the word making LingQ for
        if not unknown_sprite.word == term:
          unknown_sprite_list_new.append(unknown_sprite)
      
        # If it is the word, add to LingQ sprite list for this page
        if unknown_sprite.word == term:
          
          # Set foundWord so code knows this is not a known or ignored word
          foundWord = True
          
          # Make a new image for this LingQ
          image = get_lingq_image(unknown_sprite.wordRaw,new_status,new_extended_status)
          
          # Make sprite for this LingQ
          lingq_spriteNew = WordSprite()
          lingq_spriteNew.SetWord(unknown_sprite.wordRaw)
          lingq_spriteNew._texture = arcade.Texture(unknown_sprite.wordRaw+str(new_status)+str(new_extended_status))
          lingq_spriteNew.texture.image = image
          lingq_spriteNew.width = image.width
          lingq_spriteNew.height = image.height
          lingq_spriteNew.center_x = unknown_sprite.center_x
          lingq_spriteNew.center_y = unknown_sprite.center_y
          
          # Add new sprite to list
          self.page_lingq_list[iPage].append(lingq_spriteNew)
      
      # If not found then maybe known or ignored word
      if not foundWord:
        for iWord in range(0,len(self.page_word_list[iPage].sprite_list)):
          
          # Get sprite for this unknown word
          word_sprite = self.page_word_list[iPage].sprite_list[iWord]
          
          # If it is the word, add to LingQ sprite list for this page
          if word_sprite.word == term:
            
            # Set foundWord so code knows it was found
            foundWord = True
            
            # Make a new image for this LingQ
            image = get_lingq_image(word_sprite.wordRaw,new_status,new_extended_status)
            
            # Make sprite for this LingQ
            lingq_spriteNew = WordSprite()
            lingq_spriteNew.SetWord(word_sprite.wordRaw)
            lingq_spriteNew._texture = arcade.Texture(word_sprite.wordRaw+str(new_status)+str(new_extended_status))
            lingq_spriteNew.texture.image = image
            lingq_spriteNew.width = image.width
            lingq_spriteNew.height = image.height
            lingq_spriteNew.center_x = word_sprite.center_x
            lingq_spriteNew.center_y = word_sprite.center_y
            
            # Add new sprite to list
            self.page_lingq_list[iPage].append(lingq_spriteNew)
      
      # Save the new sprite list
      self.page_unknown_list[iPage] = unknown_sprite_list_new
    
    # Change the LingQ remotely
    idlingq = lingqapi.CreateLingQ(term,hint['text'])
    
    # Make a dictionary for this LingQ
    LingQdict = {}
    LingQdict['id'] = idlingq
    LingQdict['term'] = term
    LingQdict['word'] = -1
    LingQdict['hints'] = [hint]
    LingQdict['fragment'] = ''
    LingQdict['status'] = new_status
    LingQdict['extended_status'] = new_extended_status
    LingQdict['notes'] = ''
    LingQdict['tags'] = ''
    
    # Add to self.lingqs and self.lingqsDict
    self.lingqs.append(LingQdict)
    self.lingqsDict[term] = len(self.lingqs)-1
    
    # Remove from unknown lists if it is there
    if term in self.unknownList:
      self.unknownList.remove(term)
      self.unknownIdDict.pop(term)
    
    return
  
  #---------------------------------------------------------------
  
  def makeUnknownKnown(self,term):
    
    """Takes term, sets unknown word with this term to known."""
    
    # Loop over pages
    for iPage in range(0,len(self.page_lingq_list)):
      
      # Start new sprite lists for unknown words on this page
      unknown_sprite_list_new = arcade.SpriteList()
      
      # Loop over all unknown words on page
      for iWord in range(0,len(self.page_unknown_list[iPage].sprite_list)):
        
        # Get sprite for this unknown word
        unknown_sprite = self.page_unknown_list[iPage].sprite_list[iWord]
  
        # If this is not the unknown word to make known, add it to the list
        if not unknown_sprite.word == term:
          unknown_sprite_list_new.append(unknown_sprite)
      
      # Save the new sprite list
      self.page_unknown_list[iPage] = unknown_sprite_list_new
      
    # Set to ignored online
    wordid = self.unknownIdDict[term]
    lingqapi.MakeKnownWord(wordid)

    # Remove from unknown lists if it is there
    if term in self.unknownList:
      self.unknownList.remove(term)
      self.unknownIdDict.pop(term)
    
    return
  
  #---------------------------------------------------------------
  
  def ignoreUnknown(self,term):
    
    """Takes term, sets all LingQs with this term to ignored."""
    
    # Loop over pages
    for iPage in range(0,len(self.page_lingq_list)):
      
      # Start new sprite lists for LingQs on this page
      unknown_sprite_list_new = arcade.SpriteList()
      
      # Loop over all unknown words on page
      for iWord in range(0,len(self.page_unknown_list[iPage].sprite_list)):
        
        # Get sprite for this unknown word
        unknown_sprite = self.page_unknown_list[iPage].sprite_list[iWord]
  
        # If this is not the unknown word to delete, add it to the list
        if not unknown_sprite.word == term:
          unknown_sprite_list_new.append(unknown_sprite)
      
      # Save the new sprite list
      self.page_unknown_list[iPage] = unknown_sprite_list_new
      
    # Set to ignored online
    lingqapi.IgnoreWord(term)
    
    # Remove from unknown lists if it is there
    if term in self.unknownList:
      self.unknownList.remove(term)
      self.unknownIdDict.pop(term)
    
    return
  
  #---------------------------------------------------------------
  
  def ignoreLingQ(self,term):
    
    """Takes term, sets all LingQs with this term to ignored."""
    
    # Loop over pages and make sure not LingQ or unknown
    for iPage in range(0,len(self.page_lingq_list)):
      
      # Start new sprite lists for LingQs on this page
      lingq_sprite_list_new = arcade.SpriteList()
      
      # Loop over all LingQs on page
      for iWord in range(0,len(self.page_lingq_list[iPage].sprite_list)):
        
        # Get sprite for this LingQ
        lingq_sprite = self.page_lingq_list[iPage].sprite_list[iWord]
  
        # If this is not the LingQ to delete, add it to the list
        if not lingq_sprite.word == term:
          lingq_sprite_list_new.append(lingq_sprite)
      
      # Save the new sprite list
      self.page_lingq_list[iPage] = lingq_sprite_list_new
      
    # Set to ignored online
    lingqapi.IgnoreWord(term)
    
    return
  
  #---------------------------------------------------------------
  
  def GetWordSelectBox(self,word_sprite):
    
    """Takes word sprite, gets shape to draw around edge to show selection."""
    
    # Get position and dimensions of box
    center_x = word_sprite.center_x
    center_y = word_sprite.center_y
    width = word_sprite.width
    height = word_sprite.height
    
    # Make shape list for select box
    box_shape_list = arcade.ShapeElementList()
    
    # Outline of box
    shape = arcade.create_rectangle_outline(center_x,center_y,width,height,WORD_SELECT_BOX_COLOR,1)
    box_shape_list.append(shape)
    
    return box_shape_list
    
  #---------------------------------------------------------------
  
  def on_draw(self):
    
    # Start rendering
    arcade.start_render()
    
    # Display unknown
    self.page_unknown_list[self.nPageCurrent].draw()
    
    # Display LingQs
    self.page_lingq_list[self.nPageCurrent].draw()
    
    # Display words
    self.page_word_list[self.nPageCurrent].draw()
    
    # Display exit button if required
    if self.showHud:
      self.hud_sprite_list.draw()
      self.hud_shape_list.draw()

    
    # Display bubble if there is one
    if not self.displayBubble is None:
      self.displayBubble.draw()
    
    # Display word select box if there is one
    if not self.wordSelectBox is None:
      self.wordSelectBox.draw()
    
    return

  #---------------------------------------------------------------
  
  def on_update(self,dt):
    
    return
  
  #---------------------------------------------------------------

#=====================================================================================

class WordSprite(arcade.Sprite):
  
  def SetWord(self,word):
    self.wordRaw = word
    self.word = GetBasicWord(word)

#=====================================================================================

def get_text_image(text,text_color=arcade.color.BLACK,font_size=FONT_SIZE,width=0,align="left",font_name=('calibri','arial')):
  global text_images_save
  
  """
  Wrapper for get_text_image in text.py of arcade
  """
  
  # Get identifier for image
  idimage = text+str(text_color)+str(font_size)+str(font_size)
  
  # First try to get the word from the text_images_save dictionary
  try: 
    image = text_images_save[idimage]
  except:
    # Does not exist so make and save it
    image = arcade.get_text_image(text=text,
                          text_color=text_color,
                          font_size=font_size,
                          width=width,
                          align=align,
                          font_name=font_name)
    text_images_save[idimage] = image
    
  return image

#=====================================================================================

def get_lingq_image(text,status,extended_status,text_color=arcade.color.BLACK,font_size=FONT_SIZE,width=0,align="left",font_name=('calibri','arial')):
  global lingq_images_save
  
  """
  Wrapper for get_text_image in text.py of arcade for LingQ images
  """
  
  # Get identifier for the lingq
  idlingq = text+str(status)+str(extended_status)
  
  # First try to get the word from the lingq_images_save dictionary
  if idlingq in lingq_images_save:
    
    # Already made image so just load that
    image = lingq_images_save[idlingq]
    
  else:
    
    # Get color
    if status == 0:
      color = LINGQ_HIGHLIGHT_COLOR_1
    elif status == 1:
      color = LINGQ_HIGHLIGHT_COLOR_2
    elif status == 2:
      color = LINGQ_HIGHLIGHT_COLOR_3
    elif status == 3:
      color = LINGQ_HIGHLIGHT_COLOR_4
    
    # Make image
    image = arcade.get_text_image(text=text,
                          text_color=color,
                          font_size=font_size,
                          width=width,
                          align=align,
                          font_name=font_name,
                          background_color=color)
    
    # Save it
    lingq_images_save[idlingq] = image
    
  return image

#=====================================================================================

def get_unknown_image(text,text_color=arcade.color.BLACK,font_size=FONT_SIZE,width=0,align="left",font_name=('calibri','arial')):
  global unknown_images_save
  
  """
  Wrapper for get_text_image in text.py of arcade for unknown word images
  """
  
  # First try to get the word from the unknown_images_save dictionary
  try: 
    image = unknown_images_save[text]
  except:
    # Does not exist so make and save it
    image = arcade.get_text_image(text=text,
                          text_color=UNKNOWN_HIGHLIGHT_COLOR,
                          font_size=font_size,
                          width=width,
                          align=align,
                          font_name=font_name,
                          background_color=UNKNOWN_HIGHLIGHT_COLOR)
    unknown_images_save[text] = image
    
  return image

#=====================================================================================

def GetBasicWord(string):
  
  """Takes string with word, returns string with punctuation removed and lowercase."""
  
  # Make sure there is at least one real letter in word and return -1 if not
  isWord = False
  for char in string:
    if char.isalpha():
      isWord = True
  if not isWord:
    return -1
      
  # Make deep copy of string 
  word = copy.deepcopy(string)
  
  # Make word lower case
  word = word.lower()
  
  # Check if need to shave characters off edges
  if not ( word[0].isalpha() and word[-1].isalpha() ):
    
    # Loop forward and get first letter
    for i in range(0,len(word),1):
      if word[i].isalpha():
        iStart = i
        break
    
    # Loop backwards and get last letter
    for i in range(len(word)-1,-1,-1):
      if word[i].isalpha():
        iEnd = i
        break
    
    # Get new word
    word = word[iStart:iEnd+1]
  
  return word

#=====================================================================================

def inBoxSprite(x,y,sprite):
  
  """Takes x and y coordinates and a sprite, returns if this is in that spite's box."""
  
  return inBox(x,y,sprite.center_x,sprite.center_y,sprite.width,sprite.height)

#=====================================================================================

def inBox(x,y,center_x,center_y,width,height):
  
  """Takes x and y coordinates and dimensions of box, returns if this is in that box."""
  
  # Initially assume not
  inBox = False
  
  # Get edge coordinates
  xMin = center_x - 0.5*width
  xMax = center_x + 0.5*width
  yMin = center_y - 0.5*height
  yMax = center_y + 0.5*height
  
  # Determine if this is in the box
  if ( x > xMin ) and ( x < xMax ) and ( y > yMin ) and ( y < yMax ):
    inBox = True
  
  return inBox

#=====================================================================================

class UnknownBubble:
  
  #---------------------------------------------------------------
  
  def __init__(self,word_sprite,term,hints):
    
    # Save term and hints
    self.term = term
    self.hints = hints
    
    # Get bubble center coordinates and dimensions
    self.width = BUBBLE_WIDTH
    self.height = BUBBLE_HEIGHT
    self.xCenter , self.yCenter = self.GetBubbleCenter(word_sprite)
    
    # Setup bubble box
    self.bubble_shape_list = self.GetBubbleBox()
     
    # Setup bubble contents
    self.GetBubbleContents(word_sprite,term,hints)
    
    return
  
  
  #---------------------------------------------------------------
  
  def GetBubbleCenter(self,word_sprite):
    
    # By default, put the bubble to the right of the word, but determine if should be to left
    if word_sprite.center_x+self.width > 0.95*SCREEN_WIDTH:
      xCenter = word_sprite.center_x - 0.5*self.width
    else:
      xCenter = word_sprite.center_x + 0.5*self.width
    
    # Move bubble right if off left side of screen
    if ( xCenter - 0.5*self.width ) < MARGIN_WIDTH:
      xCenter = MARGIN_WIDTH + 0.5*self.width
    
    # Move bubble left if off right side of screen
    if ( xCenter + 0.5*self.width ) > SCREEN_WIDTH-MARGIN_WIDTH:
      xCenter = SCREEN_WIDTH - MARGIN_WIDTH - 0.5*self.width
      
    # Be default put bubble below word, but determine if it should be above
    if word_sprite.center_y - self.height < 0.05*SCREEN_HEIGHT:
      # Above
      yCenter = word_sprite.center_y + 0.5*LINE_SPACE + 0.5*self.height
    else:
      # Below
      yCenter = word_sprite.center_y - 0.5*LINE_SPACE - 0.5*self.height
    
    return xCenter , yCenter
  
  #---------------------------------------------------------------
  
  def GetBubbleBox(self):
    
    # Make shape list for bubble
    bubble_shape_list = arcade.ShapeElementList()
    
    # Main box
    shape = arcade.create_rectangle_filled(self.xCenter,self.yCenter,self.width,self.height,UNKNOWN_BUBBLE_COLOR)
    bubble_shape_list.append(shape)
    
    # Outline of box
    shape = arcade.create_rectangle_outline(self.xCenter,self.yCenter,self.width,self.height,arcade.color.BLACK,1)
    bubble_shape_list.append(shape)
    shape = arcade.create_rectangle_outline(self.xCenter,self.yCenter,self.width,self.height,arcade.color.BLACK,1,180.0)
    bubble_shape_list.append(shape)
    
    return bubble_shape_list
  
  #---------------------------------------------------------------
  
  def GetBubbleContents(self,word_sprite,term,hints):
    
    
    #------------------------------------------------
    # TERM
    
    # Make a sprite list for the term
    term_sprite_list = arcade.SpriteList()
    
    # Made image out of word
    image = get_text_image(text=term,font_size=FONT_SIZE_BUBBLE_TERM)
    
    # Make sprite from image
    term_sprite = WordSprite()
    term_sprite.SetWord(term)
    term_sprite._texture = arcade.Texture(term)
    term_sprite.texture.image = image
    term_sprite.width = image.width
    term_sprite.height = image.height
    
    # Set position of word
    term_sprite.center_x = self.xCenter - 0.5*self.width + BUBBLE_MARGIN + 0.5*term_sprite.width
    term_sprite.center_y = self.yCenter + 0.5*self.height - BUBBLE_MARGIN - 0.5*term_sprite.height
    
    # Add word to word list
    term_sprite_list.append(term_sprite)
    
    #------------------------------------------------
    # HINTS
    
    # Make sprite and shape lists for the text
    hint_sprite_list = arcade.SpriteList()
    hint_shape_list = arcade.ShapeElementList()
    
    # Number of hints available 
    nHints = len(hints)
    
    # Number of hints to show
    nHintsShow = min( nHints , BUBBLE_MAX_HINTS )
    
    # Save nHintsShow
    self.nHintsShow = nHintsShow
    
    # Center y position of first hin
    center_y = self.yCenter + 0.2*self.height
    
    # Loop over hints and add each one
    for iHint in range(0,nHintsShow):
      
      # Start hint text
      text = ''
      
      # Start hint with number of multiple hints
      if nHints > 1:
        text += str(iHint+1)+". "
      
      # Add popularity if it is there
      if 'popularity' in hints[iHint]:
        text += "(" + str( hints[iHint]['popularity'] ) + ") "
      
      # Add google if from google
      if 'from_google' in hints[iHint]:
        if hints[iHint]['from_google']:
          text += "(google) "
      
      # Add text of hint
      text += hints[iHint]['text'].replace('\n','')
      
      # Made image out of word
      image = get_text_image(text=text,font_size=FONT_SIZE_BUBBLE_HINT,width=self.width-4*BUBBLE_MARGIN)
      
      # Make sprite from image
      text_sprite = WordSprite()
      text_sprite.SetWord(text)
      text_sprite._texture = arcade.Texture(text)
      text_sprite.texture.image = image
      text_sprite.width = image.width
      text_sprite.height = image.height
      
      # Set position of word
      text_sprite.center_x = self.xCenter - 0.5*self.width + 2*BUBBLE_MARGIN + 0.5*text_sprite.width
      text_sprite.center_y = center_y
      
      # Get center_y of next hint if there is one
      center_y += -BUBBLE_HINT_SPACING-0.5*text_sprite.height
    
      # Add word to list
      hint_sprite_list.append(text_sprite)
      
      # NOW DO THE BOX
      
      # Main box
      shape = arcade.create_rectangle_filled(text_sprite.center_x,text_sprite.center_y,text_sprite.width,text_sprite.height,UNKNOWN_HINT_BOX_COLOR)
      hint_shape_list.append(shape)
      
      # Outline of box
      shape = arcade.create_rectangle_outline(text_sprite.center_x,text_sprite.center_y,text_sprite.width,text_sprite.height,arcade.color.BLACK,1)
      hint_shape_list.append(shape)
      shape = arcade.create_rectangle_outline(text_sprite.center_x,text_sprite.center_y,text_sprite.width,text_sprite.height,arcade.color.BLACK,1,180.0)
      hint_shape_list.append(shape)
      
    
    #------------------------------------------------
    # STATUS
    
    # Make sprite and shape lists for status
    status_sprite_list = arcade.SpriteList()
    status_shape_list = arcade.ShapeElementList()
    
    # Get central y positions of buttons 
    #center_y += -0.5*BUBBLE_STATUS_HEIGHT
    center_y = self.yCenter - 0.5*self.height + BUBBLE_MARGIN + 0.5*BUBBLE_STATUS_HEIGHT
    
    # Get centers of all six buttons in x coordinates
    center_x = []
    center_x.append( self.xCenter + 0.5*self.width - BUBBLE_MARGIN - 0.5*BUBBLE_STATUS_WIDTH )
    center_x.append( center_x[-1] - BUBBLE_STATUS_WIDTH )
    
    # Get text for all six buttons
    button_text = [ 'X' , 'K' ]
    
    # Make letters for each
    for iButton in range(0,len(button_text)):
      
      # Make image out of word
      image = get_text_image(text=button_text[iButton],font_size=FONT_SIZE_BUBBLE_HINT)
      
      # Make sprite from image
      text_sprite = WordSprite()
      text_sprite.SetWord(button_text[iButton])
      text_sprite._texture = arcade.Texture(button_text[iButton])
      text_sprite.texture.image = image
      text_sprite.width = image.width
      text_sprite.height = image.height
      
      # Set position of word
      text_sprite.center_x = center_x[iButton]
      text_sprite.center_y = center_y
      
      # Add word to word list
      status_sprite_list.append(text_sprite)
    
    # Make boxes for each button
    for iButton in range(0,len(button_text)):
      
      # Get color for filled box
      color = LINGQ_BUBBLE_STATUS_COLOR
      
      # Make filled box
      shape = arcade.create_rectangle_filled(center_x[iButton],center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT,color)
      status_shape_list.append(shape)
      
      # Outline of box
      shape = arcade.create_rectangle_outline(center_x[iButton],center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT,arcade.color.BLACK,1)
      status_shape_list.append(shape)
      #shape = arcade.create_rectangle_outline(center_x[iButton],center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT,arcade.color.BLACK,1,180.0)
      #status_shape_list.append(shape)
  
    # Redraw outline around last box to make sure it is done
    shape = arcade.create_rectangle_outline(center_x[-1],center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT,arcade.color.BLACK,1)
    status_shape_list.append(shape)
    shape = arcade.create_rectangle_outline(center_x[-1],center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT,arcade.color.BLACK,1,180.0)
    status_shape_list.append(shape)
    
    # Save the centers of the buttons
    self.status_center_x = center_x
    self.status_center_y = center_y
    
    #------------------------------------------------
    
    # Save results of all of the above
    self.term_sprite_list = term_sprite_list
    self.hint_sprite_list = hint_sprite_list
    self.hint_shape_list = hint_shape_list
    self.status_sprite_list = status_sprite_list
    self.status_shape_list = status_shape_list
    
    #------------------------------------------------

    return
  
  #---------------------------------------------------------------
  
  def draw(self):
    
    # Draw bubble box
    self.bubble_shape_list.draw()
    
    # Draw term sprite
    self.term_sprite_list.draw()
    
    # Draw hints
    self.hint_shape_list.draw()
    self.hint_sprite_list.draw()
    
    # Draw status boxes
    self.status_shape_list.draw()
    self.status_sprite_list.draw()
    
    return
  
  #---------------------------------------------------------------
  
  def ClickInBox(self,x,y):
    
    """Takes x and y coordinates of click, returns if in box."""
    
    return inBox(x,y,self.xCenter,self.yCenter,self.width,self.height)
  
  #---------------------------------------------------------------
  
  def ClickInStatus(self,x,y):
    
    """Takes x and y coordinates, returns if in some type of box."""
    
    # Check if in one of the hint boxes
    for iHint in range(0,self.nHintsShow):
      
      # Get sprite for this hint
      hint_sprite = self.hint_sprite_list.sprite_list[iHint]
      
      # Check if in this hint
      if inBoxSprite(x,y,hint_sprite):
        return iHint
    
    # Check if in the known box
    status_sprite = self.status_sprite_list.sprite_list[1]
    if inBox(x,y,status_sprite.center_x,status_sprite.center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT):
      return 'K'
    
    # Check if in the ignore box
    status_sprite = self.status_sprite_list.sprite_list[0]
    if inBox(x,y,status_sprite.center_x,status_sprite.center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT):
      return 'X'
    
    return None
  
  #---------------------------------------------------------------
  
  def ClickInHint(self,x,y):
    
    
    return
  
  #---------------------------------------------------------------

#=====================================================================================

class LingQBubble:
  
  #---------------------------------------------------------------
  
  def __init__(self,word_sprite,lingq):
    
    # Save LingQ
    self.lingq = lingq
    
    # Get bubble center coordinates and dimensions
    self.width = BUBBLE_WIDTH
    self.height = BUBBLE_HEIGHT
    self.xCenter , self.yCenter = self.GetBubbleCenter(word_sprite)
    
    # Setup bubble box
    self.bubble_shape_list = self.GetBubbleBox()
     
    # Setup bubble contents
    self.bubble_sprite_list , self.term_shape_list = self.GetBubbleContents(word_sprite,lingq)
    
    return
  
  
  #---------------------------------------------------------------
  
  def GetBubbleCenter(self,word_sprite):
    
    # By default, put the bubble to the right of the word, but determine if should be to left
    if word_sprite.center_x+self.width > 0.95*SCREEN_WIDTH:
      xCenter = word_sprite.center_x - 0.5*self.width
    else:
      xCenter = word_sprite.center_x + 0.5*self.width
    
    # Move bubble right if off left side of screen
    if ( xCenter - 0.5*self.width ) < MARGIN_WIDTH:
      xCenter = MARGIN_WIDTH + 0.5*self.width
    
    # Move bubble left if off right side of screen
    if ( xCenter + 0.5*self.width ) > SCREEN_WIDTH-MARGIN_WIDTH:
      xCenter = SCREEN_WIDTH - MARGIN_WIDTH - 0.5*self.width
    
    # Be default put bubble below word, but determine if it should be above
    if word_sprite.center_y - self.height < 0.05*SCREEN_HEIGHT:
      # Above
      yCenter = word_sprite.center_y + 0.5*LINE_SPACE + 0.5*self.height
    else:
      # Below
      yCenter = word_sprite.center_y - 0.5*LINE_SPACE - 0.5*self.height
    
    return xCenter , yCenter
  
  #---------------------------------------------------------------
  
  def GetBubbleBox(self):
    
    # Make shape list for bubble
    bubble_shape_list = arcade.ShapeElementList()
    
    # Main box
    shape = arcade.create_rectangle_filled(self.xCenter,self.yCenter,self.width,self.height,LINGQ_BUBBLE_COLOR)
    bubble_shape_list.append(shape)
    
    # Outline of box
    shape = arcade.create_rectangle_outline(self.xCenter,self.yCenter,self.width,self.height,arcade.color.BLACK,1)
    bubble_shape_list.append(shape)
    shape = arcade.create_rectangle_outline(self.xCenter,self.yCenter,self.width,self.height,arcade.color.BLACK,1,180.0)
    bubble_shape_list.append(shape)
    
    return bubble_shape_list
  
  #---------------------------------------------------------------
  
  def GetBubbleContents(self,word_sprite,lingq):
    
    # Make a sprite list for contents of bubble
    bubble_sprite_list = arcade.SpriteList()
    
    # Make shape list for boxes
    term_shape_list = arcade.ShapeElementList()
    
    #------------------------------------------------
    # TERM
    
    # Made image out of word
    image = get_text_image(text=lingq['term'],font_size=FONT_SIZE_BUBBLE_TERM)
    
    # Make sprite from image
    term_sprite = WordSprite()
    term_sprite.SetWord(lingq['term'])
    term_sprite._texture = arcade.Texture(lingq['term']+"bubble")
    term_sprite.texture.image = image
    term_sprite.width = image.width
    term_sprite.height = image.height
    
    # Set position of word
    term_sprite.center_x = self.xCenter - 0.5*self.width + BUBBLE_MARGIN + 0.5*term_sprite.width
    term_sprite.center_y = self.yCenter + 0.5*self.height - BUBBLE_MARGIN - 0.5*term_sprite.height
    
    # Add word to word list
    bubble_sprite_list.append(term_sprite)
    
    #------------------------------------------------
    # HINTS
    
    # Number of hints
    nHints = len( lingq['hints'] )
    
    # Number of hints to show
    nHintsShow = min( nHints , BUBBLE_MAX_HINTS )
    
    # Save nHintsShow
    self.nHintsShow = nHintsShow
    
    # Center y position of first hin
    center_y = self.yCenter + 0.2*self.height
    
    # Loop over hints and add each one
    for iHint in range(0,nHintsShow):
      
      # Start hint text
      text = ''
      
      # Start hint with number of multiple hints
      if nHints > 1:
        text += str(iHint+1)+". "
      
      # Add text of hint
      text += lingq['hints'][iHint]['text'].replace('\n','')
      
      # Made image out of word
      image = get_text_image(text=text,font_size=FONT_SIZE_BUBBLE_HINT,width=self.width-4*BUBBLE_MARGIN)
      
      # Make sprite from image
      text_sprite = WordSprite()
      text_sprite.SetWord(text)
      text_sprite._texture = arcade.Texture(text)
      text_sprite.texture.image = image
      text_sprite.width = image.width
      text_sprite.height = image.height
      
      # Set position of word
      text_sprite.center_x = self.xCenter - 0.5*self.width + 2*BUBBLE_MARGIN + 0.5*text_sprite.width
      text_sprite.center_y = center_y
      
      # Get center_y of next hint if there is one
      center_y += -BUBBLE_HINT_SPACING
      
      # Add word to word list
      bubble_sprite_list.append(text_sprite)
    
    # If fewer hints shown than max, show some not-saved hints
    if nHintsShow < BUBBLE_MAX_HINTS:
      
      # Get hints from LingQ
      hints = lingqapi.GetLingQHints(lingq['term'])
      
      # Get number to show
      nHintsShow = BUBBLE_MAX_HINTS - nHintsShow
      
      for iHint in range(0,nHintsShow):
        
        # Start hint text
        text = ''
        
        # Start hint with number of multiple hints
        if nHints > 1:
          text += str(iHint+1)+". "
        
        # Add popularity if it is there
        if 'popularity' in hints[iHint]:
          text += "(" + str( hints[iHint]['popularity'] ) + ") "
        
        # Add google if from google
        if 'from_google' in hints[iHint]:
          if hints[iHint]['from_google']:
            text += "(google) "
        
        # Add text of hint
        text += hints[iHint]['text'].replace('\n','')
        
        # Made image out of word
        image = get_text_image(text=text,font_size=FONT_SIZE_BUBBLE_HINT,width=self.width-4*BUBBLE_MARGIN)
        
        # Make sprite from image
        text_sprite = WordSprite()
        text_sprite.SetWord(text)
        text_sprite._texture = arcade.Texture(text)
        text_sprite.texture.image = image
        text_sprite.width = image.width
        text_sprite.height = image.height
        
        # Set position of word
        text_sprite.center_x = self.xCenter - 0.5*self.width + 2*BUBBLE_MARGIN + 0.5*text_sprite.width
        text_sprite.center_y = center_y
        
        # Get center_y of next hint if there is one
        center_y += -BUBBLE_HINT_SPACING-0.5*text_sprite.height
      
        # Add word to list
        bubble_sprite_list.append(text_sprite)
        
        # NOW DO THE BOX
        
        # Main box
        shape = arcade.create_rectangle_filled(text_sprite.center_x,text_sprite.center_y,text_sprite.width,text_sprite.height,UNKNOWN_HINT_BOX_COLOR)
        term_shape_list.append(shape)
        
        # Outline of box
        shape = arcade.create_rectangle_outline(text_sprite.center_x,text_sprite.center_y,text_sprite.width,text_sprite.height,arcade.color.BLACK,1)
        term_shape_list.append(shape)
        shape = arcade.create_rectangle_outline(text_sprite.center_x,text_sprite.center_y,text_sprite.width,text_sprite.height,arcade.color.BLACK,1,180.0)
        term_shape_list.append(shape)
    
    #------------------------------------------------
    # STATUS
    
    # Get central y positions of buttons 
    center_y = self.yCenter - 0.5*self.height + BUBBLE_MARGIN + 0.5*BUBBLE_STATUS_HEIGHT
    
    # Get centers of all six buttons in x coordinates
    center_x = []
    center_x.append( self.xCenter - 0.5*self.width + BUBBLE_MARGIN + 0.5*BUBBLE_STATUS_WIDTH )
    center_x.append( center_x[-1] + BUBBLE_STATUS_WIDTH )
    center_x.append( center_x[-1] + BUBBLE_STATUS_WIDTH )
    center_x.append( center_x[-1] + BUBBLE_STATUS_WIDTH )
    center_x.append( center_x[-1] + BUBBLE_STATUS_WIDTH )
    center_x.append( center_x[-1] + BUBBLE_STATUS_WIDTH )
    
    # Get text for all six buttons
    button_text = [ '1' , '2' , '3' , '4' , 'K' , 'X' ]
    
    # Make letters for each
    for iButton in range(0,len(button_text)):
      
      # Make image out of word
      image = get_text_image(text=button_text[iButton],font_size=FONT_SIZE_BUBBLE_HINT)
      
      # Make sprite from image
      text_sprite = WordSprite()
      text_sprite.SetWord(button_text[iButton])
      text_sprite._texture = arcade.Texture(button_text[iButton])
      text_sprite.texture.image = image
      text_sprite.width = image.width
      text_sprite.height = image.height
      
      # Set position of word
      text_sprite.center_x = center_x[iButton]
      text_sprite.center_y = center_y
      
      # Add word to word list
      bubble_sprite_list.append(text_sprite)
    
    # Determine which box is the current status 
    if self.lingq['status'] == 0:
      iButtonCurrent = 0
    elif self.lingq['status'] == 1:
      iButtonCurrent = 1
    elif self.lingq['status'] == 2:
      iButtonCurrent = 2
    elif ( self.lingq['status'] == 3 ) and ( self.lingq['extended_status'] == 3 ):
      iButtonCurrent = 4
    elif self.lingq['status'] == 3:
      iButtonCurrent = 3
    else:
      iButtonCurrent = -1
    
    # Make boxes for each button
    for iButton in range(0,len(button_text)):
      
      # Get color for filled box
      color = LINGQ_BUBBLE_STATUS_COLOR
      if iButton == iButtonCurrent:
        color = LINGQ_BUBBLE_STATUS_CURRENT_COLOR
      
      # Make filled box
      shape = arcade.create_rectangle_filled(center_x[iButton],center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT,color)
      term_shape_list.append(shape)
      
      # Outline of box
      shape = arcade.create_rectangle_outline(center_x[iButton],center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT,arcade.color.BLACK,1)
      term_shape_list.append(shape)
      #shape = arcade.create_rectangle_outline(center_x[iButton],center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT,arcade.color.BLACK,1,180.0)
      #term_shape_list.append(shape)
  
    # Redraw outline around last box to make sure it is done
    shape = arcade.create_rectangle_outline(center_x[-1],center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT,arcade.color.BLACK,1)
    term_shape_list.append(shape)
    shape = arcade.create_rectangle_outline(center_x[-1],center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT,arcade.color.BLACK,1,180.0)
    term_shape_list.append(shape)
    
    # Save the centers of the buttons
    self.status_center_x = center_x
    self.status_center_y = center_y
    
    #------------------------------------------------
    
    return bubble_sprite_list , term_shape_list
  
  #---------------------------------------------------------------
  
  def draw(self):
    
    # Draw bubble box
    self.bubble_shape_list.draw()
    
    # Draw status boxes
    self.term_shape_list.draw()
    
    # Draw inside sprites
    self.bubble_sprite_list.draw()
    
    return
  
  #---------------------------------------------------------------
  
  def ClickInBox(self,x,y):
    
    """Takes x and y coordinates of click, returns if in box."""
    
    return inBox(x,y,self.xCenter,self.yCenter,self.width,self.height)
  
  #---------------------------------------------------------------
  
  def ClickInStatus(self,x,y):
    
    """Takes x and y coordinates of click, returns if in status box and which one."""
    
    # Initially assume not in any status box
    clickedStatus = None
    
    # Check each box individually
    for iButton in range(0,len(self.status_center_x)):
      if inBox(x,y,self.status_center_x[iButton],self.status_center_y,BUBBLE_STATUS_WIDTH,BUBBLE_STATUS_HEIGHT):
        clickedStatus = iButton
    
    return clickedStatus
  
  #---------------------------------------------------------------
  
  def idLingQ(self):
    """Returns LingQ ID."""
    return self.lingq['id']
  
  #---------------------------------------------------------------
  
  def termLingQ(self):
    """Returns LingQ term."""
    return self.lingq['term']
  
  #---------------------------------------------------------------

#=====================================================================================

def clickedOpenHud(x,y):
  
  """Takes coordinate of click, determines if open hud button."""
  
  if y > SCREEN_HEIGHT-MARGIN_HEIGHT:
    return True
  
  return False

#=====================================================================================

def clickedPreviousPage(x,y):
  
  """Takes coordinate of click, determines if next page was clicked."""
  
  if ( x < MARGIN_WIDTH ) and ( y < SCREEN_HEIGHT-MARGIN_HEIGHT ) and ( y > MARGIN_HEIGHT ):
    return True
  
  return False

#=====================================================================================

def clickedNextPage(x,y):
  
  """Takes coordinate of click, determines if next page was clicked."""
  
  if ( x > SCREEN_WIDTH-MARGIN_WIDTH ) and ( y < SCREEN_HEIGHT-MARGIN_HEIGHT ) and ( y > MARGIN_HEIGHT ):
    return True
  
  return False

#=====================================================================================

def dict_to_list(dictIn):
  
  """Takes dictionary, returns list of items in dictionary."""
  
  listOut = []
  for item in dictIn:
    listOut.append(item)
  
  return listOut

#=====================================================================================

if __name__ == "__main__":
  
  # Set the start method for multiprocessing to the default for Windows 
  # to avoid platform dependence
  mp.set_start_method('spawn')
  
  #lingqapi.MakeKnownWord(43338891)
  #lingqapi.MakeAllKnown()
  #sys.exit()
  
  # Create the Window
  window = LingQReader()
  
  # Setup the lesson
  window.setup_lesson()
  
  # Run the game
  arcade.run()
  
#=====================================================================================
