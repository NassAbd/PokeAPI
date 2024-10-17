import requests
import streamlit as st

def get_pokemon_data(pokemon_name_or_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur : Le Pokémon {pokemon_name_or_id} n'a pas été trouvé.")
        return None

def display_pokemon_stats(pokemon_name_or_id):
    stats = []
    data = get_pokemon_data(pokemon_name_or_id)
    if data:
        name = data['name']
        hp = data['stats'][0]['base_stat']
        attack = data['stats'][1]['base_stat']
        defense = data['stats'][2]['base_stat']
        speed = data['stats'][5]['base_stat']

        to_print = f"\nStatistiques de {name.capitalize()}:"
        stats.append(to_print)
        print(to_print)
        to_print = f"- Points de vie (HP) : {hp}"
        stats.append(to_print)
        print(to_print)
        to_print = f"- Attaque : {attack}"
        stats.append(to_print)
        print(to_print)
        to_print = f"- Défense : {defense}"
        stats.append(to_print)
        print(to_print)
        to_print = f"- Vitesse : {speed}"
        stats.append(to_print)
        print(to_print)

        return stats

def compare_pokemon(pokemon1, pokemon2):
    comparaison = []

    data1 = get_pokemon_data(pokemon1)
    data2 = get_pokemon_data(pokemon2)
    if data1 and data2:
        hp1 = data1['stats'][0]['base_stat']
        attack1 = data1['stats'][1]['base_stat']
        hp2 = data2['stats'][0]['base_stat']
        attack2 = data2['stats'][1]['base_stat']
        
        to_print = f"\nComparaison entre {pokemon1.capitalize()} et {pokemon2.capitalize()}:"
        comparaison.append(to_print)
        print(to_print)
        if hp1 > hp2:
            to_print = f"{pokemon1.capitalize()} a plus de points de vie ({hp1} contre {hp2})."
            comparaison.append(to_print)
            print(to_print)
        else:
            to_print = f"{pokemon2.capitalize()} a plus de points de vie ({hp2} contre {hp1})."
            comparaison.append(to_print)
            print(to_print)
        
        if attack1 > attack2:
            to_print = f"{pokemon1.capitalize()} a une meilleure attaque ({attack1} contre {attack2})."
            comparaison.append(to_print)
            print(to_print)
        else:
            to_print = f"{pokemon2.capitalize()} a une meilleure attaque ({attack2} contre {attack1})."
            comparaison.append(to_print)
            print(to_print)
        
        return comparaison

def calculate_type_stats(pokemon_type):
    stats = []

    url = f"https://pokeapi.co/api/v2/type/{pokemon_type.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_list = data['pokemon']
        total_hp = 0
        count = 0

        for pokemon_entry in pokemon_list:
            pokemon_name = pokemon_entry['pokemon']['name']
            pokemon_data = get_pokemon_data(pokemon_name)
            if pokemon_data:
                hp = pokemon_data['stats'][0]['base_stat']
                total_hp += hp
                count += 1

        if count > 0:
            average_hp = total_hp / count
            to_print = f"\nStatistiques pour le type {pokemon_type.capitalize()}:"
            stats.append(to_print)
            print(to_print)
            to_print = f"- Nombre de Pokémon : {count}"
            stats.append(to_print)
            print(to_print)
            to_print = f"- Moyenne des points de vie (HP) : {average_hp:.2f}"
            stats.append(to_print)
            print(to_print)
        else:
            to_print = f"Aucun Pokémon trouvé pour le type {pokemon_type}."
            stats.append(to_print)
            print(to_print)
    else:
        to_print = f"Erreur : Le type {pokemon_type} n'a pas été trouvé."
        stats.append(to_print)
        print(to_print)

    return stats


# Streamlit interface
st.title("Infos Pokémon")

# Entrée pour les noms des Pokémon
pokemon_info_name = st.text_input("Entrez le nom d'un pokémon", "pikachu")
if st.button("Obtenir infos"):

    stats = display_pokemon_stats(pokemon_info_name)
    st.write(stats)

st.title("Compare Pokémon")

pokemon1_compare_name = st.text_input("Entrez le nom du premier Pokémon:", "jigglypuff")
pokemon2_compare_name = st.text_input("Entrez le nom du deuxième Pokémon:", "charmander")

# Bouton pour lancer la simulation
if st.button("Comparer"):
   
    comparaison = compare_pokemon(pokemon1_compare_name, pokemon2_compare_name)
    st.write(comparaison)

st.title("Infos Type")

type = st.text_input("Entrez le nom d'un type", "fire")
if st.button("Obtenir infos type"):

    stats = calculate_type_stats(type)
    st.write(stats)