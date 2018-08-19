import pygame
import time
import threading
import random




class LiveVisual():
    
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.setDisplay()
        self.setsprites()
        self.setcolors()
        self.Skalierfaktor = 3
        self.eventHandler_Loop = 0
        self.run()
        

    def setDisplay(self):
        self.Display_HEIGHT = 1850
        self.Display_WIDTH = 1100
        self.Display = pygame.display.set_mode((self.Display_HEIGHT, self.Display_WIDTH), pygame.RESIZABLE)
        self.icon = pygame.image.load("lightbulb2.png")
        pygame.display.set_caption("Agentensystem")
        pygame.display.set_icon(self.icon)
              
    def setsprites(self):
        self.CozmoIMG = pygame.image.load("Cozmo.png")
        self.CubeIMG = pygame.image.load("Cube.png")

    def setcolors(self):
        self.black = (0,0,0)
        self.dark_gray = (50,50,50)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.dark_red = (139,0,0)
        self.green = (0,255,0)
        self.dark_green = (0,128,0)
        self.blue = (0,0,255)
        self.yellow = (255,255,0)
        self.dark_yellow = (139,139,0)
        self.aqua = (0,255,255)
        self.light_gray = (220,220,220)
        self.gray = (190,190,190)
        self.block_color = (53,115,255)

    def text_objects(self,text,font,color):
        textSurface = font.render(text,True,color)
        return textSurface, textSurface.get_rect()    
    
    def Maschine(self,x_Koordinate,y_Koordinate,Zeile_1=None,Zeile_2 =None,Status=0):
        # Maschinenbody
        Maschinenbreite = 84* self.Skalierfaktor
        Maschinenhoehe = 55* self.Skalierfaktor
        StartpunktX = x_Koordinate
        StartpunktY = y_Koordinate

        #Displayrahmen
        DisplayRahmenBreite = 70*self.Skalierfaktor
        DisplayRahmenHoehe = 23*self.Skalierfaktor
        DisplayRahmenStartpunktX = x_Koordinate+(7*self.Skalierfaktor)
        DisplayRahmenStartpunktY = y_Koordinate+(13*self.Skalierfaktor)

        # Display
        DisplayBreite = 65*self.Skalierfaktor
        DisplayHoehe = 15*self.Skalierfaktor
        DisplayStartpunktX = x_Koordinate+(9*self.Skalierfaktor)
        DisplayStartpunktY = y_Koordinate+(17*self.Skalierfaktor)
    
        # Form Zeichnen
        pygame.draw.rect(self.Display,self.black,(StartpunktX,StartpunktY,Maschinenbreite,Maschinenhoehe))
        pygame.draw.rect(self.Display,self.dark_gray,(DisplayRahmenStartpunktX,DisplayRahmenStartpunktY,DisplayRahmenBreite,DisplayRahmenHoehe))
        pygame.draw.rect(self.Display,self.blue,(DisplayStartpunktX,DisplayStartpunktY,DisplayBreite,DisplayHoehe))
    
        # Lampen Zeichnen
        Lampenradius = 3 * self.Skalierfaktor
        grueneLampeX = StartpunktX + 60 * self.Skalierfaktor
        gelbeLampeX = StartpunktX + 67 * self.Skalierfaktor
        roteLampeX = StartpunktX + 74 * self.Skalierfaktor
        lampenY = StartpunktY + 5*self.Skalierfaktor

        if Status == 0:
            pygame.draw.circle(self.Display,self.dark_green,(grueneLampeX,lampenY),Lampenradius)
            pygame.draw.circle(self.Display,self.dark_yellow,(gelbeLampeX,lampenY),Lampenradius)
            pygame.draw.circle(self.Display,self.red,(roteLampeX,lampenY),Lampenradius)
        if Status == 1:
            pygame.draw.circle(self.Display,self.dark_green,(grueneLampeX,lampenY),Lampenradius)
            pygame.draw.circle(self.Display,self.yellow,(gelbeLampeX,lampenY),Lampenradius)
            pygame.draw.circle(self.Display,self.dark_red,(roteLampeX,lampenY),Lampenradius)
        if Status == 2:
            pygame.draw.circle(self.Display,self.green,(grueneLampeX,lampenY),Lampenradius)
            pygame.draw.circle(self.Display,self.dark_yellow,(gelbeLampeX,lampenY),Lampenradius)
            pygame.draw.circle(self.Display,self.dark_red,(roteLampeX,lampenY),Lampenradius)
    

        # Display Text
        # Zeile 1
        smallText1 = pygame.font.Font("C:\Windows\Fonts\erbos_draco_1st_open_nbp.ttf",4*self.Skalierfaktor,bold=True)
        textSurf, textRect = self.text_objects(Zeile_1,smallText1,self.aqua)
        textRect.center = ( (DisplayStartpunktX + (DisplayBreite/2)), (DisplayStartpunktY + (4*self.Skalierfaktor)))
        self.Display.blit(textSurf,textRect)

        # Zeile 2
        smallText2 = pygame.font.Font("C:\Windows\Fonts\erbos_draco_1st_open_nbp.ttf",4*self.Skalierfaktor,bold=True)
        textSurf, textRect = self.text_objects(Zeile_2,smallText2,self.aqua)
        textRect.center = ( (DisplayStartpunktX + (DisplayBreite/2)), (DisplayStartpunktY + (12*self.Skalierfaktor)))
        self.Display.blit(textSurf,textRect)
        textRect

    def Cube(self,x_Koordinate,y_Koordinate,Status=0):
        self.Display.blit(self.CubeIMG,(x_Koordinate,y_Koordinate))

    def Cozmo(self,x_Koordinate,y_Koordinate,Status=0):
        self.Display.blit(self.CozmoIMG,(x_Koordinate,y_Koordinate))
 
    def eventHandler(self,):
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
                
    def Systemsensor(self):
        eins = random.randrange(0,3,1)
        zwei = random.randrange(0,3,1)
        drei = random.randrange(0,3,1)
        vier = random.randrange(0,3,1)
        fuenf = random.randrange(0,3,1)
        self.Zeichner(eins,zwei,drei,vier,fuenf)

    def Zeichner(self,StatusMA1,StatusMA2,StatusMA3,StatusMA4,StatusMA5):
        self.Maschine(50,50,"Maschine 1","Sleep",StatusMA1)
        self.Maschine(400,50, "Maschine 2", "Sleep",StatusMA2)
        self.Maschine(750,50, "Maschine 3", "Sleep",StatusMA3)
        self.Maschine(1100,50, "Maschine 4", "Sleep",StatusMA4)
        self.Maschine(1450,50, "Maschine 5", "Sleep",StatusMA5)

        self.Cube(50,400)
        self.Cozmo(600,600)

    def run(self):
        x = 0

        while True:
            self.eventHandler()
            self.Display.fill(self.white)

            self.Systemsensor()  
            pygame.display.update()
            self.clock.tick(10)
            x+=1


Fenster = LiveVisual()

