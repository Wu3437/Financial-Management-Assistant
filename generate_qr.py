try:
    import qrcode
except ImportError:
    import subprocess
    subprocess.check_call(['python', '-m', 'pip', 'install', 'qrcode[pil]'])
    import qrcode

# 生成二维码
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data('http://localhost:8000/index2.html')
qr.make(fit=True)

img = qr.make_image(fill_color='black', back_color='white')

# 使用相对路径
img.save('qrcode.png')

print("二维码生成成功！")
print(f"文件路径: {__file__} 所在目录")
