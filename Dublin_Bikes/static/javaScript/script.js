   function myMap(){
    var mapProp= {
        center:new google.maps.LatLng(53.34745126358793,-6.259031293276394), zoom:13.5,
    };
    var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
    $.getJSON('/stations', null, function(data) {
        console.log("got json data", data)
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
                
//                infowindow  = new google.maps.InfoWindow();
//                contentString = '<div id="content" class="stationInfoTitle"><h2 class="stationTitle">' + station.name + '</h2></div>'+ '<div id='+ station.number +' class="stationAvailabitlyInfo"></div>';
//                infowindow.setContent(contentString);
                marker.addListener("click", function() {
//                    var stationNumber = station.number;
//                    console.log(stationNumber);
                    dynamicStationData(this);
                    
                    //drawStationCharts(this);
                    //drawStationChartsWeekly(this); });
                }) 
            })
    }})   
}

function dynamicStationData(marker) {
//    console.log('get station data', marker);
    $.getJSON('/station_availability/' + marker.station_number, null, function(data) {
        if ('stations' in data) {
            var dynamicData = data.stations
            var infowindow  = new google.maps.InfoWindow();
            var contentString = '<div id="content" class="stationInfoTitle"><h2 class="stationTitle">' + marker.title + '</h2><ul class="bikeInfo"><li>Available Bike Stands: ' + dynamicData[0].available_bike_stands + '</li><li>Available Bikes: ' + dynamicData[0].available_bikes + '</li><li>Banking Available: ' + dynamicData[0].banking + '</li><li>Number of Bike Stands: ' + dynamicData[0].bike_stands + '</li></ul></div>;';
            infowindow.setContent(contentString);
            infowindow.open(marker.map, marker);
            
            
//            
//            _.forEach(stations, function(station) {
//                console.log(station.available_bike_stands, station.available_bikes);
//                console.log(stationNumber);
//                contentString = "<ul class='bikeInfoList'><li>Available Bike Stands: " + station.available_bike_stands + "</li><li>Available Bikes: " + station.available_bikes + "</li><li>Banking Available: " + station.banking + "</li><li>Number of Bike Stands: " + station.bike_stands + "</li></ul>";
//                document.getElementById(station.number).innerHTML = contentString;
//            })
        }
    })
}
        
myMap()

