import cv2 as cv2
import numpy as np
import collections
import math
from time import time

 
class drawStuff():
    
    
    def draw_rectangles(self,x,y,w,h,objClassified,objId,frame1):
            
         if (objClassified==0):
             
        
             cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
             cv2.putText(frame1, str("Carro"),(x,y-10) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
             
             cv2.putText(frame1, str(objId),(x+20,y-30) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
         if (objClassified==1):
             
        
             cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)
             cv2.putText(frame1, str("Pessoa"),(x,y-10) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)    
                    
             cv2.putText(frame1, str(objId),(x+20,y-30) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)

         if (objClassified==2):
             
        
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frame1, str("Outro"),(x,y-10) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            
            cv2.putText(frame1, str(objId),(x+20,y-30) , cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)


    def draw_lines(self,points,frame1):
        
        if(len(points)>0):
            
            for i in range (len (points)):
                
                if (points[i][0] ==0):
                    
                    cv2.circle(frame1,(points[i][1],points[i][2]),1,(0, 255, 0),1)
                if (points[i][0] ==1):
                   
                    cv2.circle(frame1,(points[i][1],points[i][2]),1,(0, 0, 255),1)
                if (points[i][0] ==2):
        
                    cv2.circle(frame1,(points[i][1],points[i][2]),1,(255, 0, 0),1)
                
                
class ClassifiedObject():
    
     def __init__(self, typeObj,posX,posY,identifier):
        
        self.__typeObj = typeObj
        self.__posX = posX
        self.__posY = posY
        self.__identifier = identifier
        
        self.objTime = time()
        
        
     def getposX(self):
        
        return self.__posX
    
     def getposY(self):
        
        return self.__posY
    
     def getType(self):
        
         return self.__typeObj
     
     def getidentifier(self):
         
         return self.__identifier
     
     def updateCoords(self, posX, posY):
         
         self.__posX = posX
         self.__posY = posY
         self.objTime = time()
     
     def updateType(self,val):
        
        self.__typeObj = val
    
     def getAlive(self):
         return self.alive
         
     
     def tClock(self):
        
        return time() - self.objTime
    
     def alive(self):
        return self.tClock() < 6
    

class ClassifiedObjects():
    
    def __init__(self):
        
        self.__listClassifiedObjects = []
        self.__counter = 0
        
        
        
    def addToList(self,classifiedObject):
        
        self.__listClassifiedObjects.append(classifiedObject)
    
    def getList(self):
        
        return self.__listClassifiedObjects
    
    
    def euclideanDistance(self, x1, x2, y1, y2):
        return math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))
    
    
    
    def findClosestObject(self,posX,posY,typeObj):
        
        if (len(self.__listClassifiedObjects) <1):
            
            return False
        
        else:
        
            dicDist = {}
            
            c=0
            
          
            
            for i in range (len(self.__listClassifiedObjects)):
                
             
                if  self.__listClassifiedObjects[i].alive():
                    
                    if self.__listClassifiedObjects[i].getType() ==typeObj:
                    
                        c=1
                        
                    
                        x = self.__listClassifiedObjects[i].getposX()
                            
                        y = self.__listClassifiedObjects[i].getposY()
                        
                        dist = self.euclideanDistance(posX,x,posY,y)
                        dicDist[i] = dist
     
            if (c==0):
                return False
            
        
                
            minval = min(dicDist.values())
            
            
            if minval <30:
                
                idx = min(dicDist, key=dicDist.get)

                return idx
    
           
            else: 
                return False
 
        #arrDistances = [self.euclideanDistance(posX,i.getposX,posY,i.getposY) for i in self.__listClassifiedObjects]
   
        
    def createClassifiedObject(self, objType,posX,posY):
        
       
        idObj = self.__counter

        if (objType ==0):
            
            obj = ClassifiedObject(0,posX,posY,idObj)
            self.addToList(obj)
            
        
        if (objType ==1):
            
            obj = ClassifiedObject(1,posX,posY,idObj)
            self.addToList(obj)
        
        if (objType ==2):
            
            obj = ClassifiedObject(2,posX,posY,idObj)
            self.addToList(obj)
        
        self.__counter = self.__counter+1
        
    
    def check_border(self,posX):
        
        #1280,720
        if (posX < 10 or posX >1270):
            return False
        else:
            return True
       # left = x < 10
       # right = x > 1270
       
       
    def classify(self,width,height,area,posX,posY):
    
        #self.checkDeadClassifiedObjects()
        
        ratio = round(width / height,3)
            
            
        if((ratio) >= 1.10 and area > 1500 and self.check_border(posX)):
            
            
            if (self.findClosestObject(posX,posY,0)!=False):
                
                ind = self.findClosestObject(posX,posY,0)

                self.__listClassifiedObjects[ind].updateType(0)
                self.__listClassifiedObjects[ind].updateCoords(posX, posY)
                
                return self.__listClassifiedObjects[ind]
                
            elif (self.findClosestObject(posX,posY,0)==False):
                self.createClassifiedObject(0,posX,posY)
                
                return self.__listClassifiedObjects[-1]
            


        if((ratio) >= 0.34 and ratio <= 0.80 and area < 5000 and self.check_border(posX)):
            
                
            if (self.findClosestObject(posX,posY,1)!=False):
                    
               ind = self.findClosestObject(posX,posY,1)
               
               self.__listClassifiedObjects[ind].updateType(1)
               self.__listClassifiedObjects[ind].updateCoords(posX, posY)
               
               return self.__listClassifiedObjects[ind]
                    
            elif (self.findClosestObject(posX,posY,1)==False):
                self.createClassifiedObject(1,posX,posY)
                
                return self.__listClassifiedObjects[-1]

                        
        if((ratio) > 0.80 and (ratio) < 1.10 and area>850 and self.check_border(posX) ):
            
     
           if (self.findClosestObject(posX,posY,2)!=False):
                    
               ind = self.findClosestObject(posX,posY,2)
               
               self.__listClassifiedObjects[ind].updateType(2)
               
               self.__listClassifiedObjects[ind].updateCoords(posX, posY)
               
               return self.__listClassifiedObjects[ind]
           elif (self.findClosestObject(posX,posY,2)==False):
               
               self.createClassifiedObject(2,posX,posY)
               return self.__listClassifiedObjects[-1]

        return False
    
        
        


