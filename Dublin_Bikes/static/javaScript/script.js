   function myMap(){
    var mapProp= {
        center:new google.maps.LatLng(53.34745126358793,-6.259031293276394), zoom:13.5,
    };
    var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
    $.getJSON('/stations', null, function(data) {
        console.log("got json data")
        if ('stations' in data) {
            var stations = data.stations;
            //console.log(JSON.parse(JSON.stringify(stations)));
            _.forEach(stations, function(station) { 
                //console.log(station.name, station.number);
                var marker = new google.maps.Marker({ position : {
                           lat : station.lat,
                           lng : station.lng
                       },
                       map : map,
                       title : station.name,
                       station_number : station.number
                    });
                
                infowindow  = new google.maps.InfoWindow();
                marker.addListener("click", function() {
                    contentString = '<div id="content" class="stationInfoTitle"><h2 class="stationTitle">' + station.name + '</h2></div>'+ '<div id="station_availability" class="stationAvailabitlyInfo"></div>';
                    dynamicStationData()
                    infowindow.setContent(contentString);
                    infowindow.open(map, marker);
                    //drawStationCharts(this);
                    //drawStationChartsWeekly(this); });
                }) 
            })
    }})   
}

function dynamicStationData() {
    $.getJSON('/station_availability', null, function(data) {
        if ('stations' in data) {
            var stations = data.stations;
            _.forEach(stations, function(station) {
                contentString = "<ul class='bikeInfoList'><li>Available Bike Stands: " + station.available_bike_stands + "</li><li>Available Bikes: " + station.available_bikes + "</li><li>Banking Available: " + station.banking + "</li><li>Number of Bike Stands: " + station.bike_stands + "</li></ul>";
                document.getElementById("station_availability").innerHTML = contentString;
            })
        }
    })
}
        
myMap()

