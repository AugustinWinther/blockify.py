# STD lib imports
from sys import argv as cli_args
from os import path
import time

# 3D pary imports
from PIL import Image

def check_input():
    # Set default values
    width = 128
    height = 0
    texture_list = "./block.list/ideal.txt"

    if len(cli_args) < 2:
        print("Too few arguments!\n"
            "Script usage: python blockify.py " 
            "<input image> <width> <height> <texture list>\n"
            "or just: "
            "python blockify.py <input image>")
        quit()
    elif len(cli_args) > 1:
        image = cli_args[1]
        if len(cli_args) > 2:
            width = cli_args[2]
            if len(cli_args) > 3:
                height = cli_args[3]
                if len(cli_args) > 4:
                    texture_list = cli_args[4]

    # Check input image for errors
    if (path.exists(image) == True):
        if ((image.endswith(".png") == False) and 
            (image.endswith(".jpg") == False) and 
            (image.endswith(".bmp") == False) and
            (image.endswith(".jpeg") == False)):
            print("Input picture not supported!\n"
                "Please use PNG, BMP, JPG or JPEG")
            quit()
    else:
        print("Image '%s' does not exist!" % image)
        quit()

    # Check block width and block height for errors
    try:
        width = int(width)
        height = int(height)
    except:
        print("Width and height needs to be integers!")
        quit()

    if (width == 0 and (height < 2 and height != 0)):
        print("Block height invalid!\n"
              "Please use a block height greater than 1")
        quit()
    elif (height == 0 and (width < 2 and width != 0)):
        print("Block width invalid!\n"
              "Please use a block width greater than 1")
        quit()
    elif ((width != 0) and (height != 0)):
        if ((width < 2) or (height < 2)):
            print("Block height or width invalid!\n"
                  "Please use sizes greater than 1")
            quit()

    # Check texture_list for errors
    if (path.exists(texture_list) == False):
        print("Texture list '%s' does not exist!" % texture_list)
        quit()

    check_input.image = image
    check_input.width = width
    check_input.height = height
    check_input.texture_list = texture_list

def file_to_list(list_file):
    list = []

    with open(list_file) as file:
        for line in file: 
            text = line.split(" ")
            texture = text[0]
            color = (int(text[1]),int(text[2]),int(text[3]))  # (R,G,B)
            list.append([texture, color])
    return list

def resize_image(input_image, width, height):
    # Keep image size if width and heigth == 0
    if (width == 0 and height == 0):
        with Image.open(input_image) as image:
            # Don't know how to convert PIL.<TILETYPE>Plugin.<TILETYPE>File
            # to PIL.Image.Image, so i just resize the image to the same
            # size, thus keeping the image at the same size. :P
            resized_image = image.resize((image.size[0], image.size[1]))
    else:
        with Image.open(input_image) as image:
            if (width == 0 and height != 0):
                width = round(image.size[0] * (height / image.size[1]))
            elif (height == 0 and width != 0):
                height = round(image.size[1] * (width / image.size[0]))
            
            resized_image = image.resize((width, height))
        
    resized_width = (resized_image.size[0])
    resized_height = (resized_image.size[1])

    output_image = Image.new('RGB', ((resized_width*16), (resized_height*16)))
    
    resize_image.output_image = output_image
    resize_image.resized_image = resized_image

def pixel_to_texture(pixel_info, pixel_x, pixel_y, list):
    min_rgb_diff = 1000
    texture = False
    pixel_rgb = pixel_info[pixel_x, pixel_y]

    for index in list: 
        color_rgb = index[1]
        rgb_diff = (abs(pixel_rgb[0] - color_rgb[0])
                    + abs(pixel_rgb[1] - color_rgb[1])
                    + abs(pixel_rgb[2] - color_rgb[2]))
        if rgb_diff < min_rgb_diff:
            min_rgb_diff = rgb_diff
            texture = index[0]
    return texture

def convert_pixels(pixel_info, pixel_x, pixel_y, length, list, output_image):
    texture_file = pixel_to_texture(pixel_info, pixel_x, pixel_y, list)
    for i in range(length):
        with Image.open(texture_file) as texture:
            output_image.paste(texture,((pixel_x*16),((pixel_y+i)*16)))
 