class RunVideo():
    
    def __init__(self, filePath):

        self.cap = cv2.VideoCapture(filePath)
        self.backgroundSub = cv2.createBackgroundSubtractorMOG2(history =500,varThreshold = 22, detectShadows = True)


#backgroundSub = cv2.createBackgroundSubtractorMOG2(128,cv2.THRESH_BINARY,1)

    def findBackground(self,frame2):
       
        
        gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
        blurm = cv2.medianBlur(gray, 3)
        blur = cv2.GaussianBlur(blurm,(3,3),0)
        diff = self.backgroundSub.apply(blur,0.002)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    
        return diff, thresh
    
    
    def doRun(self):
        
        classObjects = ClassifiedObjects()
        

        xd = collections.deque([])
        try:
            ret, frame1 = self.cap.read()
            ret, frame2 = self.cap.read()
        
            #points =collections.deque([])
            
        
            
            if (self.cap.isOpened()== False):
                print("Error opening video stream or file")
                
            while self.cap.isOpened():

                
                if cv2.waitKey(5) == ord('q') or not ret:
                    break
                
                diff,thresh = self.findBackground(frame2)
                
                
                
                closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((2, 2), np.uint8()), iterations = 5)
                dilate = cv2.dilate(closing, np.ones((3, 3), np.uint8()))
                 
                contours, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                
                 
                for contour in contours:
                    
                 
                    (x, y, w, h) = cv2.boundingRect(contour)
                    
                    if cv2.contourArea(contour) < 470:
                        continue
                    
                    
                    pos_x = int(x+w/2)
                    pos_y = int(y+h/2)
                    
                    
                    objClass = classObjects.classify(w, h, cv2.contourArea(contour), x, y)
                    drawS = drawStuff()
                    
                    if (objClass != False):
                        
                        #classObject = classObjects.getList()[-1]
                    
                        objClassType = objClass.getType()
                        
                        objId = objClass.getidentifier()
                        
                        
                      #DRAW STUFF
                         
                        #drawS = drawStuff(frame1)
                        drawS.draw_rectangles(x,y,w,h,objClassType,objId,frame1)


                        if objClassType ==0:
                            
                            xd.append((0,pos_x,pos_y))
                            
                        if objClassType ==1:
                            
                            xd.append((1,pos_x,pos_y))
                            
                        if objClassType ==2:
                            
                            xd.append((2,pos_x,pos_y))
                    
               
                drawS.draw_lines(xd,frame1)
                    
                image = cv2.resize(frame1, (1280,720))
                
                cv2.imshow("dilated" , dilate)
                cv2.imshow("feed", frame1)
                 
                frame1 = frame2
                 
                ret, frame2 = self.cap.read()
            
               
            cv2.destroyAllWindows()
            self.cap.release()
                 
          
        except Exception as e:
             print(e)
             cv2.destroyAllWindows()
             self.cap.release()
    

if __name__ == '__main__':
    
    #filePath = 'camera1.mov'
    filePathDuarte = 'C:/Users/duart/OneDrive/Ambiente de Trabalho/ISEL/VIDEO/camera1.mov'
    
    
    runV = RunVideo(filePathDuarte)
    runV.doRun()




    



