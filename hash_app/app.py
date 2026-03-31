from flask import Flask, render_template, request, session
import hashing_core
import os

app = Flask(__name__)
app.secret_key = "hashtable_portfolio_secret"

WORDS_FILE = "words.txt"

# These hold the built tables and words in memory so we don't rebuild on every request
tables_cache = None
words_cache = None


# Returns cached tables, or builds them from scratch if not yet loaded
def get_tables():
    global tables_cache, words_cache
    if tables_cache is None:
        words = hashing_core.read_words(WORDS_FILE)
        words_cache = words
        tables_cache = hashing_core.build_all_tables(words)
    return tables_cache, words_cache


# Landing page
@app.route("/")
def index():
    return render_template("index.html")


# Builds all 12 tables and shows the dashboard with stats
@app.route("/build")
def build():
    global tables_cache, words_cache
    tables_cache = None   # clear cache so tables are rebuilt fresh
    words_cache = None
    tables, words = get_tables()

    # Prepare display-friendly stats for each table
    stats = []
    for info in tables:
        stats.append({
            "hash_name": info["hash_name"],
            "strategy_name": info["strategy_name"],
            "size": info["size"],
            "load_factor": info["load_factor"],
            "collisions": info["collisions"],
            "non_empty": info["non_empty"],
            "empty": info["empty"],
            "load_pct": round(info["load_factor"] * 100, 1)  # as percentage for the progress bar
        })

    return render_template("dashboard.html", stats=stats, total_words=len(words))


# Handles the search form — searches the word in all 12 tables
@app.route("/search", methods=["POST"])
def search():
    word = request.form.get("word", "").strip()
    if not word:
        return render_template("dashboard.html", error="Please enter a word.")

    tables, words = get_tables()
    results = hashing_core.search_all_tables(tables, word)

    # Separate found vs not-found results to pick the fastest among found ones
    found_results = [r for r in results if r["found"]]
    not_found_results = [r for r in results if not r["found"]]

    # Fastest = lowest time_us among found results (or all results if none found)
    fastest = None
    if found_results:
        fastest = min(found_results, key=lambda r: r["time_us"])
    elif results:
        fastest = min(results, key=lambda r: r["time_us"])

    # Rebuild stats list for the dashboard (same as in /build)
    stats = []
    for info in tables:
        stats.append({
            "hash_name": info["hash_name"],
            "strategy_name": info["strategy_name"],
            "size": info["size"],
            "load_factor": info["load_factor"],
            "collisions": info["collisions"],
            "non_empty": info["non_empty"],
            "empty": info["empty"],
            "load_pct": round(info["load_factor"] * 100, 1)
        })

    return render_template(
        "dashboard.html",
        stats=stats,
        total_words=len(words),
        search_word=word,
        results=results,
        fastest=fastest
    )


if __name__ == "__main__":
    app.run(debug=True)