def convert_image(input_image, output_image, texture_list, input_image_name):
    # Set "pixel" to be equal to the pixel information from image
    pixel_info = input_image.load()

    # Define default values to be used in converting algorithm
    pixel_x = 0
    pixel_y = 0
    start_pixel_x = 0
    start_pixel_y = 0
    max_x = input_image.size[0] - 1
    max_y = input_image.size[1] - 1
    pixel_count = max_x * max_y
    pixel_repeat = 1
    pixel_conv = 0  # Amount of pixels converted
    pixel_conv_time = 0
    time_since_last_conv = time.time()
    eta_string = ""
    last_eta_print = time.time()
    last_percent = -1

    #Time exec.
    start_time = time.time()
    print("\n Converting: %s" % input_image_name)

    # START OF CONVERTING
    while pixel_x <= max_x:
        
        # Calculate time used to convert 100 pixels
        if (pixel_conv % 100 == 0):
            pixel_conv_time = time.time() - time_since_last_conv
            time_since_last_conv = time.time() 
    
        # Create and print progress bar and ETA
        if (time.time() - last_eta_print >= 2):
            eta = pixel_conv_time*((pixel_count - pixel_conv)/100)
            eta_sec = eta % 60
            eta_min = eta / 60
            eta_string = " ETA: %dm %ds "  % (eta_min, eta_sec)
            last_eta_print = time.time()
        percent = round((pixel_x / max_x) * 100)
        if (percent > last_percent):
            last_percent = percent
            percent_left = 100 - percent
            progress_bar = ((round(percent / 2) * '█' ) 
                        + (round(percent_left / 2) * '-'))
            print(" Progress:", progress_bar, percent, "%", 
                eta_string , end="\r")


        this_pixel = pixel_info[pixel_x, pixel_y]
        start_pixel = pixel_info[start_pixel_x, start_pixel_y]

        # If pixel is last in column
        if (pixel_y == max_y):
            next_pixel = this_pixel
        else:
            next_pixel = pixel_info[pixel_x, pixel_y + 1]

        # Get color difference
        rgb_diff = (abs(start_pixel[0] - next_pixel[0])
                    + abs(start_pixel[1] - next_pixel[1])
                    + abs(start_pixel[2] - next_pixel[2]))

        # Convert pixels
        if (pixel_y < max_y):
            if (rgb_diff > 6):
                convert_pixels(pixel_info, start_pixel_x, start_pixel_y, 
                               pixel_repeat, texture_list, output_image)
                pixel_y += 1
                start_pixel_x, start_pixel_y = pixel_x, pixel_y
                pixel_repeat = 1
            else:
                pixel_repeat += 1
                pixel_y += 1
        else:
            if (rgb_diff > 6):
                convert_pixels(pixel_info, start_pixel_x, start_pixel_y, 
                               pixel_repeat, texture_list, output_image)
            else:
                pixel_repeat += 1
                convert_pixels(pixel_info, start_pixel_x, start_pixel_y, 
                               pixel_repeat, texture_list, output_image)
            pixel_y = 0
            pixel_x += 1
            start_pixel_x, start_pixel_y = pixel_x, pixel_y
            pixel_repeat = 1
        pixel_conv += 1
    # END OF CONVERTING

    # Caluclate and print time passed
    time_passed = (time.time() - start_time)
    sec_passed = time_passed % 60
    min_passed = time_passed / 60
    print("\n Finished in: %dm %ds" % (min_passed, sec_passed))

    convert_image.converted_image = output_image

def save_image(out_image, input_image_name):
    # Save converted image
    output_name = (input_image_name.split("."))[0] + "-mc.png"
    print(" Saving to: %s" % output_name)
    out_image.save(output_name)

def main():
    # Error check input and get values
    check_input()
    input_image = check_input.image
    block_width = check_input.width
    block_height = check_input.height
    texture_list = file_to_list(check_input.texture_list)

    # Resize input image to output image size
    resize_image(input_image, block_width, block_height)
    resized_image = resize_image.resized_image
    output_image = resize_image.output_image

    # Convert image to minecraft pixel art
    convert_image(resized_image, output_image, texture_list, input_image)
    converted_image = convert_image.converted_image

    #Save converted image
    save_image(converted_image, input_image)

if __name__ == "__main__":
    main()
