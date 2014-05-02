from tkinter import *
import random

class Vue():
    def __init__(self,parent):
        self.parent=parent
        self.root=Tk()
        self.carrebouge=0
        self.canevas=Canvas(self.root,width=500,height=500,bg="white",highlightthickness=50,highlightbackground="black",highlightcolor="black")
        self.canevas.pack()
        self.canevas.bind("<Button-1>",self.gotclick)
        self.canevas.bind("<ButtonRelease>",self.forgotclick)
        self.canevas.bind("<Motion>",self.gotbouge)
        
    def gotbouge(self,evt):
        if self.carrebouge:
            self.parent.carrebouge(evt.x,evt.y)
        
    def gotclick(self,evt):
        lestags=self.canevas.gettags("current")
        if "carre" in lestags:
            self.carrebouge=1
            
    def forgotclick(self,evt):
        self.carrebouge=0
        
    def miseajour(self,modele):
        self.canevas.delete(ALL)
        for i in modele.pions:
            self.canevas.create_rectangle(i.x1,i.y1,i.x2,i.y2,fill="blue", tags=("pion"))
        j=modele.carre
        self.canevas.create_rectangle(j.x1,j.y1,j.x2,j.y2,fill="red", tags=("carre"))
 
class Pion():
    def __init__(self,parent,x,y):
        self.parent=parent 
        self.x1=x-10
        self.x2=x+10
        self.y1=y-10
        self.y2=y+10
    def bouge(self,x=10,y=10):
        xa=random.randrange(x)*(random.randrange(3)-1)
        ya=random.randrange(x)*(random.randrange(3)-1)
        self.x1=self.x1+xa
        self.x2=self.x2+xa
        self.y1=self.y1+xa
        self.y2=self.y2+xa
              
class Carre():
    def __init__(self,parent):
        self.parent=parent 
        self.x1=265
        self.x2=315
        self.y1=265
        self.y2=315
        
    def bouge(self,x,y):
        self.x1=x-20
        self.x2=x+20
        self.y1=y-20
        self.y2=y+20
        
class Modele():
    def __init__(self,parent):
        self.parent=parent
        self.pions=[]
        self.carre=Carre(self)
        self.creerPions()
    
    def creerPions(self,n=4):
        for i in range(n):
            x=random.randrange(500)+50
            y=random.randrange(500)+50
            self.pions.append(Pion(self,x,y))
    def miseajour(self):
        for i in self.pions:
            i.bouge()
    def carrebouge(self,x,y):
        self.carre.bouge(x,y)
            
class Controleur():
    def __init__(self):
        self.actif=1
        self.modele=Modele(self) 
        self.vue=Vue(self)
        self.vue.miseajour(self.modele)
        self.gameOn()
        self.vue.root.mainloop()
        
    def carrebouge(self,x,y):
        self.modele.carre.bouge(x,y)
        
    def gameOn(self):
        if self.actif:
            self.modele.miseajour()
            self.vue.miseajour(self.modele)
            self.vue.root.after(50,self.gameOn)
            
if __name__ == '__main__':
    c=Controleur()
        
        
        
        
        
        
        
        
        
        
        
        
