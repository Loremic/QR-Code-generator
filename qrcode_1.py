import qrcode_0 as qr

r=True
qr.pg.init()
qr.sc.fill((255,255,255))
while r:
    
    for e in qr.pg.event.get():
        if e.type==qr.pg.QUIT:
            r=False
        k=qr.pg.key.get_pressed()
        if k[qr.pg.K_a]==True:
            qr.draw(qr.qr)
        if k[qr.pg.K_b]==True:
            qr.sc.fill((255,255,255))
    qr.pg.display.update()
qr.pg.quit()