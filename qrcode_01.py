import importfile as imf
#s=input("Insert the string for the QR-Code: ")
m=[[True,"0001"],[True,"0010"],[True,"0100"]] #Mode indicator -> Num - Alphanum - Byte
#Data Analysis
iso_8859_1_chars = [chr(i) for i in range(256)] # character list from ISO 8859-1
an = list(imf.st.digits+imf.st.ascii_uppercase+' '+'$'+'%'+'*'+'+'+'-'+'.'+'/'+':') #alphanumeric character list
v=imf.tb.vq
vb=imf.tb.vb
t=imf.tb.tb
er=imf.tb.er
C=imf.tb.cd
rb=imf.tb.rb
ncm=imf.tb.ncm
#Message preparation
def md(sr: str): #mode of the QR Code
    l=len(sr)
    c,min=[0,0,0],3 #min is out of range for comfort
    def d_enu(): #numeric mode -> completed
        if len(sr)%3==0:
            n=[[0 for _ in range(3)] for _ in range(int(l/3))]
            for i in range(len(n)):
                for j in range(3):
                    n[i][j]=sr[3*i+j]
        else:
            n=[[0]*3 for _ in range(int(l/3))]+([[0]*(l%3)] if l%3!=0 else [])
            for i in range(len(n)):
                for j in range(len(n[i])):
                    n[i][j]=sr[3*i+j]
        c=[0 for _ in range(3)] #simply c=[0,0,0]
        for i in range(len(n)):
            n[i]=int(''.join(map(str,n[i])))
            match len(str(n[i])):
                case 1:
                    c[0]+=1
                case 2:
                    c[1]+=1
                case 3:
                    c[2]+=1
        b=[[0]*10 for _ in range(c[2])]+[[0]*7 for _ in range(c[1])]+[[0]*4 for _ in range(c[0])]
        for i in range(len(n)):
            for j in range(len(b[i])):
                b[i][len(b[i])-(j+1)]=n[i]%2
                n[i]=imf.mt.floor(n[i]/2)
        return b
    def d_ean(): #alphanumeric mode -> completed
        if len(sr)%2==0:
            n=[[0 for _ in range(2)] for _ in range(int(l/2))]
            for i in range(len(n)):
                for j in range(2):
                    n[i][j]=sr[2*i+j]
        else:
            n=[[0]*2 for _ in range(int(l/2))]+([[0]*(l%2)] if l%2!=0 else [])
            for i in range(len(n)):
                for j in range(len(n[i])):
                    n[i][j]=sr[2*i+j]
        for i in range(len(n)):
            for j in range(len(n[i])):
                for k in range(len(an)):
                    if n[i][j]==an[k]:
                        n[i][j]=k
                        break
        b,c=[0 for _ in range(len(n))],[0,0]
        for i in range(len(b)):
            if len(n[i])==2:
                b[i]=45*n[i][0]+n[i][1]
            else:
                b[i]=45*n[i][0]
        if len(sr)%2==0:
            b1=[[0]*11 for _ in range(len(sr)//2)]
        else:
            b1=[[0]*11 for _ in range((len(sr)-1)//2)]+[[0]*6]
        for i in range(len(b)):
            for j in range(len(b1[i])):
                b1[i][len(b1[i])-(j+1)]=b[i]%2
                b[i]=imf.mt.floor(b[i]/2)
        return b1
    def d_eby(): #byte mode -> completed
        b,n=[[0]*8 for _ in range(l)],[0 for _ in range(l)]
        for i in range(l):
            for j in range(len(iso_8859_1_chars)):
                if sr[i]==iso_8859_1_chars[j]:
                    n[i]=j
        for i in range(l):
            for j in range(len(b[i])):
                b[i][len(b[i])-(j+1)]=n[i]%2
                n[i]=imf.mt.floor(n[i]/2)
        return b
    def vf(mode: int,len: int): #Version finder -> completed
        for i in range(40):
            if v[i][mode]>=len:
                return i+1
        return None
    def lb(leng: int,blen: int): #len in binary -> completed
        b=[0]*blen
        for i in range(blen):
            b[blen-(1+i)]=leng%2
            leng=imf.mt.floor(leng/2)
        return b 
    def bd(a:str)->int: #binary to decimal -> completed
        r=0
        for i in range(len(a)):
            r+=imf.mt.pow(2,8-(1+i))*int(a[i])
        return int(r)
    def cd(v:int,bl: list[str]): #Codewords division -> completed
        ba,bb=[],[]
        i=0
        for _ in range(C[v-1][1]):
            bc=[]
            for _ in range(C[v-1][2]):
                if i<len(bl):
                    bc.append(''.join(bl[i]))
                    i+=1
            ba.append(bc)
        if C[v-1][3]:
            for _ in range(C[v-1][4]):
                bc=[]
                for _ in range(C[v-1][5]):
                    bc.append(''.join(bl[i]))
                    i+=1
            bb.append(bc)
        return [ba,bb]
    def fm(m:list,e:list)->list: #final message structure in base10
        f,mxd=[],max(len(blc) for blc in m)
        for i in range(mxd):
            for blc in m:
                if i<len(blc):
                    f.append(blc[i])
        mxe=max(len(blc) for blc in e)
        for i in range(mxe):
            for blc in e:
                if i<len(blc):
                    f.append(blc[i])
        return f
    #mode check and first binary set-up
    for i in range(l):
        for j in range(10): #num
            if sr[i]==str(j):
                c[0]+=1
                break
        for j in an: #alphanum
            if sr[i]==j:
                c[1]+=1
                break
        for j in iso_8859_1_chars: #byte
            if sr[i]==j:
                c[2]+=1
                break
    for i in range(3):
        if c[i]<l:
            m[i][0]=False
        else:
            if i<min:
                min=i
    match min: 
        case 0: #num
            b=d_enu()
            vqr=vf(0,l)
            mi=m[0][1]
        case 1: #alphanum
            b=d_ean()
            vqr=vf(1,l)
            mi=m[1][1]
        case 2: #byte
            b=d_eby()
            vqr=vf(2,l)
            mi=m[2][1]
    b1=[''.join(str(x) for x in st) for st in b]

    if vqr>0 and vqr<10:
        bl=vb[0][min]
    elif vqr>9 and vqr<27:
        bl=vb[1][min]
    elif vqr>26 and vqr<41:
        bl=vb[2][min]
    else:
        return None
    lB,tb=lb(l,bl),t[vqr-1]*8
    b2,tl=[mi,''.join(str(x) for x in lB),''.join(b1)],0
    for i in range(len(b2)): #b2 len
        tl+=len(b2[i])
    if tl<tb:
        z=tb-tl
        tl+=z
        if z>=4:
            for i in range(4):
                b2+='0'
        else:
            for i in range(z):
                b2+='0'
    b2=''.join(b2)
    while len(b2)%8!=0:
        b2+='0'
    b3=[['0']*8 for _ in range(int(len(b2)/8))]
    for i in range(len(b3)):
        for j in range(8):
            b3[i][j]=b2[8*i+j]
        b3[i]=str(''.join(b3[i]))
    lb3,ad=int((tb-len(b3)*8)/8),[['11101100'],['00010001']]
    bo=False
    for i in range(lb3):
        match bo:
            case False:
                b3+=ad[0]
                bo=True
            case True:
                b3+=ad[1]
                bo=False   
    b4=cd(vqr,b3)
    b4_10=[[[0 for _ in range(len(b4[i][j]))] for j in range(len(b4[i]))] for i in range(len(b4))]
    ec_10=[[[0 for _ in range(er[vqr-1])] for _ in range(len(b4[i]))] for i in range(len(b4))]
    #parallel matrix to b4 but in base10
    for i in range(len(b4)): 
        for j in range(len(b4[i])): 
            for k in range(len(b4[i][j])):
                b4_10[i][j][k]=bd(b4[i][j][k])
            data_block = b4_10[i][j] + [0] * er[vqr-1]
            ecc = imf.gf.poly_div(data_block, imf.gf.ggen(er[vqr-1]))
            for k in range(len(ecc)):
                ec_10[i][j][k]=ecc[k]
    #final message structuring
    f_10=fm(b4_10,ec_10)
    fb=[[] for _ in range(len(f_10))]
    for i in range(len(f_10)):
        for j in range(len(f_10[i])):
            fb[i].append(imf.gf.db(f_10[i][j]))
    fb = ''.join(str(bit) for byte in fb for bit in byte)+'0'*rb[vqr-1]
    dim=[(vqr-1)*4+21,(vqr-1)*4+21]
    return fb,dim
#QR-Code preparation
#m,dim=md(s)
#mb,dim=md("Questo è un messaggio di test molto lungo per forzare la generazione di un QR code di versione 7. Deve superare i 122 caratteri!") #tester line
mb,dim=md("www.google.com")
vqr=int((dim[0]-21)/4+1)
qr=[[0]*(dim[1]+2) for _ in range(dim[0]+2)]
qrv=[['t']*(dim[1]+2) for _ in range(dim[0]+2)]
#outer border ->4
for i in range(dim[0]+2):
    qr[i][0]=qr[0][i]=4
    qr[i][dim[0]+1]=qr[dim[0]+1][i]=4
    qrv[i][0]=qrv[0][i]='f'
    qrv[i][dim[0]+1]=qrv[dim[0]+1][i]='f'
#Finder patterns
for i in range(1,dim[0]+1):
    if i==1 or i==7:
        for j in range(1,dim[1]+1):
            if j<8 or j>=dim[1]-6:
                qr[i][j]=1
    elif i>1 and i<7:
        for j in range(1,dim[1]+1):
            if j==1 or j==7 or j==dim[1]-6 or j==dim[1]:
                qr[i][j]=1
    if i>=3 and i<=5:
        for j in range(1,dim[1]+1):
            if (j>=3 and j<=5) or (j>=dim[1]-4 and j<=dim[1]-2):
                qr[i][j]=1
    elif i>=dim[0]-4 and i<=dim[0]-2:
        for j in range(1,dim[1]+1):
            if j>=3 and j<=5:
                qr[i][j]=1
    if i==dim[0]-6 or i==dim[0]:
        for j in range(1,dim[1]+1):
            if j<8:
                qr[i][j]=1
    elif i>dim[0]-6 and i<dim[0]:
        for j in range(1,dim[1]+1):
            if j==1 or j==7:
                qr[i][j]=1
for i in range(1,dim[0]+1):
    if i>=1 and i<=8:
        for j in range(1,dim[1]+1):
            if j<9 or j>=dim[1]-7:
                qrv[i][j]='f'
    elif i>=dim[0]-7 and i<=dim[0]:
        for j in range(1,dim[1]+1):
            if j<9:
                qrv[i][j]='f'
#alignment pattern
def pt(grid:list,p1:int,p2:int)->bool:
    for i in range(-2,3):
        for j in range(-2,3):
            if grid[p1+i][p2+j]==1:
                return False
    return True
if vqr-1!=0:
    for p1 in ncm[vqr-1][0]:
        for p2 in ncm[vqr-1][1]:
            if pt(qr,p1,p2):
                for i in range(-2,3):
                    if p1+i==p1-2 or p1+i==p1+2:
                         for j in range(-2,3):
                            qr[p1+i][p2+j]=1
                    else:
                        qr[p1+i][p2-2]=1
                        qr[p1+i][p2+2]=1
                    if i==0:
                        qr[p1][p2]=1
                    if p1+i>=p1-2 and p1+i<=p1+2:
                        for j in range(-2,3):
                            qrv[p1+i][p2+j]='f'
#timing patterns
for i in range(7,dim[0]-7,2):
    qr[i][7]=qr[7][i]=1
qr[dim[0]-7][9]=1
for i in range(7,dim[0]-7):
    qrv[i][7]=qrv[7][i]='f'
qrv[dim[0]-7][9]='f'
#version information (vqr>=7) ->3
if vqr >= 7:
    for i in range(6):
        for j in range(3):
            qr[dim[0]-(8+j)][i+1]=3
            qrv[dim[0]-(8+j)][i+1]='f'
    for i in range(6):
        for j in range(3):
            qr[i+1][dim[1]-(8+j)]=3
            qrv[i+1][dim[1]-(8+j)]='f'   
else:
    #format information area ->2
    for i in range(dim[0]+1):
        if (i>0 and i<10) or i>dim[0]-7:
            if qr[i][9]==1:
                continue
            qr[i][9]=2
            qrv[i][9]='f'
    for i in range(dim[1]+1):
        if (i>0 and i<10) or i>dim[0]-8:
            if qr[9][i]==1:
                continue
            qr[9][i]=2
            qrv[9][i]='f'       
#data bits placement -> to control the downward placement
def pbd(qr,db,qrv):
    r,c,bi,d=len(qr),len(qr[0]),0,-1
    cl,rs=c-2,r-1
    while cl>0:
        if cl==6:
            cl-=1
        for i in range(r):
            ra=rs if d==-1 else r-1-rs
            for a in [cl,cl-1]:
                if qrv[ra][a]=='t' and bi<len(db):
                    qr[ra][a]=int(db[bi])
                    bi+=1
            rs+=d
            if rs<0 or rs>=r:
                d*=-1
                rs+=d
        cl-=2
pbd(qr,mb,qrv)
for i in range(dim[0]+2):
    print(qr[i])
print(mb)
print(dim)
#Visual rappresentation
for i in range(len(dim)):
    dim[i]=10*(dim[i]+1)
sc=imf.pg.display.set_mode([dim[0]+20,dim[1]+20])

def draw(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j]==1:
                imf.pg.draw.rect(sc,(0,0,0),imf.pg.Rect(i*10+2,j*10+2,10,10))
            elif grid[i][j]==0 or grid[i][j]==4:
                imf.pg.draw.rect(sc,(255,255,255),imf.pg.Rect(i*10+2,j*10+2,10,10))
            elif grid[i][j]==3:
                imf.pg.draw.rect(sc,(0,255,0),imf.pg.Rect(i*10+2,j*10+2,10,10))
            else:
                imf.pg.draw.rect(sc,(0,0,255),imf.pg.Rect(i*10+2,j*10+2,10,10))
def drawv(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j]=='t':
                imf.pg.draw.rect(sc,(0,255,0),imf.pg.Rect(i*10+2,j*10+2,10,10))
            else:
                imf.pg.draw.rect(sc,(255,0,0),imf.pg.Rect(i*10+2,j*10+2,10,10))