from PIL import Image
from math import floor

# Name of the image file.
filename = "ruins.jpg"

input_image = Image.open(filename).convert("L").convert("RGB")
pixel_map = input_image.load()
width, height = input_image.size

print(input_image.mode)

offset = 0
base = 16

def quantize_color(R, G, B):
    factor = 1

    newR = round(factor * R / 255.0) * (255 // factor)
    newG = round(factor * G / 255.0) * (255 // factor)
    newB = round(factor * B / 255.0) * (255 // factor)
    return (newR, newG, newB)

for y in range(1, height-1):
    for x in range(1, width-1):
        R, G, B = pixel_map[x, y]
        newR, newG, newB = quantize_color(R, G, B)
        pixel_map[x, y] = newR, newG, newB

        quantization_err = tuple(map(lambda i, j: i - j, (R, G, B), (newR, newG, newB)))
        
        pixel_map[x + 1, y    ] = tuple(pixel_map[x + 1, y    ][i] + floor(quantization_err[i] * ((7 + offset) / base)) for i in range(3))
        pixel_map[x + 1, y + 1] = tuple(pixel_map[x + 1, y + 1][i] + floor(quantization_err[i] * ((1 + offset) / base)) for i in range(3))
        pixel_map[x    , y + 1] = tuple(pixel_map[x    , y + 1][i] + floor(quantization_err[i] * ((5 + offset) / base)) for i in range(3))
        pixel_map[x - 1, y + 1] = tuple(pixel_map[x - 1, y + 1][i] + floor(quantization_err[i] * ((3 + offset) / base)) for i in range(3))

# input_image.show()
input_image.save(filename.replace(".jpg", "_dithered.png"))