# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import glob

class CoinCounter:

    def __init__(self, imagePath, name='Image'):
        self.imageName = name
        self.imageOriginal = cv.imread(imagePath)
       # self.__workingImage = cv.cvtColor(self.imageOriginal, cv.COLOR_BGR2GRAY)
        self.__workingImage =self.imageOriginal[:,:,2]
        self.__imageCounted = self.imageOriginal.copy()
        self.__edges = np.array([])
        self.__thresh = np.array([])
        self.__contours = np.array([])
        self.__circles = np.array([])
        self.__correctContours = []
        
        self.valores = {
                1 :  10153.8,
                2 :  14095.9,
                5 : 17590.25,
                10 : 15288.8,
                20 : 19249.1,
                50 : 23095.6,
                100 : 21225.63,
                200 : 25179
            }

        self.__total = 0

    def __showImage(self, image, title):
        win_title= f'{self.imageName} {title}'
        cv.imshow(win_title, image)
        cv.waitKey(0)
        cv.destroyWindow(win_title)
        
    
    def showImageOriginal(self, text='original'):
        return self.__showImage(self.imageOriginal, text)
    
    def showImageProcessed(self, text='processed'):
        return self.__showImage(self.__workingImage,text )
    
    def showContors(self, text='contors'):
        imgC = cv.drawContours(self.imageOriginal, self.__correctContours, -1, (0,0,255),2)
        return self.__showImage(imgC, text)
    
    def showThresholds(self,text='edges'):
        return self.__showImage(self.__thresh, text)
        
    def showOutput(self,text='output'):
        return self.__showImage(self.__imageCounted, text)
    '''
    Faz um re-dimensionamento (se aplicavel) e aplica filtros para obter melhores resultado
    '''
    def preProcessImage(self,resize=False):
        blur = []
        if(resize):
            w, h, a = self.imageOriginal.shape
            img= cv.resize(self.__workingImage, (int(h/2), int(w/2)))
            blur=cv.GaussianBlur(img,(7,7),0)
        else:     
            blur=cv.GaussianBlur(self.__workingImage,(7,7),0)
           
        
        self.__workingImage = blur
        self.__preProcessed = True
        return self.__preProcessed
    
    '''
    Tendo em conta a imagem anterior, calcula o valor em centimos das moedas presentes
    '''

    def showBoundingBox(self, boundingBox=True ):
        for i in   self.__correctContours:
            if boundingBox:
                (x,y), r = cv.minEnclosingCircle(i)
                cv.circle( self.__imageCounted,(int(x),int(y)), int(r), (0,0,255), 2 )
            else:
                (x,y,w,h) = cv.boundingRect(i)
                cv.rectangle(self.__imageCounted, (x,y), (x+w,y+h), (0,0,255), 2)

    
    def countCoins(self, boundingBox=True):
        self.__detectEdges()
        self.__getContourCoords()
        total = 0

        for i in   self.__correctContours:
            M = cv.moments(i)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            area = cv.contourArea(i)
            aux = self.valores[1]
            coin = 1
            for j in self.valores:
                areaDiff = abs(area-self.valores[j])
                if areaDiff < aux:
                    aux = areaDiff
                    coin = j
            cv.putText(self.__imageCounted, f"{coin}",(cX,cY), cv.FONT_HERSHEY_SIMPLEX , 1, (0,0,255), 2)
            total = total + coin
          
        self.__total = round(total/100,2)
        cv.putText(self.__imageCounted, f"total: {self.__total} E",(50,50), cv.FONT_HERSHEY_SIMPLEX , 1, (0,0,255), 2)
        return total
                




    def __getContourCoords(self):
        
        contours = self.__contours[0]
        h = self.__contours[1]
        a=0
        for cont in range(len(contours)):
          
            leftmost = (contours[cont][contours[cont][:,:,0].argmin()][0])
            rightmost = (contours[cont][contours[cont][:,:,0].argmax()][0])
            topmost = (contours[cont][contours[cont][:,:,1].argmin()][0])
            bottommost = (contours[cont][contours[cont][:,:,1].argmax()][0])
            points = (leftmost,rightmost,topmost,bottommost)
            
            centerX = (leftmost[0]+rightmost[0])/2
            centerY = (topmost[1]+bottommost[1])/2
            radius = abs((rightmost[0]-leftmost[0])/2)
            area_circulo = round(np.pi * radius * radius,2) # area do circulo
            area_contour = cv.contourArea(contours[cont])
          

            if (abs(area_circulo-area_contour)<2000 and h[0][cont][2] == -1  and area_contour>8800 ):
                a=a+1
              
                self.__correctContours.append(contours[cont])
            
    
    def __detectEdges(self):
        self.__edges = cv.Canny(self.__workingImage,70,200) #threshold value do gradiente da intensidade
        self.__thresh = cv.adaptiveThreshold(self.__edges, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 0)
        
        strElem = cv.getStructuringElement(cv.MORPH_ELLIPSE,(2,2))
        morph = cv.morphologyEx(self.__thresh,cv.MORPH_CLOSE,strElem,iterations=3) ## ajuda com os objetos que se toquem 3
        self.__contours = cv.findContours(morph,cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

def runAllImages(imagesPaths, showSteps=False, showFinal=True):
    for idx, img in enumerate(imagesPaths):
        c = CoinCounter(img, 'img'+str(idx))
        c.showImageOriginal()
        c.preProcessImage(False)
        if(showSteps):
            c.showImageProcessed('P1')
            c.countCoins()
            c.showImageProcessed('Count')
            c.showThresholds('P2')
            c.showContors('Contors')
               
        else:
            
            total = c.countCoins()
            print(f'Img at {img} com valor {total}')
        if(showFinal):
            c.showBoundingBox()
            c.showOutput('Final')
           

def run1Image(imagePath):
    cc = CoinCounter(imagePath)
    cc.showImageOriginal()
    cc.preProcessImage()
    cc.showImageProcessed('PreProcessing')
    print('val' , cc.countCoins())
    cc.showContors('Contors')
    cc.showThresholds('Thresholds')
    cc.showOutput('Output')
    
    
if __name__ == '__main__':
    fileDir = "TP1/PIV_20_21_TL1_imagens_treino/"
    imagesPaths = glob.glob(f'{fileDir}*.jpg')   
    
   # run1Image(imagesPaths[0])
    runAllImages(imagesPaths)
