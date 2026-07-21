import requests
from collections import Counter
 
def fetch_all_posts() -> list[dict]:
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        timeout=5,
    )
    response.raise_for_status()
    return response.json()
 
 
def analyse(posts: list[dict]) -> None:
    print(f"Nombre total de posts : {len(posts)}")
    
    long_titles = sum(1 for p in posts if len(p["title"]) > 30)
    print(f"Titres de plus de 30 caractères : {long_titles}")
    
    user_counts = Counter(p["userId"] for p in posts)
    top_user, top_count = user_counts.most_common(1)[0]
    print(f"Utilisateur le plus prolifique : {top_user} ({top_count} posts)")
 
 
if __name__ == "__main__":
    posts = fetch_all_posts()
    analyse(posts)
