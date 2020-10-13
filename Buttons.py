
"""
Module for the button class.
"""

import arcade

#=====================================================================================

# Dictionary for saving text images
text_images_save = {}

#=====================================================================================

class Button:
  
  """
  Generic class for a button.
  
  """
  
  #---------------------------------------------------------------
  
  def __init__(self,center_x,center_y,
               width=None,height=None,backgroundColor=None,outlineColor=None,outlineThick=1,
               imageFilename=None,imageScale=1,
               textString=None,fontSize=None,widthTextMax=None):
    
    """Sets up the button."""
    
    # Save parameters
    self.center_x = center_x
    self.center_y = center_y
    self.width = width
    self.height = height
    self.backgroundColor = backgroundColor
    self.outlineColor = outlineColor
    self.outlineThick = outlineThick
    self.imageFilename = imageFilename
    self.imageScale = imageScale
    self.textString = textString
    self.fontSize = fontSize
    self.widthTextMax = widthTextMax
    
    # Get image if specified
    self._SetupImage()
    
    # Setup background
    self._SetupBackground()
    
    # Setup outline
    self._SetupOutline()
    
    # Setup text if desired
    self._SetupText()
    
    # Get button dimensions
    self._SetupDimensions()
    
    return
    
  #---------------------------------------------------------------
  
  def _SetupImage(self):
    
    """Sets up the image."""
    
    # End here if no outline wanted
    if self.imageFilename is None:
      self.image = None
      return
    
    # Make sure width and imageScale not both specified 
    if ( not self.width == None ) and ( not self.imageScale == None ):
      print("Error: cannot specify width and imageScale in creation of Button")
      raise ValueError()
    
    # Load the image
    image = arcade.Sprite(self.imageFilename,self.imageScale)
    
    # If a width has been specified, get new image with scale to match width
    if not self.width is None: 
      
      # Get correct imageScale
      self.imageScale = self.width / image.width
      
      # Reload image if not close enough to correct
      if not abs(self.imageScale-1.0) < 1.0e-3:
        image = arcade.Sprite(self.imageFilename,self.imageScale)
      
    # Set center of image
    image.center_x = self.center_x
    image.center_y = self.center_y
    
    # Set the dimensions
    self.width = image.width
    self.height = image.height
    
    # Save the image
    self.image = image
    
    return
  
  #---------------------------------------------------------------
  
  def _SetupBackground(self):
    
    """Sets up sprite for background color."""
    
    # End here if no background color wanted
    if self.backgroundColor is None:
      self.background = None
      return
    
    # Get shape
    background = arcade.create_rectangle_filled(self.center_x,self.center_y,self.width,self.height,self.backgroundColor)
      
    # Save shale
    self.background = background
    
    return
  
  #---------------------------------------------------------------
  
  def _SetupOutline(self):
    
    """Sets up outline."""
    
    # End here if no outline wanted
    if self.outlineColor is None:
      self.outline = None
      return
    
    # Get shape as a list with two (so one side is not thiner)
    outline = arcade.ShapeElementList()
    shape = arcade.create_rectangle_outline(self.center_x,self.center_y,self.width,self.height,self.outlineColor,self.outlineThick)
    outline.append(shape)
    shape = arcade.create_rectangle_outline(self.center_x,self.center_y,self.width,self.height,self.outlineColor,self.outlineThick,180.0)
    outline.append(shape)
    
    # Save shape
    self.outline = outline
    
    return
  
  #---------------------------------------------------------------
  
  def _SetupText(self):
    """Sets up text sprite if specified."""
    
    # End here if no text wanted
    if self.textString is None:
      self.text = None
      return
    
    # Made image out of test string
    image = get_text_image(text=self.textString,font_size=self.fontSize,width=self.widthTextMax)
      
    # Make sprite from image
    text = arcade.Sprite()
    text._texture = arcade.Texture(self.textString)
    text.texture.image = image
    text.width = image.width
    text.height = image.height
    
    # Set position of word
    text.center_x = self.center_x
    text.center_y = self.center_y
    
    # Save text sprite
    self.text = text
    
    return
  
  #---------------------------------------------------------------
  
  def _SetupDimensions(self):
    """Determines basic dimensions of the box."""
    
    # Get min and max of x and y of box
    self.xMin = self.center_x - 0.5*self.width
    self.xMax = self.center_x + 0.5*self.width
    self.yMin = self.center_y - 0.5*self.height
    self.yMax = self.center_y + 0.5*self.height
    
    
    return
  
  #---------------------------------------------------------------
  
  def inButton(self,x,y):
    """Takes coorindates (usually of click), returns if this is in the button."""
    
    if ( x > self.xMin ) and ( x < self.xMax ) and ( y > self.yMin ) and ( y < self.yMax ):
      return True
      
    return False
  
  #---------------------------------------------------------------
  
  def draw(self):
    
    # Draw background
    if not self.background is None:
      self.background.draw()
    
    # Draw the image
    if not self.image is None:
      self.image.draw()
    
    # Draw the text
    if not self.text is None:
      self.text.draw()
    
    # Draw outline
    if not self.outline is None:
      self.outline.draw()
    
    return
  
  #---------------------------------------------------------------
  
#=====================================================================================

def get_text_image(text,text_color=arcade.color.BLACK,font_size=1,width=0,align="left",font_name=('calibri','arial')):
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

if __name__ == "__main__":
  None
  
