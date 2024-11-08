from flask import Flask, request, jsonify, send_from_directory
import uuid
from pyroutelib3 import router
import folium
import os

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('', 'index.html')

@app.route('/generate_map', methods=['POST'])
def generate_map():
    data = request.json
    transport_mode = data.get("transport", "car")
    loc_depart = data["loc"]["depart"]
    loc_arrivee = data["loc"]["arrivee"]
    
    depart_lat = loc_depart["lat"]
    depart_lon = loc_depart["lon"]
    arrivee_lat = loc_arrivee["lat"]
    arrivee_lon = loc_arrivee["lon"]

    route = router(transport_mode)

    depart = route.findNode(depart_lat, depart_lon)
    arrivee = route.findNode(arrivee_lat, arrivee_lon)

    status, chemin = route.doRoute(depart, arrivee)

    if status == 'success':
        routeLatLons = list(map(router.nodeLatLon, chemin))

        map_center = [(depart_lat + arrivee_lat) / 2, (depart_lon + arrivee_lon) / 2]
        c = folium.Map(location=map_center, zoom_start=15)

        folium.PolyLine(routeLatLons, color="blue", weight=2.5, opacity=1).add_to(c)

        folium.Marker([depart_lat, depart_lon], popup="Départ").add_to(c)
        folium.Marker([arrivee_lat, arrivee_lon], popup="Arrivée").add_to(c)

        map_uuid = str(uuid.uuid4())

        os.makedirs("maps", exist_ok=True)
        c.save(os.path.join("maps", f"{map_uuid}.html"))

        return jsonify({"status": "success", "url": f"/maps/{map_uuid}"})
    else:
        return jsonify({"status": "error", "message": "Erreur lors du calcul de l'itinéraire"}), 400

@app.route('/maps/<filename>')
def get_map(filename):
    return send_from_directory('maps', filename + '.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)