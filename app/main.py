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

# Função para obter o vetor de características de uma festa
def get_festa_vector(data):
    vector = []
    vector.append(data["nome"])
    data_parts = data["data"].split("-")
    vector.extend(data_parts)
    local_parts = data["local"].split(" ")
    for part in local_parts:
        vector += [ord(c) for c in part]
    generos = data["genero_musical"]
    for genero in generos:
        vector += [ord(c) for c in genero]
    vector.append(data["preco"])
    return vector

# Função para calcular a similaridade entre dois vetores de características
def cosine_similarity(vec1, vec2):
    dot_product = sum([float(vec1[i])*float(vec2[i]) for i in range(len(vec1))])
    magnitude1 = math.sqrt(sum([float(num)**2 for num in vec1]))
    magnitude2 = math.sqrt(sum([float(num)**2 for num in vec2]))
    return dot_product/(magnitude1*magnitude2)

# Função para recomendar festas com base em um usuário de referência
def recommend_festas(usuario_referencia, data, n=3):
    # Obtém o vetor de características do usuário
    usuario_vector = get_festa_vector(usuario_referencia)
    # Calcula a similaridade entre o vetor do usuário e o vetor de cada festa
    similaridades = []
    for festa in data:
        festa_vector = get_festa_vector(festa)
        similaridade = cosine_similarity(usuario_vector, festa_vector)
        similaridades.append((festa, similaridade))
    # Ordena as festas por similaridade e retorna as n melhores
    similaridades.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in similaridades[:n]]

@app.route('/lista-devedores')
def lista():
    return jsonify(data)

@app.route('/festa-id/<int:id>', methods=['GET'])
def findId(id):
    for festa in data:
        if festa.get('id') == id:
            return jsonify(festa)

@app.route('/busca-festa', methods=['POST'])
def filtraFesta():
    try:
        festa = request.get_json()
        recommendations = recommend_festas(festa, data)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': 'Invalid JSON: {}'.format(e)})

if __name__ == '__main__':
    app.run(debug=True)
