from flask import Flask, request, Response, render_template
import requests

app = Flask(__name__)

session = requests.Session()

# ================= HOME PAGE =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= PLAYER =================

@app.route("/player")
def player():
    url = request.args.get("url")
    return render_template("player.html", url=url)


# ================= SMART PROXY =================

@app.route("/proxy")
def proxy():

    url = request.args.get("url")

    range_header = request.headers.get("Range")

    headers = {}

    if range_header:
        headers["Range"] = range_header

    r = session.get(url, headers=headers, stream=True)

    def generate():
        for chunk in r.iter_content(1024*512):
            if chunk:
                yield chunk

    response = Response(
        generate(),
        status=r.status_code,
        content_type=r.headers.get("Content-Type")
    )

    if "Content-Range" in r.headers:
        response.headers["Content-Range"] = r.headers["Content-Range"]

    if "Accept-Ranges" in r.headers:
        response.headers["Accept-Ranges"] = "bytes"

    if "Content-Length" in r.headers:
        response.headers["Content-Length"] = r.headers["Content-Length"]

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
