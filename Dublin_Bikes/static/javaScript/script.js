   function myMap(){
    var mapProp= {
        center:new google.maps.LatLng(53.34745126358793,-6.259031293276394), zoom:13,
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
                    drawAvailableBikeStands(this);
                    drawAvailableBikes(this);
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
            if (dynamicData[0].banking == 0){
                    var banking = "No"
                }
                else{
                    var banking = "Yes"
                }
            ;
            var contentString = '<div id="content" class="stationInfoTitle"><h2 class="stationTitle">' + marker.title + '</h2><ul class="bikeInfo"><li>Available Bike Stands: ' + dynamicData[0].available_bike_stands + '</li><li>Available Bikes: ' + dynamicData[0].available_bikes + '</li><li>Banking Available: ' + banking + '</li><li>Number of Bike Stands: ' + dynamicData[0].bike_stands + '</li></ul></div>;';
            infowindow.setContent(contentString);
            infowindow.open(marker.map, marker);
        }
    })
}

function drawAvailableBikeStands(marker){
    $.getJSON("/occupancyOfAvailableBikeStands/" + marker.station_number, function (data) {
        
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
            title: 'Available Stands by Day',
            colors: ['#ffe038', '#33ac71'],
            hAxis: {
                title: 'Time of Day', format: "E HH:mm", slantedText: true, slantedTextAngle: 30,
            }, 
            vAxis: {
                title: 'Available Stands' }
            };
        
        chart.draw(chart_data, options);
        document.getElementById('googleMap').style.height = "60%";
        
    }).fail(function () {
        console.log("error"); 
    })
}

function drawAvailableBikes(marker){
    $.getJSON("/occupancyOfAvailableBikesByHour/" + marker.station_number, function (data) {
        
        data = JSON.parse(data.data); 
//        console.log('data', data);  
//        var x = document.getElementById('graphs');
//        if (x.style.display === "none") {
//            x.style.display = "block";
//        }
        
        var chart = new google.visualization.ColumnChart(document.getElementById('graphs2'));
        
        var chart_data = new google.visualization.DataTable(); 
        chart_data.addColumn('datetime', 'Time of Day'); 
        chart_data.addColumn('number', '#');
        
        _.forEach(data, function (row) {
            chart_data.addRow([new Date(row[0]), row[1]]); 
        });
        
        var options = {
            title: 'Available Bikes by Day',
            colors: ['#9575cd', '#33ac71'],
            hAxis: {
                title: 'Time of Day', format: "E HH:mm", slantedText: true, slantedTextAngle: 30,
            }, 
            vAxis: {
                title: 'Available Bikes' }
            };
        
        chart.draw(chart_data, options);
        document.getElementById('chartsDiv').style.display = "inline-block";
        
    }).fail(function () {
        console.log("error"); 
    })
}

function closeCharts() {
    var x = document.getElementById("chartsDiv");
    if (x.style.display === "none") {
        x.style.display = "inline-block";
    } else {
        x.style.display = "none";
        document.getElementById('googleMap').style.height = "100%";
    }
}

google.charts.load('current', {packages: ['corechart']});
google.charts.setOnLoadCallback(myMap);