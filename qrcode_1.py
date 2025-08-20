import qrcode_01 as qr

r=True
qr.imf.pg.init()
qr.sc.fill((255,255,255))
while r:
    for e in qr.imf.pg.event.get():
        if e.type==qr.imf.pg.QUIT:
            r=False
        k=qr.imf.pg.key.get_pressed()
        if k[qr.imf.pg.K_a]==True:
            qr.draw(qr.qr)
        if k[qr.imf.pg.K_s]==True:
            qr.drawv(qr.qrv)
        if k[qr.imf.pg.K_d]==True:
            qr.sc.fill((255,255,255))
    qr.imf.pg.display.update()
qr.imf.pg.quit()