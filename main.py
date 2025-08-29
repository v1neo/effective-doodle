from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# List of files to search
FILES = ["restore.txt", "restore2.txt", "restore3.txt", "restore4.txt"]

@app.route('/api/lookup/query', methods=['GET'])
def lookup_query():
    query = request.args.get('q')  # URL: ?q=1111
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    results = []

    for filename in FILES:
        if not os.path.exists(filename):
            continue  # skip missing files
        with open(filename, 'r') as f:
            for line in f:
                if query in line:
                    results.append({"file": filename, "line": line.strip()})
                    print(f"Found in {filename}: {line.strip()}")  # output to console

    if not results:
        return jsonify({"message": "No results found"}), 404

    return jsonify(results)  # return raw JSON

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
