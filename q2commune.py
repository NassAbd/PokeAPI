import time
import asyncio # pour le parallèlisme
import aiohttp # pour gérer les requêtes async
from aiohttp import ClientSession

async def fetch(url, session):
    """
    Effectue une requête GET asynchrone à l'URL spécifiée.
    
    Paramètres :
    - url (str) : l'URL de l'API à appeler.
    - session (ClientSession) : la session aiohttp pour réutiliser les connexions.
    
    Retourne :
    - dict : Les données JSON de la réponse si la requête est réussie.
    """
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                print(f"Succès : {url}")
                return data
            else:
                print(f"Erreur {response.status} : {url}")
                return None
    except Exception as e:
        print(f"Exception pour {url}: {e}")
        return None

async def fetch_all(urls, max_concurrent_requests):
    """
    Gère l'envoi de requêtes asynchrones à toutes les URLs avec un contrôle de la concurrence.
    
    Paramètres :
    - urls (list) : la liste des URLs à appeler.
    - max_concurrent_requests (int) : nombre maximum de requêtes concurrentes.
    """
    connector = aiohttp.TCPConnector(limit_per_host=max_concurrent_requests)
    async with ClientSession(connector=connector) as session:
        tasks = []
        for url in urls:
            tasks.append(fetch(url, session))
        results = await asyncio.gather(*tasks)
        return results

def simulate_high_load(urls, total_requests, max_concurrent_requests):
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
    asyncio.run(fetch_all(all_urls, max_concurrent_requests))

    end_time = time.time()
    print(f"Temps total pour {total_requests} requêtes : {end_time - start_time:.2f} secondes")

# Exemple d'utilisation
if __name__ == "__main__":
    urls = [
        "https://pokeapi.co/api/v2/pokemon/pikachu/",
        "https://pokeapi.co/api/v2/pokemon/jigglypuff/",
        "https://pokeapi.co/api/v2/pokemon/charizard/"
    ]
    total_requests = 1000  # Nombre total de requêtes à envoyer (simuler une charge élevée)
    max_concurrent_requests = 100  # Limite de requêtes concurrentes

    simulate_high_load(urls, total_requests, max_concurrent_requests)
