from flask import Flask, jsonify, request, render_template
import os
import json
import math


app = Flask(__name__)

# Define o caminho completo para o arquivo JSON
caminho_arquivo = os.path.join('dataset', 'festas.json')

# Abre o arquivo JSON
with open(caminho_arquivo, 'r') as f:
    data = json.load(f)
    
	
def get_festa_vector(data):
   
    festa_vector = []
    
    # Adiciona a data como uma característica
    data_parts = data["data"].split("-")
    year = int(data_parts[0])
    month = int(data_parts[1])
    day = int(data_parts[2])
    festa_vector += [year, month, day]
    
    # Adiciona o local como uma característica
    local_parts = data["local"].split(" ")
    for part in local_parts:
        festa_vector += [ord(c) for c in part]
        
    # Adiciona os gêneros musicais como características
    generos = data["genero_musical"]
    for genero in generos:
        festa_vector += [ord(c) for c in genero]
    
    # Adiciona o preço como uma característica
    festa_vector.append(data["preco"])
    
    return festa_vector

def cosine_similarity(vector1, vector2):
    # Calcula a similaridade do cosseno entre dois vetores
    dot_product = 0
    magnitude1 = 0
    magnitude2 = 0
    for i in range(len(vector1)):
        dot_product += vector1[i] * vector2[i]
        magnitude1 += vector1[i] ** 2
        magnitude2 += vector2[i] ** 2
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    else:
        return dot_product / (math.sqrt(magnitude1) * math.sqrt(magnitude2))
    

def recommend_festas(usuario_referencia, festas):
    # Encontra as festas mais similares com base nas características do usuário
    usuario_vector = get_festa_vector(usuario_referencia)
    recomendacoes = []
    for festa in data:
        festa_vector = get_festa_vector(festa)
        similaridade = cosine_similarity(usuario_vector, festa_vector)
        recomendacoes.append((festa["nome"], similaridade))
    
    # Filtra as recomendações de acordo com as preferências do usuário
    recomendacoes_filtradas = []
    for recomendacao in recomendacoes:
        festa = next((f for f in data if f["nome"] == recomendacao[0]), None)
        if festa:
            preco = festa["preco"]
            generos = festa["genero_musical"]
            if preco <= usuario_referencia["preco_maximo"] and usuario_referencia["genero_musical"][0] in generos:
                recomendacoes_filtradas.append(recomendacao)
    
    # Ordena as recomendações filtradas por ordem decrescente de similaridade
    recomendacoes_filtradas = sorted(recomendacoes_filtradas, key=lambda x: x[1], reverse=True)
    
    return recomendacoes_filtradas
    

@app.route('/lista-devedores')
def lista():
    
    return jsonify(data)
    

    
@app.route('/lista-festa/<int:id>', methods=['GET'])
def findId(id):
    for festa in data:
        if festa.get('id') == id:
            return jsonify(festa)

    
@app.route('/busca-festa', methods=['POST'])
def filtraFesta():
    festa = request.get_json()
    
    recommendations = recommend_festas(festa, data)
    print(">>>>>>>>>>>>>>"+recommendations)


    return jsonify(recommendations)
        



# @app.route('/usuarios-filtro')
# def get_usuarios_filtro():
#     usuarios_filtrados = filtra_usuarios(data, 0, 1000)
#     return jsonify(usuarios_filtrados)




if __name__ == '__main__':
    app.run(debug=True)
