from flask import Flask, request, Response, render_template, jsonify
import subprocess, json, requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/player")
def player():
    url = request.args.get("url")
    return render_template("player.html", url=url)

@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    headers = {}
    if "Range" in request.headers:
        headers["Range"] = request.headers["Range"]
    r = requests.get(url, headers=headers, stream=True)
    def generate():
        for chunk in r.iter_content(8192):
            yield chunk
    return Response(generate(), status=r.status_code, headers=dict(r.headers))

@app.route("/tracks")
def tracks():
    url = request.args.get("url")
    cmd = [
        "ffprobe",
        "-v","quiet",
        "-print_format","json",
        "-show_streams",
        url
    ]
    out = subprocess.check_output(cmd).decode()
    data = json.loads(out)
    audio=[]
    subs=[]
    for s in data["streams"]:
        if s["codec_type"]=="audio":
            audio.append({
                "index":s["index"],
                "lang":s.get("tags",{}).get("language","unknown")
            })
        if s["codec_type"]=="subtitle":
            subs.append({
                "index":s["index"],
                "lang":s.get("tags",{}).get("language","unknown")
            })
    return jsonify({"audio":audio,"subs":subs})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8000)