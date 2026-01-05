import sys
from pathlib import Path
import redis

# Add project root to path
sys.path.append(str(Path(__file__).parents[1]))

from backend.app.core.settings import settings

def debug_redis():
    print(f"--- Debug Redis ---")
    print(f"URL: {settings.redis_url}")
    
    try:
        r = redis.from_url(settings.redis_url, decode_responses=True)
        r.ping()
        print("✅ Connexion Redis OK")
        
        queue_len = r.llen("jobs")
        print(f"Jobs dans la file 'jobs': {queue_len}")
        
        if queue_len > 0:
            print("⚠️ Il y a des jobs en attente. Le worker ne les consomme pas ?")
            items = r.lrange("jobs", 0, -1)
            print(f"IDs des jobs: {items}")
        else:
            print("ℹ️ File vide. Si vous avez créé un job, il a peut-être déjà été consommé (ou jamais envoyé).")
            
    except Exception as e:
        print(f"❌ Erreur connexion Redis: {e}")

if __name__ == "__main__":
    debug_redis()
