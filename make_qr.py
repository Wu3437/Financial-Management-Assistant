import qrcode
img = qrcode.make('http://localhost:8000/index2.html')
img.save('qrcode.png')
print('Success')
