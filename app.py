from flask import Flask, request, render_template, redirect, url_for
from src.data_collection import fetch_articles, save_to_db, query_exists
from src.credibility_scoring import calculate_credibility

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        return redirect(url_for("results", query=query))
    return render_template("index.html")

@app.route("/results")
def results():
    query = request.args.get("query")
    if query_exists(query):
        message = f"'{query}' has already been searched. Fetching from database instead."
        return render_template("results.html", message=message, query=query, results=None)
    else:
        results = fetch_articles(query)
        if results:
            save_to_db(results, query)
            return render_template("results.html", message=None, query=query, results=results[:5])  # Show top 5 results
        else:
            return render_template("results.html", message="No results found.", query=query, results=None)

if __name__ == "__main__":
    app.run(debug=True)