import streamlit as st
import pandas as pd
import sqlite3
import os

st.set_page_config(page_title="Mistério SQL: A Alavancagem Fantasma", page_icon="🕵️", layout="wide")

# Nome do único arquivo Excel que deve estar na mesma pasta
ARQUIVO_EXCEL = 'Modelo_Logico_Dados_Ficticios.xlsx'

# Função para carregar as abas do Excel para o banco de dados SQLite em memória
@st.cache_resource
def carregar_base_dados():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    
    # Mapeamento do nome da tabela SQL para o nome exato da aba (Sheet) dentro do Excel
    abas_do_excel = {
        'Ativo': 'Ativo',
        'Ação': 'Ação',
        'Cliente': 'Cliente',
        'Carteira_Cliente': 'Carteira Cliente',
        'Compromisso_Cliente': 'Compromisso Cliente'
    }
    
    if not os.path.exists(ARQUIVO_EXCEL):
        st.error(f"Erro: O arquivo '{ARQUIVO_EXCEL}' não foi encontrado na mesma pasta do app.py.")
        return None
        
    try:
        # Carregar cada aba do único arquivo Excel e transformar em tabela SQL
        for nome_tabela, nome_aba in abas_do_excel.items():
            df = pd.read_excel(ARQUIVO_EXCEL, sheet_name=nome_aba)
            df.to_sql(nome_tabela, conn, index=False, if_exists='replace')
            
        return conn
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}. Verifique se os nomes das abas estão corretos.")
        return None

conn = carregar_base_dados()

# Interface do Usuário
st.title("🕵️ Mistério SQL: A Alavancagem Fantasma")

st.markdown("""
### O Caso
A área de Risco e Compliance do nosso Multi-Family Office detectou um rombo potencial grave. Um cliente misterioso conseguiu se superalavancar, acumulando 'Compromissos em Aberto' gigantescos, enquanto escondia sua verdadeira exposição em ações de altíssimo risco operando por uma plataforma específica.

O diretor de risco foi de férias subitamente e deixou apenas um bloco com anotações confusas. Você, como analista de dados, tem acesso ao banco de dados relacional (gerado a partir do nosso arquivo Excel). Sua missão é cruzar os dados para descobrir **quem é o cliente infrator** e **qual o valor exato do seu maior compromisso alavancado**.
""")

with st.expander("📝 Ver o Bloco de Anotações do Diretor (Pistas)"):
    st.markdown("""
    * **Pista 1 (O Ativo Tóxico):** A fraude começou com uma ação ordinária do setor de 'Tecnologia'. Precisamos descobrir qual é o *ID* desse ativo (Tabelas: `Ativo` e `Ação`).
    * **Pista 2 (O Rastro):** O infrator estava segurando esse ativo (descoberto na Pista 1) na sua carteira no fechamento de março (2025-03-31). Mas ele tentou despistar operando via plataforma 'BTG'. Quem é o *IDCliente*? (Tabela: `Carteira_Cliente`).
    * **Pista 3 (O Crime):** Para a denúncia avançar, precisamos do **Nome do Cliente** e provar a alavancagem: qual era o **Valor Compromissado** dele referente ao ativo 'Cota FIA Alpha' (IDAtivo = 6) no mês de janeiro (2025-01-31)? (Tabelas: `Cliente` e `Compromisso_Cliente`).
    """)

with st.expander("🗂️ Ver o Esquema do Banco de Dados (Tabelas Criadas a partir das Sheets)"):
    st.markdown("""
    * **Ativo** *(Aba 'Ativo')*: IDAtivo, Setor, Descrição, Tipo, CNPJEmissor, DEN_SOC_EM, ISIN
    * **Ação** *(Aba 'Ação')*: TickerAção, ClassificaçãoAção, IDAtivo
    * **Cliente** *(Aba 'Cliente')*: IDCliente, NomeCliente, CodigoCliente, DocumentoCliente
    * **Carteira_Cliente** *(Aba 'Carteira Cliente')*: DataCarteiraCliente, IDCliente, IDAtivo, VlrCartCliente, Gestora, QtdCartCliente, Plataforma
    * **Compromisso_Cliente** *(Aba 'Compromisso Cliente')*: DataCompromisso, IDCliente, IDAtivo, ValorCompromissado
    """)

st.divider()
st.subheader("💻 Terminal SQL")
st.write("Escreva sua query abaixo para investigar o banco de dados:")

query = st.text_area("Query SQL:", height=150, value="SELECT * FROM Ativo LIMIT 5;")

if st.button("Executar Query"):
    if conn:
        try:
            # Executar a query do usuário
            resultado = pd.read_sql_query(query, conn)
            st.success("Query executada com sucesso!")
            st.dataframe(resultado, use_container_width=True)
        except Exception as e:
            st.error(f"Erro na sintaxe SQL: {e}")

# =====================================================================
# NOVA SEÇÃO: VERIFICAÇÃO DE RESPOSTA (O JOGADOR VALIDA SE ACERTOU)
# =====================================================================
st.divider()
st.subheader("🎯 Relatório Final: Resolveu o Mistério?")
st.write("Acha que já descobriu toda a verdade? Preencha os dados abaixo para enviar sua denúncia formal para a diretoria.")

col1, col2 = st.columns(2)

with col1:
    resposta_nome = st.text_input("Nome Completo do Cliente Infrator:")

with col2:
    # Passo o step=0.01 para permitir a digitação dos centavos corretamente
    resposta_valor = st.number_input("Valor Compromissado da Fraude (R$):", min_value=0.0, format="%.2f", step=0.01)

if st.button("Submeter Denúncia"):
    # Limpa espaços em branco e ignora letras maiúsculas/minúsculas para facilitar o acerto do jogador
    nome_jogador = resposta_nome.strip().lower()
    
    # O Gabarito da sua base de dados
    GABARITO_NOME = "joão silva"
    # Convertendo o acento para garantir que "joao silva" ou "joão silva" funcionem
    nomes_aceitos = ["joão silva", "joao silva"] 
    GABARITO_VALOR = 163310.01

    if nome_jogador == "" or resposta_valor == 0.0:
        st.warning("⚠️ Preencha os dois campos antes de enviar a denúncia.")
    elif nome_jogador in nomes_aceitos and resposta_valor == GABARITO_VALOR:
        st.balloons()
        st.success("🎉 **CASO ENCERRADO COM SUCESSO!** A diretoria aprovou seu relatório. Você descobriu que **João Silva** estava se escondendo através da plataforma BTG e comprovou sua alavancagem ilegal de **R$ 163.310,01**. Parabéns, excelente trabalho de auditoria!")
    else:
        st.error("❌ **DENÚNCIA REJEITADA!** Os dados não batem. A diretoria da CVM não encontrou as provas suficientes para esse suspeito ou valor. Volte ao Terminal SQL e cruze os dados com mais atenção!")