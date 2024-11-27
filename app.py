import streamlit as st
import pandas as pd

# Função para gerar combinações válidas
def gerar_combinacoes(jogos):
    colunas = list(jogos.columns)
    combinacoes_validas = []

    # Número de linhas
    n = len(jogos)

    # Criar combinações linha a linha
    for i in range(n):
        celula1 = (f'{colunas[0]}{i+1}', jogos[colunas[0]][i])  # Ex.: ('Jogos1-1', 'Flamengo')
        celula2 = (f'{colunas[1]}{i+1}', jogos[colunas[1]][i])  # Ex.: ('Jogos2-1', 'Empate')
        combinacoes_validas.append([celula1, celula2])  # Adiciona a linha como uma combinação válida

    # Gerar todas as combinações possíveis com uma única escolha por linha
    def gerar_recursivamente(indice, atual):
        if indice == n:  # Base da recursão: todas as linhas foram processadas
            resultado = atual[:]
            combinacoes_finais.append(resultado)
            return

        # Escolha do primeiro elemento da linha
        gerar_recursivamente(indice + 1, atual + [combinacoes_validas[indice][0]])

        # Escolha do segundo elemento da linha
        gerar_recursivamente(indice + 1, atual + [combinacoes_validas[indice][1]])

    # Lista para armazenar as combinações finais
    combinacoes_finais = []
    gerar_recursivamente(0, [])

    return combinacoes_finais

# Função para gerar as entradas da planilha
def criar_elementos(n, jogos1, jogos2):
    return pd.DataFrame({'Jogos1': jogos1, 'Jogos2': jogos2})

# Webapp usando Streamlit
st.title('Simulador de Jogos Esportivos')

# Entradas do Usuário
st.header('Defina os Jogos')

n = st.number_input('Número de jogos', min_value=1, step=1, value=3)

col1, col2 = st.columns(2)

with col1:
    jogos1 = [st.text_input(f'Jogo 1 - {i+1}', f'Jogo 1 - {i+1}') for i in range(n)]

with col2:
    jogos2 = [st.text_input(f'Jogo 2 - {i+1}', f'Jogo 2 - {i+1}') for i in range(n)]

# Gerar dataframe com os jogos
jogos = criar_elementos(n, jogos1, jogos2)

# Botão para gerar combinações
if st.button('Apostas'):
    combinacoes = gerar_combinacoes(jogos)

    # Alternar entre modo compacto e modo de rolagem
    modo_compacto = st.checkbox('Modo Compacto (Tabelas Lado a Lado)', value=True)

    if modo_compacto:
        # Exibir tabelas lado a lado
        st.header('Combinações Geradas (Modo Compacto)')
        colunas_por_linha = 3  # Quantas tabelas por linha
        linhas = [combinacoes[i:i + colunas_por_linha] for i in range(0, len(combinacoes), colunas_por_linha)]

        for linha in linhas:
            cols = st.columns(len(linha))
            for col, comb in zip(cols, linha):
                df = pd.DataFrame(comb, columns=['Célula', 'Apostas'])
                col.table(df['Apostas'])
    else:
        # Exibir tabelas no modo de rolagem
        st.header('Combinações Geradas (Modo de Rolagem)')
        for idx, comb in enumerate(combinacoes, start=1):
            st.subheader(f'Combinação {idx}')
            df = pd.DataFrame(comb, columns=['Célula', 'Apostas'])
            st.table(df['Apostas'])
