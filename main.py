from flask import Flask, request, jsonify
import gdown
import os

app = Flask(__name__)

# Google Drive file IDs
FILES = {
    "restore.txt": "17WdBUX0l9iZEq4tMmz-HLOgyc0uSnBMs",
    "restore2.txt": "1H-e2zzFmE-qGBNlkNaKpzoNFSmQmnD7K",
    "restore3.txt": "1kURV0BXYtVjgnoxR6S0Uyn_6qbzI36XV",
    "restore4.txt": "1MHbOnL5GGcHRRI41QcMwhz6N-ad8Z2VL"
}

# Download files from Google Drive if they don't exist
for filename, file_id in FILES.items():
    if not os.path.exists(filename):
        url = f"https://drive.google.com/uc?id={file_id}"
        print(f"Downloading {filename} from Google Drive...")
        gdown.download(url, filename, quiet=False)

@app.route('/api/lookup/query', methods=['GET'])
def lookup_query():
    query = request.args.get('q')  # URL: ?q=1111
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400

    results = []

    for filename in FILES.keys():
        if not os.path.exists(filename):
            continue
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if query in line:
                    results.append({"file": filename, "line": line.strip()})
                    print(f"Found in {filename}: {line.strip()}")  # console output

    if not results:
        return jsonify({"message": "No results found"}), 404

    return jsonify(results)  # raw JSON response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
