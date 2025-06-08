def recuperar_chunks(pergunta, modelo_vetorizador, divisao_do_texto, k=3):
    # Vetoriza a pergunta
    vetor_pergunta = modelo_vetorizador.encode([pergunta], convert_to_tensor=False)
    
    # Vetoriza todos os chunks
    vetores_chunks = modelo_vetorizador.encode(divisao_do_texto, convert_to_tensor=False)
    
    # Calcula similaridade
    sim = cosine_similarity(vetor_pergunta, vetores_chunks)
    
    # Pega índices dos top-k chunks mais similares
    top_k_indices = np.argsort(sim[0])[::-1][:k]
    
    chunks_relevantes = [divisao_do_texto[i] for i in top_k_indices]
    
    return chunks_relevantes

def gerar_resposta(pergunta, chunks_relevantes):
    contexto = " ".join(chunks_relevantes)
    prompt = f"Contexto: {contexto} \n\nPergunta: {pergunta} \n\nResposta:"
    resposta = modelo_gerador(prompt, max_length=200)
    return resposta[0]['generated_text']