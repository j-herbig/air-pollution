config = {
    'version': 'v1', 'config': {
    'visState': {
    'filters': [{
    'dataId': ['Sensors'], 'id': 'c717e9s', 'name': ['timestamp'], 'type': 'timeRange', 'value': [1577833200000, 1578006000000], 'enlarged': True, 'plotType': 'histogram', 'yAxis': None}], 'layers': [{
    'id': '2sqse6', 'type': 'hexagon', 'config': {
    'dataId': 'Sensors', 'label': 'Point', 'color': [179, 173, 158], 'columns': {
    'lat': 'lat', 'lng': 'lon'}, 'isVisible': True, 'visConfig': {
    'opacity': 0.8, 'worldUnitSize': 1, 'resolution': 8, 'colorRange': {
    'name': 'ColorBrewer RdYlGn-10', 'type': 'diverging', 'category': 'ColorBrewer', 'colors': ['#006837', '#1a9850', '#66bd63', '#a6d96a', '#d9ef8b', '#fee08b', '#fdae61', '#f46d43', '#d73027', '#a50026'], 'reversed': True}, 'coverage': 1, 'sizeRange': [0, 500], 'percentile': [0, 100], 'elevationPercentile': [0, 100], 'elevationScale': 5, 'colorAggregation': 'average', 'sizeAggregation': 'count', 'enable3d': False}, 'hidden': False, 'textLabel': [{
    'field': None, 'color': [255, 255, 255], 'size': 18, 'offset': [0, 0], 'anchor': 'start', 'alignment': 'center'}]}, 'visualChannels': {
    'colorField': {
    'name': 'PM2p5_bins', 'type': 'integer'}, 'colorScale': 'quantize', 'sizeField': None, 'sizeScale': 'linear'}}], 'interactionConfig': {
    'tooltip': {
    'fieldsToShow': {
    'Sensors': ['PM10', 'PM2p5', 'timestamp', 'PM2p5_bins']}, 'enabled': True}, 'brush': {
    'size': 0.5, 'enabled': False}, 'geocoder': {
    'enabled': False}, 'coordinate': {
    'enabled': False}}, 'layerBlending': 'normal', 'splitMaps': [], 'animationConfig': {
    'currentTime': None, 'speed': 1}}, 'mapState': {
    'bearing': 0, 'dragRotate': False, 'latitude': 50.07518289741276, 'longitude': 8.61378627731369, 'pitch': 0, 'zoom': 10.015695031198048, 'isSplit': False}, 'mapStyle': {
    'styleType': 'light', 'topLayerGroups': {

}, 'visibleLayerGroups': {
    'label': True, 'road': True, 'border': False, 'building': True, 'water': True, 'land': True, '3d building': False}, 'threeDBuildingColor': [9.665468314072013, 17.18305478057247, 31.1442867897876], 'mapStyles': {

}}}}