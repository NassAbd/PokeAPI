import requests
import time

def fetch(url):
    """
    Effectue une requête GET asynchrone à l'URL spécifiée.
    
    Paramètres :
    - url (str) : l'URL de l'API à appeler.
    - session (ClientSession) : la session aiohttp pour réutiliser les connexions.
    
    Retourne :
    - dict : Les données JSON de la réponse si la requête est réussie.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Succès : {url}")
            return data
        else:
            print(f"Erreur {response.status_code} : {url}")
            return None
    except Exception as e:
        print(f"Exception pour {url}: {e}")
        return None

def fetch_all(urls):
    """
    Gère l'envoi de requêtes asynchrones à toutes les URLs avec un contrôle de la concurrence.
    
    Paramètres :
    - urls (list) : la liste des URLs à appeler.
    - max_concurrent_requests (int) : nombre maximum de requêtes concurrentes.
    """
    tasks = []
    for url in urls:
        tasks.append(fetch(url))
    results = tasks
    return results

def simulate_high_load(urls, total_requests):
    """
    Simule une charge élevée de requêtes en répétant les appels vers les URLs.
    
    Paramètres :
    - urls (list) : la liste des URLs à appeler.
    - total_requests (int) : nombre total de requêtes à envoyer.
    - max_concurrent_requests (int) : nombre maximum de requêtes concurrentes.
    """
    # Générer la liste des URLs à appeler
    all_urls = urls * (total_requests // len(urls)) # répartition équitable du nombre d'URL 
    start_time = time.time()

    # Exécuter les requêtes asynchrones
    fetch_all(all_urls)

    end_time = time.time()
    print(f"Temps total pour {total_requests} requêtes : {end_time - start_time:.2f} secondes")

# Exemple d'utilisation
if __name__ == "__main__":
    urls = [
        "https://pokeapi.co/api/v2/pokemon/pikachu/",
        "https://pokeapi.co/api/v2/pokemon/jigglypuff/",
        "https://pokeapi.co/api/v2/pokemon/charizard/"
    ]
    total_requests = 100  # Nombre total de requêtes à envoyer (simuler une charge élevée)

    simulate_high_load(urls, total_requests)
