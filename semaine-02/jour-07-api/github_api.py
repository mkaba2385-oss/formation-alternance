import requests
 
 
def fetch_github_user(username: str) -> dict:
    response = requests.get(f"https://api.github.com/users/{username}", timeout=5)
    response.raise_for_status()
    return response.json()
 
 
def fetch_github_repos(username: str) -> list[dict]:
    response = requests.get(
        f"https://api.github.com/users/{username}/repos",
        params={"per_page": 100, "sort": "updated"},
        timeout=5,
    )
    response.raise_for_status()
    return response.json()
 
 
def show_profile(username: str) -> None:
    user = fetch_github_user(username)
    repos = fetch_github_repos(username)
    
    print(f"Profil : {user['name'] or user['login']}")
    print(f"Dépôts publics : {user['public_repos']}")
    print(f"Followers : {user['followers']}")
    
    top5 = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)[:5]
    print("\nTop 5 dépôts :")
    for repo in top5:
        print(f"  {repo['name']:30} {repo['stargazers_count']:>5} ")
 
 
if __name__ == "__main__":
    show_profile("torvalds")
