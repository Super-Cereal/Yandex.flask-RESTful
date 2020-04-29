from flask import Blueprint, jsonify
import base64
from requests import get


blueprint = Blueprint('yandex_api.py', __name__,
                      template_folder='templates')
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
static_map_api_server = "http://static-maps.yandex.ru/1.x/"
geocoder_apikey = "40d1649f-0493-4b70-98ba-98533de7710b"


@blueprint.route('/api/yamaps/<string:town>', methods=['GET'])
def get_map(town):
    geo_params = {
        'geocode': town,
        'apikey': geocoder_apikey,
        'format': 'json'
    }
    geo_response = get(geocoder_api_server, params=geo_params)
    try:
        ll = geo_response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    except Exception:
        return jsonify({'error': f"Error during query execution: {geo_response.url}"})
    map_params = {
        'll': ','.join(ll.split()),
        'l': 'sat',
        'z': 13,
        'size': '450,450'
    }
    map_response = get(static_map_api_server, params=map_params)
    if not map_response:
        return jsonify({'error': f"Error during query execution: {map_response.url}"})
    return recode_image(map_response.content)


def recode_image(byte_image):
    image = base64.b64encode(byte_image)
    return jsonify({'image': image.decode('utf-8')})
