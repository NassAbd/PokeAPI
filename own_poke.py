from flask import Flask, jsonify, request #import objects from the Flask model
app = Flask(__name__) #define app using Flask
import json

json_file = 'own_poke.json'

with open(json_file) as op:
    data = json.load(op)
    
def save_data():
    """Enregistre les données actuelles dans le fichier JSON."""
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)
    
# test    
@app.route('/', methods=['GET'])
def test():
    return jsonify({'message' : 'It works!'})

# all pokemons
@app.route('/pokemons', methods=['GET'])
def returnAll():
    #pokes = [poke for poke in data]
    return jsonify({'pokes' : data})

# a precise pokemon
@app.route('/pokemons/<string:name>', methods=['GET'])
def returnOne(name):
    poke_find = [poke for poke in data if poke['name'] == name]
    if not poke_find : 
        return jsonify({'error': 'pokemon not found'}), 400
    return jsonify({'poke' : poke_find})

# new pokemon
@app.route('/pokemons', methods=['POST'])
def addOne():
    # Récupérer les données JSON de la requête
    rq = request.json

    # Vérifier que toutes les données requises sont présentes
    if not all(key in rq for key in ('name', 'hp', 'attack', 'defense')):
        return jsonify({'error': 'Missing data'}), 400
    
    if rq["name"] in [poke["name"] for poke in data] : 
        return jsonify({'error': 'pokemon already here'}), 400

    # Créer un nouveau Pokémon avec les données reçues
    poke = {
        'name': rq['name'],
        'hp': rq['hp'],
        'attack': rq['attack'],
        'defense': rq['defense'],
    }

    # Ajouter le Pokémon à la liste
    data.append(poke)
    
    save_data()

    # Retourner la liste mise à jour
    return jsonify({'pokes': data}), 201

# change pokemon
@app.route('/pokemons/<string:oldname>/<string:newname>', methods=['PUT'])
def editOne(oldname, newname):
    poke_find = [poke for poke in data if poke['name'] == oldname]
    if not poke_find : 
        return jsonify({'error': 'pokemon not found'}), 400

    poke_find[0]['name'] = newname

    save_data()

    return jsonify({'pokes' : data})

# del pokemon
@app.route('/pokemons/<string:name>', methods=['DELETE'])
def removeOne(name):
    poke_find = [poke for poke in data if poke['name'] == name]
    if not poke_find : 
        return jsonify({'error': 'pokemon not found'}), 400
    data.remove(poke_find[0])

    save_data()
    
    return jsonify({'pokes' : data})

if __name__ == '__main__':
    app.run(debug=True, port=8080) #run app on port 8080 in debug mode