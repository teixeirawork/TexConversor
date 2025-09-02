import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS # Importa a biblioteca CORS
import fitz # PyMuPDF
from docx import Document
from io import BytesIO

# Instalar as bibliotecas necessárias:
# pip install Flask PyMuPDF python-docx Flask-Cors gunicorn

app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas da sua aplicação

@app.route('/convert', methods=['POST'])
def convert_pdf_to_word():
    """
    Endpoint da API para converter um arquivo PDF em Word.
    """
    print("---------------------------------------")
    print("Requisição recebida para /convert")

    # 1. Verifica se o arquivo foi enviado na requisição
    if 'file' not in request.files:
        print("Erro: Nenhum arquivo enviado")
        print("---------------------------------------")
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    pdf_file = request.files['file']

    # 2. Verifica se o nome do arquivo não está vazio
    if pdf_file.filename == '':
        print("Erro: Nome do arquivo vazio")
        print("---------------------------------------")
        return jsonify({"error": "Nome do arquivo vazio"}), 400

    # 3. Processa o arquivo se for um PDF válido
    if pdf_file and pdf_file.filename.endswith('.pdf'):
        try:
            print("Iniciando a conversão do PDF...")
            # Converte o PDF em texto usando PyMuPDF
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            doc_content = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                doc_content += page.get_text() + "\n\n"
            
            print("Conteúdo do PDF lido com sucesso.")

            # Cria um novo documento Word na memória
            doc = Document()
            doc.add_paragraph(doc_content)
            
            print("Documento Word criado.")

            # Salva o documento Word em um buffer de bytes na memória
            doc_bytes_io = BytesIO()
            doc.save(doc_bytes_io)
            doc_bytes_io.seek(0)
            
            print("Conversão finalizada com sucesso! Enviando arquivo...")

            # Envia o arquivo Word para o cliente
            return send_file(
                doc_bytes_io,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                download_name=f"{os.path.splitext(pdf_file.filename)[0]}.docx"
            )

        except Exception as e:
            # Retorna um erro caso algo dê errado no processamento
            print(f"Erro na conversão: {e}")
            print("---------------------------------------")
            return jsonify({"error": "Erro interno no servidor"}), 500
    
    # Retorna erro se o tipo de arquivo não for PDF
    print("Erro: Tipo de arquivo não suportado")
    print("---------------------------------------")
    return jsonify({"error": "Tipo de arquivo não suportado, por favor, envie um PDF."}), 415

if __name__ == '__main__':
    # Define a porta do servidor para o ambiente de produção
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
