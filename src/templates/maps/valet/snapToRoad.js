// draw colored polylines to indicate parking hour limit in areas

        var limitedParkingCoordinates = output.prkg_section.coordinates;
        console.log(limitedParkingCoordinates);

        runSnapToRoad(limitedParkingCoordinates);

        function runSnapToRoad(path) {
          var pathValues = [];
          for (var i = 0; i < path.length; i++) {
            var coord = path[i].lat + ',' + path[i].lng;
            //console.log(coord);
            pathValues.push(coord);

          }

          console.log(pathValues.join('|'));

          $.get('https://roads.googleapis.com/v1/snapToRoads', {
            interpolate: true,
            key: apiKey,
            path: pathValues.join('|')
          }, function(data) {
            processSnapToRoadResponse(data);
            drawSnappedPolyline();

          });
        }

        // Store snapped polyline returned by the snap-to-road method.
        function processSnapToRoadResponse(data) {
          snappedCoordinates = [];
          placeIdArray = [];
          for (var i = 0; i < data.snappedPoints.length; i++) {
            var latlng = new google.maps.LatLng(
                data.snappedPoints[i].location.latitude,
                data.snappedPoints[i].location.longitude);
            snappedCoordinates.push(latlng);
            placeIdArray.push(data.snappedPoints[i].placeId);
          }
        }

        // Draws the snapped polyline (after processing snap-to-road response).
        function drawSnappedPolyline() {
          var snappedPolyline = new google.maps.Polyline({
            path: snappedCoordinates,
            strokeColor: 'black',
            strokeWeight: 3
          });

          snappedPolyline.setMap(map);
          polylines.push(snappedPolyline);
        }