import os   # Used to loop through files
import sys  # To be used for the passing of arguments from command line
from PIL import Image

# Check if arguments are passed from command line
if len(sys.argv) < 2:
    print("No arguments passed!\n"
          "Script usage: python texture-indexing.py <path to texture folder>")
    quit()

# Define passed argument
texture_dir = sys.argv[1] # Path to textures

# Create texture color index file
index_file = open("texture_index.txt", "x")

# Function that returns the average color of a picture
def get_avg_color(picture_file):
    picture = Image.open(picture_file) # Opens and identifies the given picture file
    picture_width  = picture.size[0]
    picture_height = picture.size[1]
    pixel = picture.load()  # Sets "pixel" to be equal to the pixel informationn from picture
    red_total = 0   # Total red color channel value
    blue_total = 0  # Total red color channel value
    green_total = 0 # Total red color channel value
    
    # Loop through all pixels in picture
    for pixel_row in range(picture_height):
        for pixel_column in range(picture_width):
            red_total = red_total + pixel[pixel_column, pixel_row][0]  # Add red channel value to total
            blue_total = blue_total + pixel[pixel_column, pixel_row][2] # Add blue channel value to total
            green_total = green_total + pixel[pixel_column, pixel_row][1] # Add green channel value to total  
    
    # Divides each total channel value by amount of pixels in picture
    red_average = round(red_total / (picture_height * picture_width)) 
    blue_average = round(blue_total / (picture_height * picture_width))
    green_average = round(green_total / (picture_height * picture_width))

    # Return RGB tuple
    return (red_average, green_average, blue_average)

# Loop through textures and append to texture color index
for texture_name in os.listdir(texture_dir):
    texture_path = str(texture_dir) + str(texture_name)
    texture_color = get_avg_color(texture_path)
    
    index_file.write(texture_path)
    index_file.write(" ")
    index_file.write(str(texture_color[0]))  # Red
    index_file.write(" ")
    index_file.write(str(texture_color[1]))  # Green
    index_file.write(" ")
    index_file.write(str(texture_color[2]))  # Blue
    index_file.write("\n")