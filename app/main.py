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
    # generos = ["Pop", "Eletrônica", "Forró", "Sertanejo", "Techno", "House", "Rock", "MPB", "Funk"]
    vector = []
    for genero in data:
        if genero in data["genero_musical"]:
            vector.append(1)
        else:
            vector.append(0)
    vector.append(data["idade_minima"])
    vector.append(data["preco"])
    data_parts = data["data"].split("-")
    vector.extend(data_parts)
    return vector

# Função para calcular a similaridade entre dois vetores de características
def euclidean_distance(vec1, vec2):
    squared_diffs = [(float(vec1[i])-float(vec2[i]))**2 for i in range(len(vec1))]
    return math.sqrt(sum(squared_diffs))

def recommend_festas(usuario_referencia, data, n=3):
    # Obtém o vetor de características do usuário
    usuario_vector = get_festa_vector(usuario_referencia)

    # Calcula a distância euclidiana entre o vetor do usuário e o vetor de cada festa
    distancias = []
    for festa in data:
        festa_vector = get_festa_vector(festa)
        distancia = euclidean_distance(usuario_vector, festa_vector)
        distancias.append((festa, distancia))

    # Ordena as festas por distância e retorna as n mais próximas
    distancias.sort(key=lambda x: x[1])
    return [x[0] for x in distancias[:n]]



@app.route('/lista-festas' , methods=['GET'])
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
