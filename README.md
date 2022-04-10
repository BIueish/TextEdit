# TextEdit
Pygame extension providing text input functionalities

Dependencies: pygame

Optional dependencies: pyperclip(Needed for Copy/Paste)

## Usage

To use just import text.py and create a TextEdit class.
Render and update this TextEdit class in your program loop.

Example:
```py
import pygame, sys
from pygame.locals import *
from text import TextEdit

display = pygame.display.set_mode((600, 600))
inputText = TextEdit()

while True:
  displaysurf.fill((255, 255, 255))
  inputText.update()
  inputText.render()
  for i in pygame.event.get():
    if i.type == QUIT:
      pygame.quit()
      sys.exit()
  pygame.display.update()

```

## Features

The TextEdit class has the following features:
  - Basic typing
  - Syntax highlighting
  - Selection
  - Copy and paste
  - etc.
  
Read the wiki for more information.
