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
                marker.addListener("click", function() {
//                    var stationNumber = station.number;
//                    console.log(stationNumber);
                    dynamicStationData(this);
                    drawStationCharts(this);
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
        }
    })
}

function drawStationCharts(marker){
    $.getJSON("/occupancy/" + marker.station_number, function (data) {
        
        data = JSON.parse(data.data); 
//        console.log('data', data);  
//        var x = document.getElementById('graphs');
//        if (x.style.display === "none") {
//            x.style.display = "block";
//        }
        
        var chart = new google.visualization.ColumnChart(document.getElementById('graphs'));
        
        var chart_data = new google.visualization.DataTable(); 
        chart_data.addColumn('datetime', 'Time of Day'); 
        chart_data.addColumn('number', '#');
        
        _.forEach(data, function (row) {
            chart_data.addRow([new Date(row[0]), row[1]]); 
        });
        
        var options = {
            title: 'Availability',
            colors: ['#9575cd', '#33ac71'],
            hAxis: {
                title: 'Time of Day', format: "E HH:mm", slantedText: true, slantedTextAngle: 30,
            }, 
            vAxis: {
                title: 'Average Number of Available Stands' }
            };
        
        chart.draw(chart_data, options);
        
    }).fail(function () {
        console.log("error"); 
    })
}

google.charts.load('current', {packages: ['corechart']});
google.charts.setOnLoadCallback(drawStationCharts);
myMap()

