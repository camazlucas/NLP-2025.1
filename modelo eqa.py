def carregar_documento(caminho_do_pdf):

    with pdfplumber.open(caminho_do_pdf) as pdf:
        texto = " ".join(
            page.extract_text() for page in pdf.pages
            if page.extract_text()
        )
        texto = " ".join(texto.split())
    return texto

def dividir_em_chunks_tokenizados(texto):

    tokens = tokenizer.tokenize(texto)
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = tokens[i:i + chunk_size]
        chunks.append(tokenizer.convert_tokens_to_string(chunk))
    return chunks

def sliding_window_tokenizados(texto):
    tokens = tokenizer.tokenize(texto)
    janelas = []

    for i in range(0, len(tokens), stride):
        janela = tokens[i:i + window_size]
        texto_janela = tokenizer.convert_tokens_to_string(janela)
        janelas.append(texto_janela)

        if i + window_size >= len(tokens):
            break

    return janelas

def processar_pergunta(pergunta, documento):

    chunks = divisao_do_texto

    # 1. Tokeniza a pergunta para verificar tamanho
    tokens_pergunta = tokenizer.tokenize(pergunta)
    if len(tokens_pergunta) > tamanho_pergunta:  # Limite arbitrário (ajuste conforme necessário)
        print("Pergunta muito longa! Simplifique para melhor precisão.")

    # 2. Executa Q&A em cada chunk
    respostas = []
    for chunk in chunks:
        try:
            resposta = qa_pipeline(question=pergunta, context=chunk)
            respostas.append(resposta)

            resposta_completa = {
                'answer': resposta.get('answer', ''),
                'score': resposta.get('score', 0),
                'context': resposta.get('context', chunk[:500])  # Fallback: 500 primeiros chars
            }
            respostas.append(resposta_completa)
        except Exception as e:
            print(f"Erro no chunk: {str(e)}")
            continue

    # 3. Filtra respostas com score baixo e seleciona a melhor
    respostas_validas = [r for r in respostas if r['score'] >= 0.2]
    if not respostas_validas:
        print("Não há resposta sobre isto nesse documento.")
        return None

    return max(respostas_validas, key=lambda x: x['score'])