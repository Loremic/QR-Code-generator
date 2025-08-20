import math as mt
def db(n:int)->str:
    s=''
    if n==0:
        return '0'*8
    while n>=1:
        s=str(n%2)+s
        n//=2
    while len(s)!=8:
        s='0'+s
    return s

def lt():
    l,al=[0]*256,[0]*256
    x=1
    for i in range(255):
        al[i]=x
        l[x]=i
        x<<=1
        if x&0x100:
            x^=0x11D
    return l,al
l,al=lt()

def mgf(a:int,b:int)->int:
    if a==0 or b==0:
        return 0
    return al[(l[a]+l[b])%255]

def poly_mult(a:list,b:list)->list:
    r=[0]*(len(a)+len(b)-1)
    for i in range(len(a)):
        for j in range(len(b)):
            r[i+j]^=mgf(a[i],b[j])
    return r

def ggen(t:int)->list: 
    g=[1]
    for i in range(t):
        g=poly_mult(g,[1,al[i]])
    return g

def poly_div(a:list,b:list)->list:
    r=a[:]
    for i in range(len(a)-len(b)+1):
        c=r[i]
        if c!=0:
            for j in range(1,len(b)):
                r[i+j]^=mgf(b[j],c)
    return r[-(len(b)-1):]