   function myMap(){
    var mapProp= {
        center:new google.maps.LatLng(53.34745126358793,-6.259031293276394), zoom:11,
    };
    var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
    $.getJSON('/stations', null, function(data) {
        console.log("got json data")
        if ('stations' in data) {
            var stations = data.stations;
            console.log(JSON.parse(JSON.stringify(stations)));
            _.forEach(stations, function(station) { 
                console.log(station.name, station.number);
                var marker = new google.maps.Marker({ position : {
                           lat : station.lat,
                           lng : station.lng
                       },
                       map : map,
                       title : station.name,
                       station_number : station.number
                    });
                //marker.addListener("click", function() {
                    //drawStationCharts(this);
                    //drawStationChartsWeekly(this); });
            }) }
    });
}

myMap()