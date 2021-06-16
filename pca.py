import streamlit as st
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

st.title("""Principal component analysis""")
st.subheader("File input")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    is_excel = uploaded_file.name[-4:] == 'xlsx' or uploaded_file.name[-3:] == 'xls'
    if not is_excel:
        dec = st.checkbox('Comma as decimal place separator?',value = False)
        delim = st.selectbox('Column delimiter:',[',',';','Tab','Space'])

        if delim == 'Tab:':
            delim = '\r'
        elif delim == 'Space':
            delim = ' '

        if dec:
            decimal = ','
        else:
            decimal = '.'

    header = st.checkbox('Is first line header?',value = True)
    
    if header:
        if is_excel:
            dataframe = pd.read_excel(uploaded_file)
        else: 
            dataframe = pd.read_csv(uploaded_file,decimal=decimal,delimiter=delim)
    else:
        if is_excel:
            dataframe = pd.read_excel(uploaded_file,header=None)
        else:
            dataframe = pd.read_csv(uploaded_file,decimal=decimal,delimiter=delim,header=None)

    st.write(dataframe)
    
    sel = st.multiselect("Select columns for the graph",dataframe.columns)
    if len(sel)>1:
        data = dataframe.loc[:,sel]

        X = data.values
        pca = PCA(n_components = 2)
        pc = pca.fit_transform(X)
        pcvars = pca.explained_variance_ratio_[:2]
        fig = plt.figure() 
        plt.plot(pc[:,0],pc[:,1],'o')

        lp = st.checkbox('Label points?')

        if lp:
            sel_label = st.selectbox("Select labels for the points",dataframe.columns)
            labels = dataframe[sel_label]
            for i in range(pc.shape[0]):

                x = pc[i,0]
                y = pc[i,1]

                label = str(labels[i])

                plt.annotate(label, # this is the text
                    (x,y), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0,3), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center        
 
        plt.xlabel(f'PC1 ({100*pcvars[0]:.3f}%)')        
        plt.ylabel(f'PC2 ({100*pcvars[1]:.3f}%)')
        plt.title('PCA')
        st.pyplot(fig)
