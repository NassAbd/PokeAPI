import time
import asyncio # pour le parallèlisme
import aiohttp # pour gérer les requêtes async
from aiohttp import ClientSession
import cachetools.func # garder le résultat de fetch_with_cache avec les mêmes paramètres


#@cache
@cachetools.func.ttl_cache(maxsize=100, ttl=60 * 60) # durée limitée : 60 * 60 secondes = 1h
async def fetch_with_cache(url, session):
    """
    Effectue une requête GET asynchrone à l'URL spécifiée avec mise en cache.
    
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
                print(f"[CACHE MISS] Requête effectuée : {url}")
                return data
            else:
                print(f"Erreur {response.status} : {url}")
                return None
    except Exception as e:
        print(f"Exception pour {url}: {e}")
        return None

async def fetch_all_with_cache(urls, max_concurrent_requests):
    """
    Gère l'envoi de requêtes asynchrones à toutes les URLs avec un contrôle de la concurrence et du cache.
    
    Paramètres :
    - urls (list) : la liste des URLs à appeler.
    - max_concurrent_requests (int) : nombre maximum de requêtes concurrentes.
    """
    connector = aiohttp.TCPConnector(limit_per_host=max_concurrent_requests)
    async with ClientSession(connector=connector) as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_with_cache(url, session))
        results = await asyncio.gather(*tasks)
        return results

def simulate_high_load_with_cache(urls, total_requests, max_concurrent_requests):
    """
    Simule une charge élevée de requêtes en répétant les appels vers les URLs avec gestion du cache.
    
    Paramètres :
    - urls (list) : la liste des URLs à appeler.
    - total_requests (int) : nombre total de requêtes à envoyer.
    - max_concurrent_requests (int) : nombre maximum de requêtes concurrentes.
    """
    # Générer la liste des URLs à appeler
    all_urls = urls * (total_requests // len(urls))
    start_time = time.time()

    # Exécuter les requêtes asynchrones avec cache
    asyncio.run(fetch_all_with_cache(all_urls, max_concurrent_requests))

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

    simulate_high_load_with_cache(urls, total_requests, max_concurrent_requests)
