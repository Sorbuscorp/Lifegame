import pygame
import random
from field import World
import defaultAgent

AGENTS_COUNT=200

class PyGameGUI():

    def __init__(self, resolution, world):
        self.resolution = resolution # (WIDTH, HEIGHT)
        self.world = world
        self.tileXSize=resolution[0]/world.size
        self.tileYSize=resolution[1]/world.size
        self.isPaused=False
        try:
            self.agentRadius=(self.tileXSize/len(world.agents))/2
            if self.agentRadius<=5:
                self.agentRadius=5
        except:
            pass
        pygame.init()
        self.Surface = pygame.display.set_mode(self.resolution)
        self.Clock = pygame.time.Clock()
       
    def Tune(self, settings: dict):
        self.FPS = settings['FPS']
    
    def DrawWorld(self):
        for row in self.world.cells:
            for cell in row:
                l=cell.x*self.tileXSize
                t=cell.y*self.tileYSize
                
                resourceCoef=(1-(self.world.maxResource-cell.res)/self.world.maxResource)
                priceCoef=(self.world.maxPrice-cell.price)/self.world.maxPrice
                
                color=pygame.Color(0,0,0)
                color.hsva=(120,50,100*resourceCoef,100)
                pygame.draw.rect(self.Surface, color, (l,t,self.tileXSize,self.tileYSize))

                color.hsva=(120,50*priceCoef,100,100)
                pygame.draw.rect(self.Surface, color, (l,t,self.tileXSize,self.tileYSize),2)


    def DrawAgents(self):
        for agent in self.world.agents:
            if agent.lastDrawCords[0]==-1 or agent.lastDrawCords[1]==-1:
                x_shift=random.uniform(0.1, 0.9)
                y_shift=random.uniform(0.1, 0.9)
                x=agent.cell.x*self.tileXSize + self.tileXSize*x_shift
                y=agent.cell.y*self.tileYSize + self.tileYSize*y_shift
                agent.lastDrawCords=(x,y)
            else:
                x,y=agent.lastDrawCords
            

            lifeCoef=1-(defaultAgent.MAX_LIFE-agent.life)/defaultAgent.MAX_LIFE
            mentalcoef=1-(defaultAgent.MAX_MENTAL-abs(agent.mental))/defaultAgent.MAX_MENTAL
            #color setting
            h = 0 # red
            if agent.isLive :
                s = 75
                v = 100*lifeCoef
            else:
                s=0
                v = 100
            
            a = 100 
            color=pygame.Color(0,0,0)
            color.hsva=(h,s,v,a)
            pygame.draw.circle(self.Surface, color, (x,y), self.agentRadius)
            color.hsva=(0,0,100*mentalcoef,0)
            pygame.draw.circle(self.Surface, color, (x,y), self.agentRadius,1)
  




    def Run(self):

        while True:
            self.Surface.fill(pygame.Color('White'))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.isPaused=not self.isPaused
                    if event.key == pygame.K_r:
                        world.reset(AGENTS_COUNT)

            if self.isPaused :
                continue

            self.DrawWorld()
            self.world.lifeTick()
            self.DrawAgents()
            # print(self.Clock.get_fps())
            pygame.display.flip()
            self.Clock.tick(self.FPS)

world=World(10,AGENTS_COUNT)
gui = PyGameGUI((1000, 1000), world)
gui.Tune({ 'FPS': 15 })
gui.Run()