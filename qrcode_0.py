#quiet zone of 4 px
import pygame as pg
import time as tm

dim=[310,310]
sc,z=pg.display.set_mode(dim),[int((dim[0]-20)/10),int((dim[0]-20)/10)]

qr=[[0 for _ in range(z[0])] for _ in range(z[1])]
#Base elements: Position pattern
for i in range(len(qr)):
    if i==0 or i==6:
        for j in range(len(qr[i])):
            if j<7 or j>z[1]-8:
                qr[i][j]=1
            else:
                j+=z[0]-14
    elif i<6 and i>0:
        for j in range(z[1]):
            if j==0 or j==6 or j==z[1]-7 or j==z[1]-1:
                qr[i][j]=1
    elif i==z[0]-7 or i==z[0]-1:
        for j in range(len(qr[i])):
            if j<7:
                qr[i][j]=1
            else:
                break 
    elif i>z[0]-7 and i<z[0]-1:
        qr[i][0]=1
        qr[i][6]=1
    else:
        i+=z[0]-14
        
for i in range(z[0]):
    if i>=2 and i<=4:
        for j in range(z[1]):
            if (j>=2 and j<=4) or (j>=z[0]-5 and j<=z[0]-3):
               qr[i][j]=1
    if i>=z[0]-5 and i<=z[0]-3:
        for j in range(z[1]):
            if j>=2 and j<=4:
               qr[i][j]=1
#Base elements: Alignment pattern               
for i in range(z[0]-9,z[0]-4):
    if i==z[0]-9 or i==z[0]-5:
        for j in range(z[0]-9,z[0]-4):
            qr[i][j]=1
    else:
        qr[i][z[1]-9]=1
        qr[i][z[1]-5]=1
qr[z[0]-7][z[1]-7]=1
#Base elements: Timing
for i in range(8,z[0]-8):
    if i%2==0:
        qr[i][6]=1
qr[8][z[1]-8]=1
for i in range(8,z[1]-8):
    if i%2==0:
        qr[6][i]=1
        
def draw(grid,screen=sc):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            match grid[i][j]:
                case 0:
                    pg.draw.rect(screen,(255,255,255),pg.Rect(i*10+20,j*10+20,10.0,10.0))
                case 1:
                    pg.draw.rect(screen,(0,0,0),pg.Rect(i*10,j*10,10.0,10.0))