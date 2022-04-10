import pygame, sys, copy
from pygame.locals import *

try:
    import pyperclip
    importclip = True
except ImportError:
    print("ERROR: module pyperclip not found! pyperclip is needed for copy and paste features.")
    importclip = False


class TextEdit:
    def __init__(self, x=0, y=0, width=600, height=600, color=(255, 255, 255), show=True, focus=True, text=None, font="", size=13, spacing=3, fontcolor=(0, 0, 0), blink=20, syntaxhighlight=True):
        if text is None:
            text = [""]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.show = show
        self.focus = focus
        self.text = text
        self.size = size
        try:
            self.font = pygame.font.Font(font, size)
        except:
            self.font = pygame.font.SysFont("Courier New", size)
        char = self.font.render(" ", False, (0, 0, 0))
        self.fontwidth = char.get_width()
        self.spacing = spacing
        self.backspace = False
        self.backspacec = 20
        self.keypress = None
        self.mousedown = False
        self.keypressc = 20
        self.fontcolor = fontcolor
        self.cursorPos = [0, 0]
        self.selectPos = copy.deepcopy(self.cursorPos)
        self.cursorBlink = blink
        self.blink = blink
        self.syntaxhighlight = syntaxhighlight
        self.keywords = {"def":(255, 127, 0), "while":(255, 127, 0), "if":(255, 127, 0), "elif":(255, 127, 0), "else":(255, 127, 0),
                         "return":(255, 127, 0), "for":(255, 127, 0), "in":(255, 127, 0), "or":(255, 127, 0), "and":(255, 127, 0),
                         "import":(255, 127, 0), "from":(255, 127, 0), "class":(255, 127, 0), "True":(255, 127, 0), "False":(255, 127, 0),
                         "not":(255, 127, 0), "lambda":(255, 127, 0), "pass":(255, 127, 0), "print":(186,85,211), "int":(186,85,211),
                         "float":(186,85,211), "str":(186,85,211), "input":(186,85,211), "self":(138,43,26), "break":(255, 127, 0),
                         "continue":(255, 127, 0), "list":(186,85,211)}
        self.breaks = ["[", "]", "(", ")", "{", "}", "<", ">", ':', ";", ",", ".", "/", "\\", " ", "'", '"', "-", "=", '+', '*', "|", '`']
        self.comment = ['#']

    def resizeToDisplay(self):
        self.width = pygame.display.get_surface().get_width()-self.x
        self.height = pygame.display.get_surface().get_height()-self.y

    def colorSyntax(self, text):
        if self.syntaxhighlight:
            final = []
            currentToken = ""
            inString = False
            startString = None
            inInteger = False
            for i in text:
                if not inString and i in self.comment:
                    final.append([text[text.index(i):], (125, 125, 125)])
                    break
                if not inString and not inInteger and i in self.breaks:
                    if currentToken in self.keywords:
                        final.append([currentToken, self.keywords[currentToken]])
                    else:
                        final.append([currentToken, self.fontcolor])
                    currentToken = ""
                    if i != '"' and i != "'":
                        final.append([i, self.fontcolor])
                        continue
                if i == "'" or i == '"':
                    if not inString:
                        inString = True
                        startString = i
                    else:
                        if i == startString:
                            inString = False
                            final.append([currentToken+i, (0, 200, 0)])
                            currentToken = ""
                            continue
                if not inString:
                    try:
                        num = int(i)
                        if not inInteger:
                            inInteger = True
                    except:
                        if inInteger:
                            final.append([currentToken, (150, 200, 200)])
                            currentToken = ""
                            final.append([i, self.fontcolor])
                            inInteger = False
                            continue
                currentToken += i
            if currentToken in self.keywords:
                final.append([currentToken, self.keywords[currentToken]])
            else:
                final.append([currentToken, self.fontcolor])
            if len(final) == 0:
                if currentToken in self.keywords:
                    final.append([currentToken, self.keywords[currentToken]])
                else:
                    final.append([currentToken, self.fontcolor])
            return final
        else:
            return [[text, self.fontcolor]]

    def render(self):
        if self.show:
            pygame.draw.rect(pygame.display.get_surface(), self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), (self.x, self.y, self.width, self.height), 2)

            x, y = self.x+self.spacing, self.y+self.spacing

            if self.cursorBlink <= 0:
                self.cursorBlink -= 1
                if self.cursorBlink == -self.blink:
                    self.cursorBlink = self.blink
            else:
                self.cursorBlink -= 1
            if not self.focus:
                self.cursorBlink = self.blink

            for i in range(0, len(self.text)):
                if self.cursorPos != self.selectPos:
                    if min(self.cursorPos[0], self.selectPos[0]) <= i <= max(self.cursorPos[0], self.selectPos[0]):
                        if i == self.selectPos[0] or i == self.cursorPos[0]:
                            if self.selectPos[0] == self.cursorPos[0]:
                                surf2 = self.font.render(" " * min(self.selectPos[1], self.cursorPos[1]), False, (0, 0, 0))
                                surf = self.font.render(' ' * (max(self.selectPos[1], self.cursorPos[1])-min(self.selectPos[1], self.cursorPos[1])), False,
                                                        (255, 255, 255),
                                                        (50, 100, 150))
                                pygame.display.get_surface().blit(surf, (self.x + self.spacing + surf2.get_width(), y))
                            else:
                                if self.selectPos[0] < self.cursorPos[0]:
                                    if i == self.cursorPos[0]:
                                        surf = self.font.render(' ' * self.cursorPos[1], False, (255, 255, 255),
                                                                (50, 100, 150))
                                        pygame.display.get_surface().blit(surf, (self.x + self.spacing, y))
                                    else:
                                        surf2 = self.font.render(" "*self.selectPos[1], False, (0, 0, 0))
                                        surf = self.font.render(' ' * (len(self.text[i])-self.selectPos[1]), False, (255, 255, 255),
                                                                (50, 100, 150))
                                        pygame.display.get_surface().blit(surf, (self.x + self.spacing+surf2.get_width(), y))

                                else:
                                    if i == self.selectPos[0]:
                                        surf = self.font.render(' ' * self.selectPos[1], False, (255, 255, 255),
                                                                (50, 100, 150))
                                        pygame.display.get_surface().blit(surf, (self.x + self.spacing, y))
                                    else:
                                        surf2 = self.font.render(" " * self.cursorPos[1], False, (0, 0, 0))
                                        surf = self.font.render(' ' * (len(self.text[i]) - self.cursorPos[1]), False,
                                                                (255, 255, 255),
                                                                (50, 100, 150))
                                        pygame.display.get_surface().blit(surf,(self.x + self.spacing + surf2.get_width(), y))
                        else:
                            surf = self.font.render(' ' * len(self.text[i]), False, (255, 255, 255), (50, 100, 150))
                            pygame.display.get_surface().blit(surf, (self.x+self.spacing, y))
                elif i == self.cursorPos[0]:
                    surf = self.font.render(" "*self.width, False, (0, 0, 0), (self.color[0]+10, self.color[1]+10, self.color[2]+10))
                    pygame.display.get_surface().blit(surf, (self.x, y))
                if i == self.cursorPos[0]:
                    if self.cursorBlink <= 0:
                        surf = self.font.render(' '*self.cursorPos[1], False, (255, 255, 255))
                        pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), (self.x+self.spacing+surf.get_width(), y, 2, surf.get_height()))
                y += self.size + self.spacing

            y = self.y + self.spacing

            for i in self.text:
                for j in self.colorSyntax(i):
                    surf = self.font.render(j[0], True, j[1])
                    pygame.display.get_surface().blit(surf, (x, y))
                    x += surf.get_width()
                x = self.x+self.spacing
                y += self.size+self.spacing

    def update(self):
        if self.show:
            for i in pygame.event.get():
                if i.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if i.type == KEYDOWN and self.focus:
                    if i.key == K_BACKSPACE:
                        self.backspace = True
                        if self.selectPos == self.cursorPos:
                            if self.cursorPos[1] == 0:
                                if self.cursorPos[0] != 0:
                                    self.cursorPos[1] = len(self.text[self.cursorPos[0]-1])
                                    self.text[self.cursorPos[0]-1] += self.text[self.cursorPos[0]]
                                    del self.text[self.cursorPos[0]]
                                    self.cursorPos[0] -= 1
                            else:
                                self.text[self.cursorPos[0]] = self.text[self.cursorPos[0]][:self.cursorPos[1]-1] + self.text[self.cursorPos[0]][self.cursorPos[1]:]
                                self.cursorPos[1] -= 1
                            self.selectPos = copy.deepcopy(self.cursorPos)
                        else:
                            if self.selectPos[0] == self.cursorPos[0]:
                                self.text[self.selectPos[0]] = self.text[self.selectPos[0]][:min(self.selectPos[1], self.cursorPos[1])]+self.text[self.selectPos[0]][max(self.selectPos[1], self.cursorPos[1]):]
                            else:
                                delete = []
                                for j in range(max(self.selectPos[0], self.cursorPos[0])-1, min(self.selectPos[0], self.cursorPos[0]), -1):
                                    delete.append(j)
                                if self.selectPos[0] < self.cursorPos[0]:
                                    self.text[self.selectPos[0]] = self.text[self.selectPos[0]][:self.selectPos[1]] + self.text[self.cursorPos[0]][self.cursorPos[1]:]
                                    delete.append(self.cursorPos[0])
                                else:
                                    self.text[self.cursorPos[0]] = self.text[self.cursorPos[0]][:self.cursorPos[1]] + self.text[self.selectPos[0]][self.selectPos[1]:]
                                    delete.append(self.selectPos[0])
                                delete.sort(reverse=True)
                                for i in delete:
                                    del self.text[i]
                                del delete
                            if self.selectPos[1] < self.cursorPos[1] or self.selectPos[0] < self.cursorPos[0]:
                                self.cursorPos = copy.deepcopy(self.selectPos)
                            else:
                                self.selectPos = copy.deepcopy(self.cursorPos)
                        self.cursorBlink = 0
                    elif i.key == K_RETURN:
                        self.text.insert(self.cursorPos[0]+1, "")
                        self.cursorPos[0] += 1
                        self.text[self.cursorPos[0]] += self.text[self.cursorPos[0]-1][self.cursorPos[1]:]
                        self.text[self.cursorPos[0]-1] = self.text[self.cursorPos[0]-1][:self.cursorPos[1]]
                        self.cursorPos[1] = 0
                        self.cursorBlink = 0
                        self.selectPos = copy.deepcopy(self.cursorPos)
                    elif i.key == K_TAB:
                        self.text[self.cursorPos[0]] = self.text[self.cursorPos[0]][:self.cursorPos[1]] + "    " + self.text[self.cursorPos[0]][self.cursorPos[1]:]
                        self.cursorPos[1] += 4
                        self.selectPos = copy.deepcopy(self.cursorPos)
                        self.cursorBlink = 0
                    elif i.key == K_LEFT:
                        self.keypress = K_LEFT
                        if self.cursorPos != self.selectPos and not (i.mod & KMOD_SHIFT):
                            if self.cursorPos[0] == self.selectPos[0]:
                                if self.cursorPos[1] < self.selectPos[1]:
                                    self.selectPos = copy.deepcopy(self.cursorPos)
                                else:
                                    self.cursorPos = copy.deepcopy(self.selectPos)
                            else:
                                if self.cursorPos[0] < self.selectPos[0]:
                                    self.selectPos = copy.deepcopy(self.cursorPos)
                                else:
                                    self.cursorPos = copy.deepcopy(self.selectPos)
                            continue
                        if self.cursorPos[1] == 0:
                            if self.cursorPos[0] != 0:
                                self.cursorPos[0] -= 1
                                self.cursorPos[1] = len(self.text[self.cursorPos[0]])
                        else:
                            self.cursorPos[1] -= 1
                        if not (i.mod & KMOD_SHIFT):
                            self.selectPos = copy.deepcopy(self.cursorPos)
                        self.cursorBlink = 0
                    elif i.key == K_RIGHT:
                        self.keypress = K_RIGHT
                        if self.cursorPos != self.selectPos and not (i.mod & KMOD_SHIFT):
                            if self.cursorPos[0] == self.selectPos[0]:
                                if self.cursorPos[1] < self.selectPos[1]:
                                    self.cursorPos = copy.deepcopy(self.selectPos)
                                else:
                                    self.selectPos = copy.deepcopy(self.cursorPos)
                            else:
                                if self.cursorPos[0] < self.selectPos[0]:
                                    self.cursorPos = copy.deepcopy(self.selectPos)
                                else:
                                    self.selectPos = copy.deepcopy(self.cursorPos)
                            continue
                        if self.cursorPos[1] == len(self.text[self.cursorPos[0]]):
                            if self.cursorPos[0] != len(self.text)-1:
                                self.cursorPos[0] += 1
                                self.cursorPos[1] = 0
                        else:
                            self.cursorPos[1] += 1
                        if not (i.mod & KMOD_SHIFT):
                            self.selectPos = copy.deepcopy(self.cursorPos)
                        self.cursorBlink = 0
                    elif i.key == K_UP:
                        self.keypress = K_UP
                        if self.cursorPos[0] != 0:
                            self.cursorPos[0] -= 1
                            if self.cursorPos[1] > len(self.text[self.cursorPos[0]]):
                                self.cursorPos[1] = len(self.text[self.cursorPos[0]])
                            if not (i.mod & KMOD_SHIFT):
                                self.selectPos = copy.deepcopy(self.cursorPos)
                            self.cursorBlink = 0
                    elif i.key == K_DOWN:
                        self.keypress = K_DOWN
                        if self.cursorPos[0] != len(self.text)-1:
                            self.cursorPos[0] += 1
                            if self.cursorPos[1] > len(self.text[self.cursorPos[0]]):
                                self.cursorPos[1] = len(self.text[self.cursorPos[0]])
                            if not (i.mod & KMOD_SHIFT):
                                self.selectPos = copy.deepcopy(self.cursorPos)
                            self.cursorBlink = 0
                    elif i.key == K_LSHIFT or i.key == K_RSHIFT:
                        pass
                    elif importclip and i.key == K_c and i.mod & KMOD_LMETA:
                        copytext = ""
                        if self.selectPos[0] == self.cursorPos[0]:
                            if self.selectPos[1] < self.cursorPos[1]:
                                copytext = self.text[self.cursorPos[0]][self.selectPos[1]:self.cursorPos[1]]
                            else:
                                copytext = self.text[self.cursorPos[0]][self.cursorPos[1]:self.selectPos[1]]
                        else:
                            for line in range(min(self.cursorPos[0], self.selectPos[0])+1, max(self.cursorPos[0], self.selectPos[0])):
                                copytext += self.text[line]+'\n'
                            if self.selectPos[0] < self.cursorPos[0]:
                                copytext = self.text[self.selectPos[0]][self.selectPos[1]:]+'\n'+copytext
                                copytext += self.text[self.cursorPos[0]][:self.cursorPos[1]]
                            else:
                                copytext = self.text[self.cursorPos[0]][self.cursorPos[1]:]+'\n'+copytext
                                copytext += self.text[self.selectPos[0]][:self.selectPos[1]]
                        pyperclip.copy(copytext)
                    elif importclip and i.key == K_v and i.mod & KMOD_LMETA:
                        pastetext = pyperclip.paste()
                        for i in pastetext:
                            if i == '\n':
                                self.cursorPos[0] += 1
                                self.text.insert(self.cursorPos[0], "")
                            else:
                                self.text[self.cursorPos[0]] += i
                        self.cursorPos[1] = len(self.text[self.cursorPos[0]])
                    elif i.key == K_LSUPER or i.key == K_RSUPER:
                        pass
                    else:
                        self.text[self.cursorPos[0]] = self.text[self.cursorPos[0]][:self.cursorPos[1]] + i.unicode + self.text[self.cursorPos[0]][self.cursorPos[1]:]
                        self.cursorPos[1] += 1
                        self.cursorBlink = 0
                        self.selectPos = copy.deepcopy(self.cursorPos)
                elif i.type == KEYUP and self.focus:
                    if i.key == K_BACKSPACE:
                        self.backspace = False
                        self.backspacec = 20
                    if i.key == self.keypress:
                        self.keypress = None
                        self.keypressc = 20
                elif i.type == MOUSEBUTTONDOWN:
                    if pygame.Rect((self.x, self.y, self.width, self.height)).collidepoint(pygame.mouse.get_pos()):
                        self.mousedown = True
                        self.focus = True
                        x, y = pygame.mouse.get_pos()
                        y -= (self.y+self.spacing)
                        x -= (self.x+self.spacing)
                        self.selectPos[0] = min(int(y/(self.size+self.spacing)), len(self.text)-1)
                        self.selectPos[1] = min(len(self.text[self.selectPos[0]]), int(x/self.fontwidth))
                        self.cursorBlink = 0
                elif i.type == MOUSEBUTTONUP and self.focus:
                    if self.mousedown:
                        if pygame.Rect((self.x, self.y, self.width, self.height)).collidepoint(pygame.mouse.get_pos()):
                            self.mousedown = False
                            x, y = pygame.mouse.get_pos()
                            y -= (self.y + self.spacing)
                            x -= (self.x + self.spacing)
                            self.cursorPos[0] = min(int(y / (self.size + self.spacing)), len(self.text) - 1)
                            self.cursorPos[1] = min(len(self.text[self.cursorPos[0]]), int(x / self.fontwidth))
                        elif self.mousedown:
                            self.cursorPos = copy.deepcopy(self.selectPos)
                            self.mousedown = False
            if self.mousedown:
                if pygame.Rect((self.x, self.y, self.width, self.height)).collidepoint(pygame.mouse.get_pos()):
                    x, y = pygame.mouse.get_pos()
                    y -= (self.y + self.spacing)
                    x -= (self.x + self.spacing)
                    self.cursorPos[0] = min(int(y / (self.size + self.spacing)), len(self.text) - 1)
                    self.cursorPos[1] = min(len(self.text[self.cursorPos[0]]), int(x / self.fontwidth))
                    self.cursorBlink = 0
            if self.backspacec > 0 and self.backspace:
                self.backspacec -= 1
            if self.keypress is not None and self.keypressc > 0:
                self.keypressc -= 1
            if self.keypress is not None and self.keypressc == 0:
                self.keypressc = 3
                event = pygame.event.Event(pygame.KEYDOWN)
                event.key = self.keypress
                event.mod = KMOD_NONE
                pygame.event.post(event)
            if self.backspace and self.backspacec == 0:
                self.backspacec = 3
                if self.selectPos == self.cursorPos:
                    if self.cursorPos[1] == 0:
                        if self.cursorPos[0] != 0:
                            self.cursorPos[1] = len(self.text[self.cursorPos[0] - 1])
                            self.text[self.cursorPos[0] - 1] += self.text[self.cursorPos[0]]
                            del self.text[self.cursorPos[0]]
                            self.cursorPos[0] -= 1
                    else:
                        self.text[self.cursorPos[0]] = self.text[self.cursorPos[0]][:self.cursorPos[1] - 1] + self.text[
                                                                                                                  self.cursorPos[
                                                                                                                      0]][
                                                                                                              self.cursorPos[
                                                                                                                  1]:]
                        self.cursorPos[1] -= 1
                    self.selectPos = copy.deepcopy(self.cursorPos)
                else:
                    if self.selectPos[0] == self.cursorPos[0]:
                        self.text[self.selectPos[0]] = self.text[self.selectPos[0]][
                                                       :min(self.selectPos[1], self.cursorPos[1])] + self.text[
                                                                                                         self.selectPos[
                                                                                                             0]][max(
                            self.selectPos[1], self.cursorPos[1]):]
                    else:
                        delete = []
                        for j in range(max(self.selectPos[0], self.cursorPos[0]) - 1,
                                       min(self.selectPos[0], self.cursorPos[0]), -1):
                            delete.append(j)
                        if self.selectPos[0] < self.cursorPos[0]:
                            self.text[self.selectPos[0]] = self.text[self.selectPos[0]][:self.selectPos[1]] + self.text[
                                                                                                                  self.cursorPos[
                                                                                                                      0]][
                                                                                                              self.cursorPos[
                                                                                                                  1]:]
                            delete.append(self.cursorPos[0])
                        else:
                            self.text[self.cursorPos[0]] = self.text[self.cursorPos[0]][:self.cursorPos[1]] + self.text[
                                                                                                                  self.selectPos[
                                                                                                                      0]][
                                                                                                              self.selectPos[
                                                                                                                  1]:]
                            delete.append(self.selectPos[0])
                        delete.sort(reverse=True)
                        for i in delete:
                            del self.text[i]
                        del delete
                    if self.selectPos[1] < self.cursorPos[1] or self.selectPos[0] < self.cursorPos[0]:
                        self.cursorPos = copy.deepcopy(self.selectPos)
                    else:
                        self.selectPos = copy.deepcopy(self.cursorPos)
                self.cursorBlink = 0
