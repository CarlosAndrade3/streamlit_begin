import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from PIL import Image
import matplotlib.pyplot as plt

# Escrevendo um título
st.title('Streamlit Example')

# Escrevendo um texto
st.write('Este é um texto')

## Escrevendo um texto utilizando as regras de markdown
st.write('Texto **negrito**')

## Escrevendo um cabeçalho
st.header('Este é um header')

## Escrevendo um cabeçalho
st.subheader('Este é um subheader')

## Escrevendo uma legenda
st.caption('Este é um caption')

## Escrevendo um código
st.code("""
a = 20
b = 30
print(a + b)
""")

## Escrevendo uma formúla em latex
st.latex('\sum_{i=0}^j x_i')

df = pd.DataFrame(
    {'A': [1,2,3],
     'B': ['SP', 'RJ', 'PR']}
)

## Escrevendo um dataframe
st.write(df)

st.dataframe(df)

## Escrevendo uma tabela estática
st.table(df)

base_model = np.random.random_integers(0, 10, 100)
st.write(base_model)

new_model = np.random.random_integers(100, 200, 100)
st.write(base_model)

model_df = pd.DataFrame({'baseline': base_model, 'new_model': new_model})
st.write(model_df)


st.metric(
    'Model performance', # Titulo
    new_model.mean(), # Valor principal
    new_model.mean() - base_model.mean(), # delta
    # delta_color='inverse' # cor
)


## Gráficos
st.line_chart(model_df)

st.area_chart(model_df)

st.bar_chart(model_df)

## Inputs

click = st.button('Click me')

st.write(click)

## Checkbox
select = st.checkbox('Concorda?')
st.write(select, value=False)

## Radio

radio = st.radio('Selecione uma fruta', ['maca', 'banana', 'uva'])

st.write(radio)

## Dropdown

drop = st.selectbox('Selecione uma fruta', ['maca', 'banana', 'uva'])
st.write(drop)

## Multiselect

multiselect = st.multiselect('Selecione a(s) fruta(s)', ['maca', 'banana', 'uva'])
st.write(multiselect)

## Sliders
slider = st.slider('Qual sua idade', 0, 130,20)
st.write(slider)

## text input

text = st.text_input('Qual seu nome?')
st.header(f"Olá {text}")


## Calendario
date = st.date_input('Qual sua data de nascimento?')

st.write(type(date))
st.write(f'Sua data de nascimento é: {date}')


## Carregando arquivos

uploaded_file = st.file_uploader('Carregue um arquivo')
st.write(uploaded_file)

if uploaded_file is not None:
    
    img = Image.open(uploaded_file)

st.image(img)