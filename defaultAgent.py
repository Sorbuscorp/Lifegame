import names

#from field import World
MAX_LIFE=100
MAX_MENTAL=100
class Agent:
    def __init__(self, cell, world) -> None:
        self.lastDrawCords=(-1,-1)
        self.world=world
        self.name = names.get_full_name()
        self.life=MAX_LIFE
        self.mental = MAX_MENTAL
        self.prevCell=None
        self.cell = cell #надо поменять реализацию cells (сейчас агент может менять ячейку)
        self.isLive = True
        pass

    def live(self):
        hunger=MAX_LIFE-self.life
        if self.cell.res==0 : #если ресурс в клетке кончился
            self.move()
            return
        elif hunger>0 : #если ресурс есть и жизнь не на максимуме
            self.eat(hunger)
            return
        else: #если все хорошо то "свободное время"
            self.wait() 
            return
        
    def search(self):#простой поиск соседней клетки с едой (каждый запрос стоит сколько-то ментального ресурса)
        x=self.cell.x
        y=self.cell.y
        max_resource=(-1,-1,-1)
        max_res_to_mental=(-1.0,-1,-1)
        for i in range(4):
            sign=i % 2
            add=1
            new_x, new_y =x,y
            if sign!=0 :
                add=-add
            if i<2 :
                new_x=new_x+add
            else:
                new_y=new_y+add
            try:               
                resource=self.world.scan(self,new_x,new_y)
            except Exception as exc:
                print(exc)
                continue
            if resource[0]>max_resource[0] :
                max_resource=(resource[0],new_x,new_y)
            if (resource[0]/resource[1])>max_res_to_mental[0] :
                max_res_to_mental=(resource[0]/resource[1],new_x,new_y)
        
        return  (max_resource,max_res_to_mental)

    def move(self):
        max_resource, max_effective=self.search()
        if self.mental>MAX_MENTAL/2 :
            self.world.move_to(self,max_resource[1],max_resource[2])
        else:
            self.world.move_to(self,max_effective[1],max_effective[2])

    def eat(self, hunger):
        eated=self.cell.removeRes(hunger)
        self.life+=eated
        return

    def wait(self):
        pass
        return