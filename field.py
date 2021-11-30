import random
import defaultAgent

class Cell:  #в зависимости от колва ресурса можно изменять цвет ячейки а от цены цвет границы ячейки
    def __init__(self,x,y, resource, mentalPrice) -> None:  
        self.x=x
        self.y=y
        self.res = resource
        self.price = mentalPrice

    def addRes(self,resource):
        self.res+=resource

    def removeRes(self, resource):
        if self.res>=resource :
            self.res-=resource
            return resource
        else:
            r=self.res
            self.res=0
            return r

class World:
    def __init__(self, size, agentsN) -> None:
        self.maxResource=2000
        self.maxPrice=25
        self.size=size
        self.ticks=0
        self.lifeCost = 1
        #self.cells = [[Cell(x,y,random.randint(1,self.maxResource), random.randint(1,self.maxPrice)) for y in range(self.size)] for x in range(self.size)]
        self.reset(agentsN)

    def reset(self, NAgents):
        self.cells = [[Cell(x,y,random.randint(1,self.maxResource), random.randint(1,self.maxPrice)) for y in range(self.size)] for x in range(self.size)]
        self.agents = []
        self.corps = []
        self.initAgents(NAgents)

    def initAgents(self, N):
        for i in range(N):
            self.addAgent()

    def addAgent(self):
        cell=self.cells[ random.randint(0,self.size-1)][ random.randint(0,self.size-1)]
        self.agents.append(defaultAgent.Agent(cell,self))

    def move_to(self, whoAsk, x, y):
        if x<0 or y<0 or x>=self.size or x>=self.size:
            return Exception('Cell out of range')
        cell=self.cells[x][y]
        whoAsk.mental-=cell.price
        whoAsk.prevCell=whoAsk.cell
        whoAsk.lastDrawCords=(-1,-1)
        whoAsk.cell=cell

    def scan(self, whoAsk, x, y):#запросить информацию о ячейки
        if x<0 or y<0 or x>=self.size or x>=self.size :
            raise Exception('Cell out of range')
        #whoAsk.mental-=self.lifeCost
        cell=self.cells[x][y]
        return (cell.res, cell.price)


    def lifeTick(self):
        self.ticks+=1
        for a in self.agents:
            if not a.isLive:
                continue
            a.life-=self.lifeCost
            if a.life>0 and a.mental>0:
                a.live()
            else:
                a.isLive=False
    



    