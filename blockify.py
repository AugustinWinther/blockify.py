from sys import argv as arguments
from PIL import Image

# Check if enough arguments are passed
if len(arguments) < 2:
    print("Too few arguments!\n"
          "Script usage: python blockify.py " 
          "<input image> <width> <height> <texture list>\n"
          "or just: "
          "python blockify.py <input image>")
    quit()
elif len(arguments) == 2:
    input_image = arguments[1]
    block_width = 128
    block_height = 0
    texture_list = "./block.list/all.txt"
elif len(arguments) > 4:
    input_image = arguments[1]
    block_width = int(arguments[2])
    block_height = int(arguments[3])
    texture_list = arguments[4]
    
keep_ratio = "no"

# Check passed arguments for errors
if ((input_image.endswith(".png") == False) and 
    (input_image.endswith(".jpg") == False) and 
    (input_image.endswith(".bmp") == False) and
    (input_image.endswith(".jpeg") == False)):
    print("Input picture not supported!\n"
          "Please use PNG, BMP, JPG or JPEG")
    quit()
elif ((block_width == 0) and (block_height == 0)):
    print("Height and width can't both be 0!\n")
    quit()
elif (block_width == 0):
    if ((block_height > 512) or (block_height < 16)):
        print("Block height invalid!\n"
              "Please use a block height between 16 and 512")
        quit()
    keep_ratio = "width"
elif (block_height == 0):
    if ((block_width > 512) or (block_width < 16)):
        print("Block width invalid!\n"
              "Please use a block width between 16 and 512")
        quit()
    keep_ratio = "height"
elif (keep_ratio == "no"):
    if ((block_width > 512) or (block_width < 16)):
        print("Block width invalid!\n"
                "Please use a block width between 16 and 512")
        quit()
    elif ((block_height > 512) or (block_height < 16)):
        print("Block width invalid!\n"
                "Please use a block width between 16 and 512")
        quit()

# 2D list containing contents from texture_list.
# Item example: ['path/texture.png', (255, 255, 255)]
index_list = []

# Adds lines from texture_list to index_list.
# Line example: path/texture.png 255 255 255
with open(texture_list) as file:
    for line in file: 
        text = line.split(" ")
        texture = text[0]
        color = (int(text[1]),int(text[2]),int(text[3]))  # (R,G,B)
        index_list.append([texture, color])

# Resizes input_image to pixel_art_res
with Image.open(input_image) as image:
    if (keep_ratio == "width"):
        block_width = round(image.size[0] * (block_height / image.size[1]))
    elif (keep_ratio == "height"):
        block_height = round(image.size[1] * (block_width / image.size[0]))
    image = image.resize((block_width, block_height))
    image_width, image_height = (image.size[0]), (image.size[1])

# Create an empty image which will be used as final output image.  
# This image will be a mosaic of textures from index_list.  
# Times width and height by 16px (texture resolution).  
final_image = Image.new('RGB', ((image_width*16), (image_height*16)))

# Find best matching texture for pixel color
def pixel_to_texture(pixel_x, pixel_y):
    min_rgb_diff = 1000
    texture = False
    pixel_rgb = pixel[pixel_x, pixel_y]

    for index in index_list: 
        color_rgb = index[1]
        rgb_diff = (abs(pixel_rgb[0] - color_rgb[0]) + 
                    abs(pixel_rgb[1] - color_rgb[1]) + 
                    abs(pixel_rgb[2] - color_rgb[2]))
        if rgb_diff < min_rgb_diff:
            min_rgb_diff = rgb_diff
            texture = index[0]
    return texture

# Replaces pixels based on start pixel coordinate(pixel_x, pixel_y).
# and how many times that pixel repeats itself (length).
# NOTE: Replaces pixels from top to bottom (y-top to y-bottom)
# NOTE: Times x and y with 16px (texture resolution)
def replace_pixels(pixel_x, pixel_y, length):
    texture_file = pixel_to_texture(pixel_x, pixel_y)
    for i in range(length):
        with Image.open(texture_file) as texture:
            final_image.paste(texture,((pixel_x*16),((pixel_y+i)*16)))
 
# Set "pixel" to be equal to the pixel information from image
pixel = image.load()

# Go through every pixel in image, and replace pixels with textures
pixel_x = pixel_y = 0
start_pixel_x = start_pixel_y = 0
max_x, max_y = (image_width - 1), (image_height - 1)
pixel_repeat = 1

while pixel_x <= max_x:
   
    # Prints progress bar
    percent = round((pixel_x / max_x) * 100)
    percent_left = 100 - percent
    progress_bar = (round(percent / 2) * '█' ) + (round(percent_left / 2) * '-')
    print(" Progress:", progress_bar, percent, "%", end="\r")


    this_pixel = pixel[pixel_x, pixel_y]
    start_pixel = pixel[start_pixel_x, start_pixel_y]

    if (pixel_y == max_y):
        next_pixel = this_pixel
    else:
        next_pixel = pixel[pixel_x, pixel_y + 1]

    rgb_diff = (abs(start_pixel[0] - next_pixel[0]) + 
                abs(start_pixel[1] - next_pixel[1]) + 
                abs(start_pixel[2] - next_pixel[2]))

    if (pixel_y < max_y):
        if (rgb_diff > 6):
            replace_pixels(start_pixel_x, start_pixel_y, pixel_repeat)
            pixel_y += 1
            start_pixel_x, start_pixel_y = pixel_x, pixel_y
            pixel_repeat = 1
        else:
            pixel_repeat += 1
            pixel_y += 1
    else:
        if (rgb_diff > 6):
            replace_pixels(start_pixel_x, start_pixel_y, pixel_repeat)
            pixel_y = 0
            pixel_x += 1
            start_pixel_x, start_pixel_y = pixel_x, pixel_y
            pixel_repeat = 1
        else:
            pixel_repeat += 1
            replace_pixels(start_pixel_x, start_pixel_y, pixel_repeat)
            pixel_y = 0
            pixel_x += 1
            start_pixel_x, start_pixel_y = pixel_x, pixel_y
            pixel_repeat = 1

# Output filename is input image name + "-mc.png".
# (Input = file.jpg   =>   Output = file-mc.png)
final_image.save((input_image.split("."))[0] + "-mc.png")