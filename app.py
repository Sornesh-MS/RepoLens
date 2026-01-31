from flask import Flask, jsonify
import requests
from collections import Counter

app = Flask(__name__)

GITHUB_BASE_URL = "https://api.github.com/users/"


@app.route("/")
def home():
    return jsonify({
        "message": "GitHub Profile Analyzer API",
        "usage": "/<github_username>"
    })


@app.route("/<username>")
def analyze_github_profile(username):

    # Fetch Profile
    profile_response = requests.get(GITHUB_BASE_URL + username)

    if profile_response.status_code != 200:
        return jsonify({"error": "GitHub user not found"}), 404

    profile = profile_response.json()

    #Fetch Repositories
    repos_response = requests.get(GITHUB_BASE_URL + username + "/repos")
    repos = repos_response.json() if repos_response.status_code == 200 else []

    # Analyze Repositories
    total_stars = 0
    total_forks = 0
    languages = []
    most_starred_repo = None
    max_stars = 0

    for repo in repos:
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        language = repo.get("language")

        total_stars += stars
        total_forks += forks

        if language:
            languages.append(language)

        if stars > max_stars:
            max_stars = stars
            most_starred_repo = repo.get("name")

    # Final JSON Response
    result = {
        "username": username,
        "name": profile.get("name"),
        "bio": profile.get("bio"),
        "public_repositories": profile.get("public_repos"),
        "followers": profile.get("followers"),
        "following": profile.get("following"),
        "analysis": {
            "total_repositories": len(repos),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "most_used_languages": dict(Counter(languages)),
            "most_starred_repository": most_starred_repo
        }
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
