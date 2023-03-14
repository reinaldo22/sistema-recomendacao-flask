from flask import Flask, request, render_template
from math import sqrt

app = Flask(__name__)

# Dados dos itens
avaliacoesUsuario = {'Ana': 
		{'Freddy x Jason': 2.5, 
		 'O Ultimato Bourne': 3.5,
		 'Star Trek': 3.0, 
		 'Exterminador do Futuro': 3.5, 
		 'Norbit': 2.5, 
		 'Star Wars': 3.0},
	 
	  'Marcos': 
		{'Freddy x Jason': 3.0, 
		 'O Ultimato Bourne': 3.5, 
		 'Star Trek': 1.5, 
		 'Exterminador do Futuro': 5.0, 
		 'Star Wars': 3.0, 
		 'Norbit': 3.5}, 

	  'Pedro': 
	    {'Freddy x Jason': 2.5, 
		 'O Ultimato Bourne': 3.0,
		 'Exterminador do Futuro': 3.5, 
		 'Star Wars': 4.0},
			 
	  'Claudia': 
		{'O Ultimato Bourne': 3.5, 
		 'Star Trek': 3.0,
		 'Star Wars': 4.5, 
		 'Exterminador do Futuro': 4.0, 
		 'Norbit': 2.5},
				 
	  'Adriano': 
		{'Freddy x Jason': 3.0, 
		 'O Ultimato Bourne': 4.0, 
		 'Star Trek': 2.0, 
		 'Exterminador do Futuro': 3.0, 
		 'Star Wars': 3.0,
		 'Norbit': 2.0}, 

	  'Janaina': 
	     {'Freddy x Jason': 3.0, 
	      'O Ultimato Bourne': 4.0,
	      'Star Wars': 3.0, 
	      'Exterminador do Futuro': 5.0, 
	      'Norbit': 3.5},
			  
	  'Leonardo': 
	    {'O Ultimato Bourne':4.5,
             'Norbit':1.0,
	     'Exterminador do Futuro':4.0}
}

avaliacoesFilme = {'Freddy x Jason': 
		{'Ana': 2.5, 
		 'Marcos:': 3.0 ,
		 'Pedro': 2.5, 
		 'Adriano': 3.0, 
		 'Janaina': 3.0 },
	 
	 'O Ultimato Bourne': 
		{'Ana': 3.5, 
		 'Marcos': 3.5,
		 'Pedro': 3.0, 
		 'Claudia': 3.5, 
		 'Adriano': 4.0, 
		 'Janaina': 4.0,
		 'Leonardo': 4.5 },
				 
	 'Star Trek': 
		{'Ana': 3.0, 
		 'Marcos:': 1.5,
		 'Claudia': 3.0, 
		 'Adriano': 2.0 },
	
	 'Exterminador do Futuro': 
		{'Ana': 3.5, 
		 'Marcos:': 5.0 ,
		 'Pedro': 3.5, 
		 'Claudia': 4.0, 
		 'Adriano': 3.0, 
		 'Janaina': 5.0,
		 'Leonardo': 4.0},
				 
	 'Norbit': 
		{'Ana': 2.5, 
		 'Marcos:': 3.0 ,
		 'Claudia': 2.5, 
		 'Adriano': 2.0, 
		 'Janaina': 3.5,
		 'Leonardo': 1.0},
				 
	 'Star Wars': 
		{'Ana': 3.0, 
		 'Marcos:': 3.5,
		 'Pedro': 4.0, 
		 'Claudia': 4.5, 
		 'Adriano': 3.0, 
		 'Janaina': 3.0}
}

def similaridade(user, avaliacoes):
    similaridades = {}
    for other_user in avaliacoes:
        if other_user != user:
            similaridade = 0
            intersecao = set(avaliacoes[user].keys()) & set(avaliacoes[other_user].keys())
            if intersecao:
                notas1 = [avaliacoes[user][filme] for filme in intersecao]
                notas2 = [avaliacoes[other_user][filme] for filme in intersecao]
                similaridade = sum([nota1 * nota2 for nota1, nota2 in zip(notas1, notas2)]) / (len(notas1) * len(notas2))
            else:
                similaridade = 0  # inicializa com zero se interseção for vazio
            similaridades[other_user] = similaridade
    return similaridades

    

# Função para obter a lista de recomendações com base nos gêneros selecionados e no valor do item escolhido
def get_recommendations(user, nota, avaliacoes):
    similaridades = similaridade(user, avaliacoes)
    notas = {}
    total_similaridade = {}
    for other_user in avaliacoes:
        if other_user != user:
            similaridade = similaridades.get(other_user, 0)
            if similaridade > 0:
                for filme in avaliacoes[other_user]:
                    if filme not in avaliacoes[user]:
                        notas.setdefault(filme, 0)
                        notas[filme] += avaliacoes[other_user][filme] * similaridade
                        total_similaridade.setdefault(filme, 0)
                        total_similaridade[filme] += similaridade
    rankings = [(nota / total_similaridade[filme], filme) for filme, nota in notas.items() if total_similaridade[filme] > 0]
    rankings.sort(reverse=True)
    return [filme for _, filme in rankings if _ >= nota]


    

# # Rota para a página inicial
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Rota para a página de recomendação
# @app.route('/recomendacao', methods=['GET', 'POST'])
# def recomendacao():
#     if request.method == 'POST':
#         # Obtendo os gêneros selecionados e o valor atribuído ao item escolhido
#         selected_genres = request.form.getlist('genres')
#         item_value = int(request.form['value'])
        
#         # Obtendo a lista de recomendações
#         recommended_items = get_recommendations(selected_genres, item_value)

#         # Retornando a lista de itens recomendados renderizados no template
#         return render_template('recomendacao.html', items=recommended_items[:10])
#     else:
#         # Retornando a página de seleção de gêneros e valor do item
#         return render_template('selecao.html')


@app.route('/teste')
def teste():
    este = get_recommendations('Marcos', 2, avaliacoes)
    print(este)
    return str(este)

if __name__ == '__main__':
    app.run(debug=True)
