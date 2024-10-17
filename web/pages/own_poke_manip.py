import streamlit as st
import requests

# Définir l'URL de base de l'API Flask
BASE_URL = "http://localhost:8080"

st.title("Gestion de mes Pokémon")

# Option pour afficher tous les Pokémon
if st.button("Afficher tous les Pokémon"):
    response = requests.get(f"{BASE_URL}/pokemons")
    if response.status_code == 200:
        pokemons = response.json().get('pokes', [])
        st.write("Liste des Pokémon :")
        for pokemon in pokemons:
            st.write(f"Nom : {pokemon['name']}, HP : {pokemon['hp']}, Attack : {pokemon['attack']}, Defense : {pokemon['defense']}")
    else:
        st.error("Erreur lors de la récupération des Pokémon.")

# Option pour ajouter un nouveau Pokémon
st.header("Ajouter un nouveau Pokémon")
new_name = st.text_input("Nom du Pokémon")
new_hp = st.number_input("HP", min_value=1, step=1)
new_attack = st.number_input("Attaque", min_value=1, step=1)
new_defense = st.number_input("Défense", min_value=1, step=1)

if st.button("Ajouter le Pokémon"):
    if new_name and new_hp and new_attack and new_defense:
        new_pokemon = {
            "name": new_name,
            "hp": new_hp,
            "attack": new_attack,
            "defense": new_defense
        }
        response = requests.post(f"{BASE_URL}/pokemons", json=new_pokemon)
        if response.status_code == 201:
            st.success("Pokémon ajouté avec succès !")
        else:
            st.error("Erreur lors de l'ajout du Pokémon : " + response.json().get('error', 'Unknown error'))
    else:
        st.warning("Veuillez remplir tous les champs.")

# Option pour modifier le nom d'un Pokémon
st.header("Modifier le nom d'un Pokémon")
old_name = st.text_input("Nom actuel du Pokémon à modifier")
new_name_for_update = st.text_input("Nouveau nom du Pokémon")

if st.button("Modifier le nom"):
    if old_name and new_name_for_update:
        response = requests.put(f"{BASE_URL}/pokemons/{old_name}/{new_name_for_update}")
        if response.status_code == 200:
            st.success("Nom du Pokémon mis à jour avec succès !")
        else:
            st.error("Erreur lors de la mise à jour : " + response.json().get('error', 'Unknown error'))
    else:
        st.warning("Veuillez fournir les deux noms.")

# Option pour supprimer un Pokémon
st.header("Supprimer un Pokémon")
name_to_delete = st.text_input("Nom du Pokémon à supprimer")

if st.button("Supprimer le Pokémon"):
    if name_to_delete:
        response = requests.delete(f"{BASE_URL}/pokemons/{name_to_delete}")
        if response.status_code == 200:
            st.success("Pokémon supprimé avec succès !")
        else:
            st.error("Erreur lors de la suppression : " + response.json().get('error', 'Unknown error'))
    else:
        st.warning("Veuillez indiquer le nom du Pokémon.")
