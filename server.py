from flask import Flask, jsonify, send_file
from yargy import Parser

from notebook.common import TOKENIZER
from notebook.station_title import STATION_TITLE
from preprocess import fix_text
from structure import History, Message, Subway

app = Flask(__name__)


@app.route("/stations")
def check_rule():
    return send_file('static/stations/index.html')


@app.route("/api/stations", defaults={'offset': 0})
@app.route("/api/stations/<int:offset>")
def api_check_rule(offset: int):
    words = {w.lower() for _ in Subway.load().stations.keys() for w in _.split() if not w.isdigit()}
    parser = Parser(STATION_TITLE)


    def process(m: Message):
        text = fix_text(list(TOKENIZER(m.text)), words)
        matches = sorted(parser.findall(text), key=lambda _: _.span)
        return {
            "text":       text,
            "date":       m.date,
            "message_id": m.message_id,
            "spans":      [_.span for _ in matches],
            "stations":   [_.fact.value for _ in matches],
        }


    msgs = list(History.load().messages.values())
    return jsonify([process(m) for m in msgs[offset: offset + 10]])


@app.route("/")
def hello():
    return send_file('static/index.html')


@app.route('/subway')
def subway():
    return send_file('metro.json')


@app.route("/history")
def show_history():
    return jsonify({m.message_id: m._data for m in History.load().messages.values()})


@app.route("/history/<int:id>")
def show_msg(id: int):
    messages = History.load().messages
    msg = messages[id] if id in messages else {}
    return jsonify(msg._data)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    app.debug = True
    app.run('0.0.0.0', 8080)
