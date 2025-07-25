from flask import Flask, render_template, jsonify
from hdfs import InsecureClient
import json
from collections import Counter

app = Flask(__name__)

# Configuración del HDFS
HDFS_HOST = "http://master:9870"
HDFS_USER = "cluster"
HDFS_PATH = "/user/cluster/song_data/"
client = InsecureClient(HDFS_HOST, user=HDFS_USER)


def get_latest_data():
    # Obtener la carpeta más reciente
    folders = sorted(client.list(HDFS_PATH))
    latest_folder = folders[-1]
    latest_path = HDFS_PATH + latest_folder
    print(f"Carpeta más reciente: {latest_path}")

    data = []
    for dirpath, _, files in client.walk(latest_path):
        for f in files:
            file_path = f"{dirpath}/{f}"
            print(f"Leyendo archivo: {file_path}")
            with client.read(file_path) as reader:
                for line in reader:
                    try:
                        line = line.strip()
                        if line:  # Evitar líneas vacías
                            data.append(json.loads(line))
                    except json.JSONDecodeError as e:
                        print(f"Error al parsear línea en {file_path}: {e}")
    print(f"Total registros leídos: {len(data)}")
    return data



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    songs = get_latest_data()
    return jsonify(songs)

@app.route('/top10')
def top10():
    songs = get_latest_data()
    if not songs:
        return jsonify([])

    # Contar reproducciones por título
    counter = Counter([s['title'] for s in songs])
    top10_songs = counter.most_common(10)

    # Crear estructura de respuesta
    top10_data = []
    for title, count in top10_songs:
        song_info = next(s for s in songs if s['title'] == title)
        top10_data.append({
            "title": title,
            "artist": song_info["artist"],
            "count": count
        })

    return jsonify(top10_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
