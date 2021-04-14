# Blockify - Written in Python
Picture to Minecraft pixel art generator written in python.

### Dependencies
- Python >= 3.9.4 - https://www.python.org/downloads/
- Pillow >= 8.2.0 - ``` pip install pillow ```

### How to use
```python blockify.py <input image> <width> <height> <texture list>``` 
- ```<input image>``` Picture you want to convert
- ```<width>``` Amount of Minecraft blocks wide
- ```<height>``` Amount of Minecraft blocks high
- ```<texture list>``` One of the texture lists from ./block.list 

(To keep the ratio of input image, specify either width or height, and let the other one be 0.)

e.g. ```python blockify.py test.jpg 256 0 all.txt ```

(If you want the block width and block height to be the same as the image dimensions, set BOTH width and height input as 0)

e.g. ```python blockify.py test.jpg 0 0 all.txt ```
