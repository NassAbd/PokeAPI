import streamlit as st
import requests
import time

def robust_api_call(url, max_retries=5, backoff_factor=2):
    """
    Requête HTTP GET vers l'URL donnée, avec gestion des erreurs.
    
    Paramètres :
    - url (str) : l'URL de l'API à appeler.
    - max_retries (int) : nombre maximum de tentatives en cas d'échec (défaut : 5).
    - backoff_factor (int) : facteur multiplicatif pour le délai d'attente entre les tentatives (défaut : 2).
    
    Retourne :
    - dict : Les données JSON de la réponse si la requête est réussie.
    - None : Si toutes les tentatives échouent.
    """
    retries = 0
    
    while retries < max_retries:
        try:
            response = requests.get(url)
            status_code = response.status_code
            
            # Si la requête est réussie
            if status_code == 200:
                return response.json()
            
            # Gérer les erreurs spécifiques
            if status_code == 429:
                # Trop de requêtes, attendre avant de réessayer
                retry_after = int(response.headers.get("Retry-After", 1))
                print(f"Erreur 429 : Trop de requêtes. Attente de {retry_after} secondes avant de réessayer.")
                time.sleep(retry_after)
            elif status_code in [500, 503]:
                # Erreurs serveur, attendre et réessayer
                wait_time = backoff_factor ** retries # backoff_factor ** retries = Délai augmentant avec le nombre de retry
                print(f"Erreur {status_code} : Problème de serveur. Réessayer dans {wait_time} secondes.")
                time.sleep(wait_time)
            elif status_code == 400:
                print("Erreur 400 : Mauvaise requête. Vérifiez l'URL ou les paramètres.")
                break
            elif status_code == 401:
                print("Erreur 401 : Non autorisé. Vérifiez le token d'authentification.")
                break
            elif status_code == 403:
                print("Erreur 403 : Accès interdit. Vous n'avez pas les droits nécessaires.")
                break
            elif status_code == 404:
                print("Erreur 404 : Ressource non trouvée. L'identifiant est peut-être incorrect.")
                break
            else:
                # Autres erreurs
                print(f"Erreur {status_code} : Une erreur inconnue est survenue.")
                break
            
        except requests.exceptions.ConnectionError:
            print("Erreur de connexion : Impossible de joindre l'API. Réessayer dans quelques secondes.")
            time.sleep(backoff_factor ** retries)
        except requests.exceptions.Timeout:
            print("Délai d'attente dépassé : L'API n'a pas répondu à temps. Réessayer.")
            time.sleep(backoff_factor ** retries)
        except requests.exceptions.RequestException as e:
            # Pour d'autres erreurs non prévues
            print(f"Une erreur inattendue est survenue : {e}")
            break
        
        # Augmenter le nombre de tentatives
        retries += 1
        print(f"Tentative {retries} sur {max_retries} échouée. Nouvelle tentative...")
    
    # Si toutes les tentatives échouent, retourner None
    print("Échec de la requête après plusieurs tentatives.")
    return None

# Exemple d'utilisation
url = "https://pokeapi.co/api/v2/pokemon/pikachu/"  # URL de l'API Pokémon pour pikachu
result = robust_api_call(url)

if result:
    print("Requête réussie :", result)
else:
    print("Impossible de récupérer les données après plusieurs tentatives.")



class Pokemon:
    def __init__(self, name):
        self.name = name
        self.hp = 0
        self.attack = 0
        self.defense = 0
        self.get_stats_from_api()

    def get_stats_from_api(self):
        """
        Récupère les statistiques du Pokémon à partir de l'API PokéAPI.
        """
        url = f"https://pokeapi.co/api/v2/pokemon/{self.name.lower()}"
        response = robust_api_call(url)

        data = response
        for stat in data['stats']:
            if stat['stat']['name'] == 'hp':
                self.hp = stat['base_stat']
            elif stat['stat']['name'] == 'attack':
                self.attack = stat['base_stat']
            elif stat['stat']['name'] == 'defense':
                self.defense = stat['base_stat']
        print(f"{self.name} - HP: {self.hp}, Attack: {self.attack}, Defense: {self.defense}")


    def calculate_damage(self, opponent):
        """
        Calcule les dégâts infligés à l'adversaire en fonction de l'attaque et de la défense.
        """
        damage = self.attack - (opponent.defense / 2)
        return max(1, int(damage)) # pour éviter damage <= 0

