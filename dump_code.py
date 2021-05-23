
# Leitura dos dados
cursos = pd.read_excel("bd.xlsx")
col = cursos.columns
col = list(col[0:16])+['STATUS']
cursos = cursos.loc[:, col]

# Seleção de campos que podem ser consultados
col = cursos.columns
col = ['CURSO',  'DIRETORIA',  'UNIDADE REGIONAL',  'CARGO DE CONFIANÇA',  'INSTITUIÇÃO DE ENSINO',  'ANO DE OBTENÇÃO DO TÍTULO',  'DEMANDA', 'STATUS']


# Filtro para consulta
filtros = ['TODOS'] + col

# Usuário que está consultando
usuarios = pd.read_excel("usuarios.xlsx")

login = st.text_input('Nome de usuário', '')
senha = st.text_input('Senha', '')

ul = list(usuarios['login'])
sl = list(usuarios['senha'])
sl = [str(n) for n in sl]

b = True

if b:
    if True: #(login in ul) and (senha in sl):

        opt = st.selectbox('Escolha', col)

        f = st.selectbox('Filtro', filtros)
        if f != 'TODOS':
            selecionado = cursos[f].unique()
            sel = st.multiselect('Quais',selecionado)

            indopt = np.array([False]*cursos.shape[0])
            for s in sel:
                cond = cursos.loc[:,f] == s
                indopt = np.logical_or(indopt,cond)

            cursos = cursos.loc[indopt,:]

    # Busca por assunto
        assunto = st.text_input('Busca assunto', '')
        titulos = list(cursos['TÍTULO'])
        if len(assunto) > 3:
            assunto = assunto.split()
            ind = []
            for a in assunto:
                for i, t in enumerate(titulos):
                    if a.lower() in str(t).lower():
                        ind += [i]

            titulos = np.array(titulos)
            titulos = titulos[ind]

            cursos = cursos.iloc[ind, :]

    # Resultados
        d = cursos[opt].value_counts()
        st.bar_chart(d)