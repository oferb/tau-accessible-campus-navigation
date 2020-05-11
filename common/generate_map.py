base_map = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Route</title>
    <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=geometry&key=AIzaSyB1WaJbnBJD_lCEP4VF3VX3CGH-u-ncOKU"></script>
    <script src="maplabel-compiled.js"></script>
    <style>
        html,
        body,
        #map_canvas {
          height: 100%;
          width: 100%;
          margin: 0px;
          padding: 0px
        }
    </style>
</head>
<body>
<div id="map_canvas"></div>
</body>
<script type="application/javascript">
    var colors = [];
    function initialize() {
      var map = new google.maps.Map(
        document.getElementById("map_canvas"), {
          zoom: 13,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });
      var bounds = new google.maps.LatLngBounds();
      MAP_BODY
      map.fitBounds(bounds);
    }
    google.maps.event.addDomListener(window, "load", initialize);
</script>
</html>"""
def points_to_js_struct(points):
    points = [p[:2] if len(p) == 3 else p for p in points]
    return '[%s]' % ','.join(["new google.maps.LatLng(%s,%s)" % p for p in points])
def render_routes(routes):
    routes_text = '[%s]' % ','.join([points_to_js_struct(route) for route in routes])
    routes_js = """steps = %s;
    for (var j=0;j<steps.length;j++){
          var line = new google.maps.Polyline({
            path: steps[j],
            geodesic: true,
            strokeColor: colors[j],
            strokeOpacity: 0.3,
            strokeWeight: 5,
            map: map});
    }
    for (var j=0;j<steps.length;j++){
    for (var i=0;i<steps[j].length;i++){
    bounds.extend(steps[j][i]);
    }
    }
    """ % routes_text
    return routes_js
def generate_map(route, path):
    content = render_routes(route)
    map = base_map.replace('MAP_BODY', content)
    f = open(path, 'w')
    f.write(map)
    f.close()

route_1 = [
    (32.11326248462344, 34.80252070379018),
    (32.11324650601604, 34.8030463299894),
    (32.113237, 34.803391),
    (32.113155 , 34.803864),
    (32.11315444, 34.80391873),
    (32.11309553, 34.80463961),
    (32.11305329803146, 34.80479855126322),
    (32.11310229731222, 34.8053959650141),
    (32.11311050929496, 34.80573731502611),
    (32.11311050929496, 34.80573731502611)
]
route_2 = [
    (32.1121983,34.804422),
    (32.1121601,34.804376),
    (32.111836,34.8044022),
    (32.1117469,34.8045092),
    (32.1117317,34.8048604),
    (32.1117473,34.8049392),
    (32.1115985,34.8049684),
    (32.1115448,34.805091),
    (32.1115447,34.8051871),
    (32.1114257,34.8052931)
]
generate_map([route_1,route_2], "test.html")