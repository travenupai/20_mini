import sys
import os
import streamlit as st
from io import BytesIO
from zipfile import ZipFile
from docx import Document

# Configuração do diretório src para importações
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

# Importação do módulo VidmarmercadoCrew
try:
    from src.vidmarmini.crew import VidmarminiCrew
except ModuleNotFoundError:
    st.error("Não foi possível importar o módulo VidmarmercadoCrew. Verifique se o caminho está correto e se o módulo existe.")

# Configuração do título da aplicação
st.title('Análise de Pesquisa de Mercado com AI Agents - CrewAI')

# Campo de entrada para a URL do site
site_url = st.text_input("Digite a URL do site para análise, incluindo o https:// ")

# Inicialize o session state para armazenar o estado da análise e arquivos gerados
if "analise_realizada" not in st.session_state:
    st.session_state.analise_realizada = False
    st.session_state.arquivos_md = []

# Função para converter conteúdo Markdown em Word
def markdown_to_docx(conteudo_md):
    doc = Document()
    for line in conteudo_md.split("\n"):
        doc.add_paragraph(line)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Função para criar um arquivo ZIP com os documentos
def criar_zip(arquivos_md):
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        # Adiciona os arquivos .docx ao ZIP
        for arquivo_md in arquivos_md:
            try:
                with open(arquivo_md, 'r', encoding='utf-8') as file:
                    conteudo = file.read().replace("\n", "\n\n")
                    docx_buffer = markdown_to_docx(conteudo)
                    zip_file.writestr(arquivo_md.replace('.md', '.docx'), docx_buffer.getvalue())
            except FileNotFoundError:
                st.error(f"Arquivo {arquivo_md} não encontrado.")
    
    zip_buffer.seek(0)
    return zip_buffer

# Botão para iniciar a execução do pipeline
if st.button("Executar Análise"):
    # Exibe um spinner enquanto o pipeline está em execução
    with st.spinner("Analisando... por favor, aguarde."):
        if 'VidmarmercadoCrew' in globals():
            # Executa o pipeline com a URL fornecida
            crew_instance = VidmarminiCrew().crew()  # Cria uma instância da Crew
            result = crew_instance.kickoff(inputs={'site_url': site_url})  # Usa kickoff para iniciar a execução
            
            # Verifica se o pipeline retornou algum resultado
            if result:
                st.write("Análise concluída! Aqui estão os arquivos de saída:")
                
                # Atualize o session_state com os resultados
                st.session_state.analise_realizada = True
                st.session_state.arquivos_md = ["customer_feedback_analysis.md", "market_trends_monitoring.md", "product_comparison.md"]
        else:
            st.error("A análise não pôde ser executada devido a problemas na importação do módulo VidmarmercadoCrew.")

# Exibir botão para baixar todos os arquivos em um único arquivo ZIP após a análise ser realizada
if st.session_state.analise_realizada:
    zip_buffer = criar_zip(st.session_state.arquivos_md)
    st.download_button(
        label="Baixar todos os documentos em ZIP",
        data=zip_buffer,
        file_name="analise_mercado.zip",
        mime="application/zip"
    )
