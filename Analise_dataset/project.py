import streamlit as st
import cv2 as cv
from PIL import Image
import numpy as np
from scipy.interpolate import UnivariateSpline


def LookupTable(x, y):
    spline = UnivariateSpline(x, y)
    return spline(range(256))

def load_file():
    uploaded_file = st.file_uploader('Carregue uma imagem')

    if uploaded_file is not None:

        img = Image.open(uploaded_file)
    
        img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
        return img
    
    
def adjust_bright_and_contrast(input_img, brightness = 0, contrast = 0):
    buf_img = input_img.copy()
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_bright = (highlight - shadow)/255
        gamma_bright = shadow
        
        buf_img = cv.addWeighted(buf_img, alpha_bright, buf_img, 0, gamma_bright)

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_contrast = f
        gamma_contrast = 127*(1-f)
        
        buf_img = cv.addWeighted(buf_img, alpha_contrast, buf_img, 0, gamma_contrast)

    return buf_img

def greyscale(img):
    greyscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    return greyscale

def sharpen(img):
    kernel = np.array([
                [-1, -1, -1],
                [-1, 9.5, -1],
                [-1, -1, -1]])
    img_sharpen = cv.filter2D(img, -1, kernel)
    return img_sharpen

def sepia(img):
    img_sepia = np.array(img, dtype=np.float64) # converting to float to prevent loss
    sepia_kernel = np.matrix([
        [0.272, 0.534, 0.131],
        [0.349, 0.686, 0.168],
        [0.393, 0.769, 0.189]])
    img_sepia = cv.transform(img_sepia, sepia_kernel) # multipying image with special sepia matrix
    img_sepia[np.where(img_sepia > 255)] = 255 # normalizing values greater than 255 to 255
    img_sepia = np.array(img_sepia, dtype=np.uint8)
    return img_sepia

def pencil_sketch_grey(img):
    # Utilizando a função do openCV para criar um efeito de rascunho em cinza e colorido
    sk_gray, sk_color = cv.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
    return  sk_gray

def pencil_sketch_col(img):
    # Utilizando a função do openCV para criar um efeito de rascunho em cinza e colorido
    sk_gray, sk_color = cv.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
    return  sk_color


def HDR(img):
    # Utilizando o openCV para aumentar os detalhes da imagem
    hdr = cv.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    return  hdr

def invert(img):
    inv = cv.bitwise_not(img)
    return inv
st.title('Streamlit Example')

def summer(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel  = cv.split(img)
    red_channel = cv.LUT(red_channel, increaseLookupTable).astype(np.uint8)
    blue_channel = cv.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
    summer = cv.merge((blue_channel, green_channel, red_channel ))
    return summer

def winter(img):
    increaseLookupTable = LookupTable([0, 64, 128, 256], [0, 80, 160, 256])
    decreaseLookupTable = LookupTable([0, 64, 128, 256], [0, 50, 100, 256])
    blue_channel, green_channel,red_channel = cv.split(img)
    red_channel = cv.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
    blue_channel = cv.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
    win = cv.merge((blue_channel, green_channel, red_channel))
    return win

uploaded = load_file()

contrast = st.slider('Contrast', -200, +200,0)
bright = st.slider('bright', -200, +200,0)
width = st.slider('Image width', 100, 1000, 200)

st.header('Original image')
original_image = cv.cvtColor(uploaded, cv.COLOR_BGR2RGB)

multiselect = st.multiselect('Selecione os filtros',
    ['greyscale',
     'sharpen',
     'sepia',
     "pencil sketch grayscale",
     "pencil sketch",
     "HDR",
     "invert",
     "summer",
     'winter'
])
st.write(multiselect)

filter_switcher = {
    'greyscale': greyscale,
    "sharpen": sharpen,
    'sepia': sepia,
    'pencil sketch grayscale': pencil_sketch_grey,
    'pencil sketch': pencil_sketch_col,
    'HDR': HDR,
    'invert': invert,
    'summer': summer,
    'winter': winter    
}

adjusted_image = adjust_bright_and_contrast(uploaded, bright, contrast)

for img_filter in multiselect:
    adjusted_image = filter_switcher[img_filter](adjusted_image)
adjusted_image_rgb = cv.cvtColor(adjusted_image, cv.COLOR_BGR2RGB)

st.image([original_image, adjusted_image_rgb], width=width, caption=["original", 'modified'])