def simulate_battle(pokemon1, pokemon2, rounds=5):
    """
    Simule un combat entre deux Pokémon sur un nombre de tours spécifié.
    
    Paramètres :
    - pokemon1 : Premier Pokémon
    - pokemon2 : Deuxième Pokémon
    - rounds : Nombre de tours (5 par défaut)
    
    Retourne le Pokémon vainqueur ou 'Égalité' si les deux Pokémon infligent les mêmes dégâts totaux.
    """
    total_damage1 = 0
    total_damage2 = 0

    battle_log = []

    for round in range(1, rounds + 1):
        # Pokémon 1 attaque Pokémon 2
        damage_by_pokemon1 = pokemon1.calculate_damage(pokemon2)
        pokemon2.hp -= damage_by_pokemon1
        total_damage1 += damage_by_pokemon1
        to_print = f"Tour {round}: {pokemon1.name} inflige {damage_by_pokemon1} dégâts à {pokemon2.name} (HP restant: {pokemon2.hp})"
        battle_log.append(to_print + "\n")
        print(to_print)

        
        # Vérifier si Pokémon 2 est K.O.
        if pokemon2.hp <= 0:
            to_print = f"\n{pokemon2.name} est K.O.! {pokemon1.name} remporte le combat !"
            battle_log.append(to_print + "\n")
            print(to_print)
            return pokemon1, battle_log

        # Pokémon 2 attaque Pokémon 1
        damage_by_pokemon2 = pokemon2.calculate_damage(pokemon1)
        pokemon1.hp -= damage_by_pokemon2
        total_damage2 += damage_by_pokemon2
        to_print = f"Tour {round}: {pokemon2.name} inflige {damage_by_pokemon2} dégâts à {pokemon1.name} (HP restant: {pokemon1.hp})"
        battle_log.append(to_print + "\n")
        print(to_print)

        # Vérifier si Pokémon 1 est K.O.
        if pokemon1.hp <= 0:
            to_print = f"\n{pokemon1.name} est K.O.! {pokemon2.name} remporte le combat !"
            battle_log.append(to_print + "\n")
            print(to_print)
            return pokemon2, battle_log

    # Afficher les dégâts totaux infligés par chaque Pokémon
    to_print = f"\nDégâts totaux infligés par {pokemon1.name} : {total_damage1}"
    battle_log.append(to_print + "\n")
    print(to_print)
    to_print = f"Dégâts totaux infligés par {pokemon2.name} : {total_damage2}"
    battle_log.append(to_print + "\n")
    print(to_print)

    # Déterminer le vainqueur basé sur les dégâts totaux si personne n'est K.O.
    if total_damage1 > total_damage2:
        to_print = f"\n{pokemon1.name} remporte le combat avec le plus de dégâts infligés !"
        battle_log.append(to_print + "\n")
        print(to_print)
        return pokemon1, battle_log
    elif total_damage2 > total_damage1:
        to_print = f"\n{pokemon2.name} remporte le combat avec le plus de dégâts infligés !"
        battle_log.append(to_print + "\n")
        print(to_print)
        return pokemon2, battle_log
    else:
        to_print = "\nLe combat se termine par une égalité."
        battle_log.append(to_print + "\n")
        print(to_print)
        return "Égalité", battle_log
    
# Streamlit interface
st.title("Simulateur de Combat Pokémon")

# Entrée pour les noms des Pokémon
pokemon1_name = st.text_input("Entrez le nom du premier Pokémon:", "pikachu")
pokemon2_name = st.text_input("Entrez le nom du deuxième Pokémon:", "charmander")

# Bouton pour lancer la simulation
if st.button("Simuler le combat"):
    # Création des objets Pokémon
    try :
        pokemon1 = Pokemon(name=pokemon1_name)
        pokemon2 = Pokemon(name=pokemon2_name)
    except ValueError: 
        print("Problème à l'initialisation des pokémons")

    # Simuler le combat
    winner, battle_log = simulate_battle(pokemon1, pokemon2)

    # Affichage des résultats
    st.subheader("Résultats du combat")
    for log in battle_log:
        st.write(log)
    
    # Afficher le vainqueur
    if isinstance(winner, Pokemon):
        st.success(f"Le vainqueur est : {winner.name}")
    else:
        st.info("Le combat se termine par une égalité.")
