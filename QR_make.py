# -*- coding: UTF-8 -*-
import qrcode
from PIL import Image

qr = qrcode.QRCode(box_size=10)
qr.add_data('最近コオドを使って決済するのがはやりなので遅まきながらコオドで遊んでみました')
qr.make()
img_qr = qr.make_image()
img_qr.save('./pyaudio/qr_10.png')