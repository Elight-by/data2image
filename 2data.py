from PIL import Image

MAX_VAL = 255

img = Image.open(str(input("Enter the path to the file: ")))
pixels = img.load()

a, b = img.size

def unpack_x(first, second):
    for index, i in enumerate(first):
        if index == 0:
            a = i
        elif index == 1:
            b = i
        elif index == 2:
            c = i

    for index, i in enumerate(second):
        if index == 0:
            d = i
        elif index == 1:
            e = i
        elif index == 2:
            f = i

    return (a * MAX_VAL**3) + (b * MAX_VAL**2) + (c * MAX_VAL) + d

read_to = unpack_x(pixels[a-3, b-1], pixels[a-2, b-1])

rgbs = []
file_bites = []
x, y = -1, 0

for i in range(read_to):
    if x+1 == a:
        x = 0
        y += 1
    else:
        x += 1
    r, g, b = pixels[x, y]
    rgbs.append((r, g, b))

for i in rgbs:
    for n in i:
        file_bites.append(format(n, '08b'))

a, b = img.size
r, g, b = pixels[a-1, b-1]
if g == 255 and b == 255:
    file_bites.pop(len(file_bites)-1)
    file_bites.pop(len(file_bites)-1)
elif g == 0 and b == 255:
    file_bites.pop(len(file_bites)-1)

extension = ''
a, b = img.size
r, g, b = pixels[a-5, b-1]
color = (r, g, b)
for i in color:
    if i != 0:
        extension += chr(i)
    else:
        pass
a, b = img.size
r, g, b = pixels[a-4, b-1]
color = (r, g, b)
for i in color:
    if i != 0:
        extension += chr(i)
    else:
        pass


file_bytes = bytes(int(b, 2) for b in file_bites)

with open(f"recovered.{extension}", 'wb') as file:
    file.write(file_bytes)

print("The file is saved in the directory where the program is running")