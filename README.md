# 🕵️ Mistério SQL: A Alavancagem Fantasma

Um jogo interativo de investigação de dados baseado no modelo de banco de dados real do nosso grupo. Desenvolvido em Python e Streamlit, o sistema lê diretamente as abas de uma planilha Excel e simula um ambiente de consultas SQL (JOINs, filtros, cruzamento de chaves) voltado para cenários de auditoria e *Compliance* no mercado financeiro.

<img width="1307" height="554" alt="image" src="https://github.com/user-attachments/assets/1e2e4fd3-ee18-444f-a102-d8906801285a" />

## 📖 A História

A área de Risco e Compliance detectou um rombo potencial grave. Um cliente misterioso conseguiu se superalavancar, acumulando 'Compromissos em Aberto' gigantescos, enquanto escondia sua verdadeira exposição operando através de uma corretora específica. Sua missão, como auditor de dados, é explorar as tabelas usando linguagem SQL para cruzar os rastros e descobrir a identidade do infrator.

---

## 🚀 Como Executar Localmente

Para rodar este Mistério SQL na sua própria máquina, você precisará apenas ter o **Python** instalado. O processo leva menos de dois minutos.

### Passo a Passo

**1. Reúna os arquivos**
Faça o download dos arquivos do projeto e coloque-os todos dentro de uma mesma pasta no seu computador.

**2. Abra o Terminal**
Abra o terminal (Prompt de Comando, PowerShell ou o terminal embutido no VS Code) e navegue até a pasta que você acabou de criar.

**3. Instale as bibliotecas necessárias**
A aplicação utiliza o **Streamlit** para gerar a interface web, o **Pandas** e o **OpenPyXL** para ler as abas do Excel. Para instalar tudo de uma vez, execute o comando abaixo:
```bash
pip install streamlit pandas openpyxl
