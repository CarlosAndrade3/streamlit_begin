import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# st.write('Hello!')
st.title('Dashboard de EDA!')
st.sidebar.title('Menu')

arquivo = st.sidebar.file_uploader(
    label='Selecione o arquivo do DataFrame em csv ou Excel',
    type = ['csv','xlsx']
)

# df_heart = pd.read_csv('./data/heart.csv')

if arquivo is not None:
    print(arquivo)

    try:
        df = pd.read_csv(arquivo)

    except:
        df = pd.read_excel(arquivo)

    if df is not None:
        numeric_columns = df.select_dtypes(['float','int']).columns

        checkbox = st.sidebar.checkbox('Mostrar DataFrame')
        if  checkbox:
            st.subheader('DataFrame')
            st.dataframe(df)

        corr = st.sidebar.checkbox('Mostrar Heatmap')
        if  corr:
            st.subheader('Heatmap de correlação entre as variáveis')
            fig, ax = plt.subplots()
            sns.heatmap(df.corr())
            st.pyplot(fig) 


        comparativo = st.sidebar.checkbox('Mostrar gráfico comparativo')

        if  comparativo:

            st.sidebar.subheader('Configuracões do gráfico')
            biblioteca = st.sidebar.selectbox(
                label='Selecione a biblioteca',
                options=[None,'matplotlib','Seaborn','Plotly']
            )

            tipo_grafico = st.sidebar.selectbox(
                    label='Selecione o tipo de gráfico',
                    options=[None,'Scatterplot','Lineplot','Boxplot']
                )

            if tipo_grafico == 'Boxplot':
                xaxis=st.sidebar.selectbox('Selecione a variável', options=numeric_columns)
            else:
                xaxis=st.sidebar.selectbox('Selecione a variável do eixo x', options=numeric_columns)
                yaxis=st.sidebar.selectbox('Selecione a variável do eixo y', options=numeric_columns)


            if biblioteca == 'matplotlib':

                if tipo_grafico == 'Scatterplot':
                    st.subheader('Gráfico de dispersão (scatterplot)') 
                    
                    fig, ax = plt.subplots()
                    plt.scatter(data=df,x= xaxis, y= yaxis)
                    st.pyplot(fig)

                if tipo_grafico == 'Lineplot':
                    st.subheader('Gráfico de linha (lineplot)') 
        
                    fig, ax = plt.subplots()
                    plt.plot(df[xaxis], df[yaxis])
                    st.pyplot(fig)

                if tipo_grafico == 'Boxplot':
                    st.subheader('Gráfico de quartil (boxplot)') 
                
                    fig, ax = plt.subplots()
                    plt.boxplot(df[xaxis])
                    st.pyplot(fig)


            elif biblioteca == 'Seaborn':

                if tipo_grafico == 'Scatterplot':
                    st.subheader('Gráfico de dispersão (scatterplot)') 
                    
                    fig, ax = plt.subplots()
                    sns.scatterplot(x= df[xaxis], y= df[yaxis])
                    st.pyplot(fig)

                if tipo_grafico == 'Lineplot':
                    st.subheader('Gráfico de linha (lineplot)') 
        
                    fig, ax = plt.subplots()
                    sns.lineplot(x=df[xaxis], y= df[yaxis])
                    st.pyplot(fig)

                if tipo_grafico == 'Boxplot':
                    st.subheader('Gráfico de quartil (boxplot)') 
                
                    fig, ax = plt.subplots()
                    sns.boxplot(data=df, x=df[xaxis])
                    st.pyplot(fig)
                    

            elif biblioteca == 'Plotly':
                if tipo_grafico == 'Scatterplot':
                    st.subheader('Gráfico de dispersão (scatterplot)') 
                    
                    plot = px.scatter(data_frame = df, x = xaxis, y = yaxis)
                    st.plotly_chart(plot)

                if tipo_grafico == 'Lineplot':
                    st.subheader('Gráfico de linha (lineplot)') 
        
                    plot = px.line(x = df[xaxis], y = df[yaxis])
                    st.plotly_chart(plot)

                if tipo_grafico == 'Boxplot':
                    st.subheader('Gráfico de quartil (boxplot)') 
                
                    plot = px.box(data_frame = df, x = xaxis)
                    st.plotly_chart(plot)

 