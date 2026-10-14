import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")


def run_search(query, site, filetype):
    """Placeholder web search."""
    return [{
        "title": "Example result",
        "url": "https://example.com",
        "snippet": "This is a placeholder.",
    }]


def run_image_search(query, site, filetype):
    """Placeholder image search."""
    # Replace with a real image API later.
    return [
        {
            "title": f"{query or 'image'} {i}",
            "url":   f"https://picsum.photos/seed/{query or 'g'}{i}/400/300",
            "thumb": f"https://picsum.photos/seed/{query or 'g'}{i}/400/300",
            "source": "example.com",
        }
        for i in range(1, 10)
    ]


@app.route("/")
def index():
    return render_template("index.html", query="", site="", filetype="")


@app.route("/search")
def search():
    query    = request.args.get("q", "").strip()
    site     = request.args.get("as_sitesearch", "").strip()
    filetype = request.args.get("as_filetype", "").strip()

    lucky         = "btnI"  in request.args
    image_search  = "btnIS" in request.args

    if not query and not site and not filetype:
        return render_template(
            "index.html",
            error="Please enter a search term or fill in an advanced field",
            query=query, site=site, filetype=filetype,
        ), 400

    # --- Image search branch ---
    if image_search:
        images = run_image_search(query, site, filetype)
        return render_template(
            "imageResults.html",
            query=query,
            images=images,
        )

    results = run_search(query, site, filetype)

    if lucky and results:
        return redirect(results[0]["url"])

    return render_template(
        "searchResults.html",
        query=query,
        site=site,
        filetype=filetype,
        results=results,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug, host="0.0.0.0", port=port)
