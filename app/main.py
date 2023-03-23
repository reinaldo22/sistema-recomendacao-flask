from flask import Flask, jsonify, request, render_template
import os
import json
import math

app = Flask(__name__)

# Define o caminho completo para o arquivo JSON
caminho_arquivo = os.path.join('dataset', 'eventos.json')

# Abre o arquivo JSON
with open(caminho_arquivo, 'r') as f:
    data = json.load(f)

# Função para obter o vetor de características de uma festa
def get_evento_vector(value):
    # generos = ["Pop", "Eletrônica", "Forró", "Sertanejo", "Techno", "House", "Rock", "MPB", "Funk"]
    vector = []

    for genero in value:
        if genero in value["genero_musical"]:
            vector.append(1)
        else:
            vector.append(0)
   
    vector.append(value["idade_minima"])
    vector.append(value["preco"])
   
    data_parts = value["data"].split("-")
    vector.extend(data_parts)
   
    return vector


# Função para calcular a similaridade entre dois vetores de características
def euclidean_distance(vec1, vec2):
    squared_diffs = [(float(vec1[i])-float(vec2[i]))**2 for i in range(len(vec1))]
    return math.sqrt(sum(squared_diffs))


def recommend_eventos(usuario_referencia, data, n=3):
    # Obtém o vetor de características do usuário
    usuario_vector = get_evento_vector(usuario_referencia)

    # Calcula a distância euclidiana entre o vetor do usuário e o vetor de cada festa
    distancias = []
    for festa in data:
        festa_vector = get_evento_vector(festa)
        distancia = euclidean_distance(usuario_vector, festa_vector)
        distancias.append((festa, distancia))

    # Ordena as festas por distância e retorna as n mais próximas
    distancias.sort(key=lambda x: x[1])
    return [x[0] for x in distancias[:n]]


def register(name, description, date, place, genre, age, price):
    new_id = -1
    for element in data:
        new_id = element['id']

    new_data = {'id': new_id + 1, 'nome': name, 'descricao': description, 'data': date, 'local': place, 'genero_musical':[genre], 'idade_minima': age, 'preco': price}
    data.append(new_data)

    with open(caminho_arquivo, 'w') as f:
        json.dump(data, f)


@app.route('/', methods=['GET', 'POST'])
def show_recommendations():
    if (request.form):
        date = request.form['date']
        genre = request.form['genre']
        age = request.form['age']
        price = request.form['price']
        
        new_data = {'data': date, 'idade_minima': int(age), 'preco': float(price), 'genero_musical': [genre]}
        recommendations = recommend_eventos(new_data, data)
        
        print(recommendations)

        return render_template('index.html', items=recommendations)

    return render_template('index.html')


@app.route('/cadastrar-evento', methods=['GET', 'POST'])
def show_register():
    if (request.form):
        name = request.form['name']
        description = request.form['description']
        date = request.form['date']
        place = request.form['place']
        genre = request.form['genre']
        age = request.form['age']
        price = request.form['price']
        register(name, description, date, place, genre, int(age), float(price))

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
