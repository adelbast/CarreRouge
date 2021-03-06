from tkinter import *
import random
from timeit import default_timer
import tkinter.messagebox

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
            if evt.x <70 or evt.x>530:
                self.parent.actif=0

            if evt.y <70 or evt.y>530:
                self.parent.actif=0
            
        
    def gotclick(self,evt):
        lestags=self.canevas.gettags("current")
        if "carre" in lestags:
            self.carrebouge=1
        if self.parent.aClique==0:
            self.parent.aClique=1
            self.parent.modele.start = default_timer()
            
    def forgotclick(self,evt):
        self.carrebouge=0

    def afficherTimer(self):
        self.parent.modele.score = default_timer()-self.parent.modele.start
        print(self.parent.modele.score)
        tkinter.messagebox.showinfo("GameOver","Vous avez survécu "+ (str)(round(self.parent.modele.score))+ " secondes" )

        
        
    def miseajour(self,modele):
        self.canevas.delete(ALL)
        for i in modele.pions:
            self.canevas.create_rectangle(i.x1,i.y1,i.x2,i.y2,fill="blue", tags=("pion"))
        j=modele.carre
        self.canevas.create_rectangle(j.x1,j.y1,j.x2,j.y2,fill="red", tags=("carre"))
        self.canevas.addtag_overlapping ("collision",j.x1,j.y1,j.x2,j.y2)
        lestags=self.canevas.gettags("collision")
        if "pion" in lestags:
            print("mort modele")
            self.parent.actif=0
             
class Pion():
    def __init__(self,parent,x1,y1,x2,y2,directX,directY):
        self.parent=parent 
        self.x1=x1
        self.x2=x2
        self.y1=y1
        self.y2=y2
        self.acceleration = 1
        self.directX=directX  
        self.directY=directY 
        
    def bouge(self):
        
        if self.x1 <= 0 or self.x2 >= 500:
            self.directX = self.directX * -1
        if self.y1 <= 0 or self.y2 >= 500:
            self.directY = self.directY * -1
        
        self.x1+=self.directX* self.acceleration
        self.x2 += self.directX* self.acceleration
        self.y1+=self.directY* self.acceleration
        self.y2 += self.directY * self.acceleration   
        """
        self.parent.pions[0].x1+=
        self.parent.pions[0].x2+=1
        self.parent.pions[0].y1+=1
        self.parent.pions[0].y2+=1

        self.parent.pions[3].x1-=1
        self.parent.pions[3].x2-=1
        self.parent.pions[3].y1-=1
        self.parent.pions[3].y2-=1
        """ 
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
        self.score=0
        
    
    def creerPions(self):
            self.pions.append(Pion(self,60,60,160,160,2,2))
            self.pions.append(Pion(self,355,340,455,360,-2,-2))
            self.pions.append(Pion(self,330,135,390,185,-2,2))
            self.pions.append(Pion(self,115,350,145,410,2,-2))
            
    def miseajour(self):
        for i in self.pions:
            i.bouge()
    def carrebouge(self,x,y):
        self.carre.bouge(x,y)

    def resetJeu(self):
        self.__init__(self.parent)
            
class Controleur():
    def __init__(self):
        self.actif=1
        self.aClique=0
        self.tabScore=[]
        self.modele=Modele(self) 
        self.vue=Vue(self)
        self.vue.miseajour(self.modele)
        self.gameOn()
        self.vue.root.mainloop()
        
 
    def carrebouge(self,x,y):
        self.modele.carre.bouge(x,y)
        
    def gameOn(self):
        if self.actif:
            if self.aClique:
                self.modele.miseajour()
                self.vue.miseajour(self.modele)
                
                for i in self.modele.pions:
                    i.acceleration+=0.05
            self.vue.root.after(50,self.gameOn)
        else:
            self.vue.afficherTimer()
            if self.checkHighScore():
                self.demanderNom(self.checkHighScore())
            h=""
            compteur = 1;
            for i in self.tabScore:
                h+= str(compteur)+ "-" + i[0].upper()+ " " + str(round(i[1])) + " secondes" + "\n"
                compteur+= 1
            tkinter.messagebox.showinfo("High-Scores",h )   
            self.reset()

    def demanderNom(self, position):
        nom=tkinter.simpledialog.askstring("High-Score","Vous êtes " +  str(position)+" Entrez votre nom: ")
        self.tabScore.insert(position-1,[nom,self.modele.score])
        print (self.tabScore)
       
        


        
    def reset(self):
        self.modele.resetJeu()
        self.vue.miseajour(self.modele)
        self.actif=1
        self.aClique=0
        self.gameOn()

    def checkHighScore(self):
        if len(self.tabScore)==0:
            return 1
        position=1
        for i in range(5):
            print(self.tabScore[i])
            if self.modele.score > self.tabScore[i][1]:
                return position
            position+=1
            if position > len(self.tabScore) and position < 5:
                return position
        return False

    
            
                
        
        
        
    def highScore(self):
        tableau
        

            
if __name__ == '__main__':
    c=Controleur()
        
        
        
        
        
        
        
        
        
        
        
        
