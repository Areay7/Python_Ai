import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_qr_code(file_name, qr_size=200, font_size=12):
    # 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(file_name)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((qr_size, qr_size))

    # 添加文件名文本
    draw = ImageDraw.Draw(qr_img)
    font_path = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = file_name
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((qr_size - text_width) // 2, qr_size + 10)

    # 计算文本位置，将文本放置在整张图的底部
    image_width, image_height = qr_img.size
    text_position = ((image_width - text_width) // 2, image_height - text_height - 10)

    # 添加文件名文本
    draw.text(text_position, text, font=font, fill="black")

    # 保存二维码图像
    qr_img.save(f"{file_name}.png")

# 程序入口
if __name__ == "__main__":
    file_name = input("请输入文件名：")
    qr_size = int(input("请输入二维码大小（默认200）：") or 200)
    font_size = int(input("请输入字体大小（默认12）：") or 12)
    generate_qr_code(file_name, qr_size, font_size)
    print("二维码已生成！")






