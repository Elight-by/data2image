from PIL import Image
import math
import os

MAX_VAL = 255

path_data_to_img = str(input("Enter path to file (Min file size: 50 bytes, max file size 255^4 x 3 bytes): "))

def to_dec(binary_str):
    return int(binary_str, 2)

def find_dimensions(x, ratio_limit=1.5):
    target = x + 5
    side = math.ceil(math.sqrt(target))
    
    a = side
    b = side

    while True:
        changed = False
        if (a - 1) * b >= target and (max(a - 1, b) / min(a - 1, b)) <= ratio_limit:
            a -= 1
            changed = True
        elif a * (b - 1) >= target and (max(a, b - 1) / min(a, b - 1)) <= ratio_limit:
            b -= 1
            changed = True
            
        if not changed:
            break
            
    return a, b

def pack_x(x):
    d = x % MAX_VAL
    res1 = x // MAX_VAL
    
    c = res1 % MAX_VAL
    res2 = res1 // MAX_VAL
    
    b = res2 % MAX_VAL
    a = res2 // MAX_VAL
    
    return a, b, c, d, 0, 0

file_bites = []

with open(path_data_to_img, 'rb') as file:
    byte = file.read(1) 
    while byte:
        binary_string = format(ord(byte), '08b')
        file_bites.append(binary_string)
        byte = file.read(1)

data_size = os.path.getsize(path_data_to_img)
if data_size < 50 or data_size > 12684751875:
    print("The file is too small or too big")
    exit()
pixel_nm = math.ceil(data_size/3)
a, b1 = find_dimensions(pixel_nm, 1.5)
x, y = -1, 0

img = Image.new('RGB', (a, b1), color=(255, 255, 255))
pixels = img.load()

index = 1

rgbs = []

for i in range(len(file_bites)):
    if index == 1:
        r = to_dec(file_bites[i])
    elif index == 2:
        g = to_dec(file_bites[i])
    elif index == 3:
        b = to_dec(file_bites[i])
        index = 0
        rgbs.append((r, g, b))
    index += 1


gs, bs = 0, 0

if len(file_bites) % 3 != 0:
    if (len(file_bites) - 1) % 3 == 0:
        gs = 255
        bs = 255
           
    elif (len(file_bites) - 2) % 3 == 0:
        gs = 0
        bs = 255

if bs == 255 and gs == 255:
    rgbs.append((r, gs, bs))
elif bs == 255 and gs == 0:
    rgbs.append((r, g, bs))


for index, i in enumerate(pack_x(pixel_nm)):
    if index == 0:
        r = i
    elif index == 1:
        g = i
    elif index == 2:
        b = i
        rtf = (r, g, b)
    elif index == 3:
        r = i
    elif index == 4:
        g = i
    elif index == 5:
        b = i
        rts = (r, g, b)


pixels[a-1, b1-1] = (000, gs, bs)
pixels[a-2, b1-1] = rts
pixels[a-3, b1-1] = rtf


for i in rgbs:
    if x+1 == a:
        x = 0
        y += 1
    else:
        x += 1
    pixels[x, y] = i

extension = []
file_extension = os.path.splitext(path_data_to_img)[1][1:]
for i in file_extension:
    extension.append(i)

for i in range(6-len(extension)):
    extension.append('')

rgbs = []
for index, i in enumerate(extension):
    if index == 0:
        try:
            r = int(format(ord(i), '08b'), 2)
        except:
            r = 0
    elif index == 1:
        try:
            g = int(format(ord(i), '08b'), 2)
        except:
            g = 0
    elif index == 2:
        try:
            b = int(format(ord(i), '08b'), 2)
        except:
            b = 0
        rgbs.append((r, g, b))

    if index == 3:
        try:
            r = int(format(ord(i), '08b'), 2)
        except:
            r = 0
    elif index == 4:
        try:
            g = int(format(ord(i), '08b'), 2)
        except:
            g = 0
    elif index == 5:
        try:
            b = int(format(ord(i), '08b'), 2)
        except:
            b = 0
        rgbs.append((r, g, b))

for index, i in enumerate(rgbs):
    if index == 0:
        pixels[a-5, b-1] = i
    elif index == 1:
        pixels[a-4, b-1] = i

img.save("generated.png")