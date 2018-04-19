function myMap() {

    var mapProp = {
        center: new google.maps.LatLng(53.34745126358793, -6.259031293276394), 
        zoom: 13.8,
    };
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);

        directionsService = new google.maps.DirectionsService, //allows directions to be shown
        directionsDisplay = new google.maps.DirectionsRenderer({ //displays the directions
            map: map,
            panel: document.getElementById('directions'), //this is div where directions will be diaplyed 
            preserveViewport: true //prevents zoom out when directions started
        });


    // Try HTML5 geolocation.
    if (navigator.geolocation) { //if the user has enabled geolocation
        navigator.geolocation.getCurrentPosition(function(position) { //gets their current position
            user_pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

            var icon = {
                url:"https://png.icons8.com/windows/1600/map-pin.png",
                //url: "https://lh4.ggpht.com/Tr5sntMif9qOPrKV_UVl7K8A_V3xQDgA7Sw_qweLUFlg76d_vGFA7q1xIKZ6IcmeGqg=w300",
                scaledSize: new google.maps.Size(60, 60), //icon to display their current location
            };

            //shows the icon on the map where the user is.
            info_Window = new google.maps.Marker({
                position: user_pos,
                map: map,
                icon: icon,
            });

        }, function() {
            handleLocationError(true, info_Window, map.getCenter());
            show_direction_button = false; //set to false if geolocation not enables. means user wont have option to select directions
        });
    } else {

        // Browser doesn't support Geolocation
        handleLocationError(false, info_Window, map.getCenter());
    }

    function handleLocationError(browserHasGeolocation, info_Window, user_pos) {
        document.getElementById('directions').innerHTML = 'Sorry in order to use this feature you need to allow access to your geolocation.\nPlease change this in your browser settings and try again.';
    }
    
    
    
    


    //calls get stations method in views which returns the data in json format
    $.getJSON('/stations', null, function(data) {
        console.log("got json data", data)
        
        //code to fill drop down menu for stations
        var i;
        var stationHTML = "";
        for (i = 0; i < data.stations.length; i++) {
            stationHTML += "<option value="+data.stations[i].number+">"+data.stations[i].name+"</option>";
        }
        document.getElementById("predictionStation").innerHTML=stationHTML;
        makeDayDropdown();

        //Different markers to indicate stations with more available bikes
        var icon = {
            url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
        };
        var icon1 = {
            url: "http://maps.google.com/mapfiles/ms/icons/orange-dot.png",
        };
        var icon2 = {
            url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
        };
        

        if ('stations' in data) {
            var stations = data.stations;
            _.forEach(stations, function(station) {

                //if bike has less than 10 bikes in its station then the markre will be red
                if (station.available_bikes <= 1) {
                    var marker = new google.maps.Marker({
                        position: {
                            lat: station.lat,
                            lng: station.lng
                        },
                        map: map,
                        title: station.name,
                        station_number: station.number,
                        icon: icon

                    });

                }
                
                else if (station.available_bikes < 10 ){
                    var marker = new google.maps.Marker({
                        position: {
                            lat: station.lat,
                            lng: station.lng
                        },
                        map: map,
                        title: station.name,
                        station_number: station.number,
                        icon: icon1
                });
            }
                        
                //otherwise it will be green 
                else {
                    var marker = new google.maps.Marker({
                        position: {
                            lat: station.lat,
                            lng: station.lng
                        },
                        map: map,
                        title: station.name,
                        station_number: station.number,
                        icon: icon2

                    });

                }
                //add the markers to the markers_Array(stores the objects)
                marker_array.push(marker); 
                
                //as I add makers to the array it gives its index by the length of the current array -1. ie the first station has index 0
                options += '<a href="javascript:myclick(' + (marker_array.length-1) + ')">' + station.name + '<\/a><br>';

               
        //adding a listerner funtion the markers. will activate another function on click
        marker.addListener("click", function() {
                    
                    //the code below is executed when the marker is clicked.
                    document.getElementById('directions').style.display = 'none';
                    directionsDisplay.setMap(null); //hiding blue directions line if its already there
                    directionsDisplay.setPanel(null); //hide directions list if alreay there    
                    //map.setZoom(15); //zoom in on marker when clicked
                    //map.setCenter(marker.getPosition()); //map zoom supon click
                    
                    
                    //if the marker has an animation then stop it 
                    if (marker.getAnimation() != null) {
                        marker.setAnimation(null);
                      } 
                    //otherwise make it bounce
                    else {
                        marker.setAnimation(google.maps.Animation.BOUNCE);
                      }
                    
                    //timer for the marker bounce
                    setTimeout(function() {
                        marker.setAnimation(null)
                    }, 3000);
                    
                    
                //calling the dynamic static data with the current marker 
                dynamicStationData(this);
                    var x = document.getElementById("day");
                    var z = document.getElementById("hour");
                    
                     if ( x.classList.contains('active') ){
                        drawAvailableBikeStandsDaily(this);
                        drawAvailableBikesDaily(this);
                    }
                    else if ( z.classList.contains('active') ){
                        drawAvailableBikeStandsHourly(this);
                        drawAvailableBikesHourly(this);
                    }
                    
                })
            })

        }           
        //this fills the div that contains the list of stations(div appears with click of a button)
        document.getElementById("stations_text").innerHTML = options;

    })

}



//ajax function that displays the prediction of number of bikes
$(document).ready(function() {
    $('#submit_button').click(function(event) {
        $.ajax({
            
            data: ({
                days : $('#days').val(),
                time : $('#time').val(),
                predictionStation : $('#predictionStation').val()   
            }),
            type : 'POST',
            url : '/modelPredictions'
        }).done(function(result) {
            if (result.error){
                console.log("error")

            }
            else{
                document.getElementById('result_container').style = "inline-block";
                document.getElementById('result').innerHTML = result;

            }});

        event.preventDefault();
        });
        });








function makeDayDropdown(){
    $.getJSON('/forcast', null, function(data){
        var drop_days = "";
            for (i = 0; i < data.days.length; i++) {
            drop_days += "<option value="+data.days[i].day_num+">"+data.days[i].day+"</option>";
        }
        document.getElementById("days").innerHTML=drop_days;
    }
)}



//when the station name in the drop down is clicked this function is called and it triggers the click of a marker
function myclick(i) {
  google.maps.event.trigger(marker_array[i], "click");
}






//this function shows the list of the stations in the drop down when the stations button is clicked
function showStationsList(){
    
    if (stations_window){
        document.getElementById('stations_list').style.display = 'none';
        document.getElementById('googleMap').style.width = '100%';
        stations_window = false;
    }
    else{
            document.getElementById('directions').style.display = 'none';
            document.getElementById('googleMap').style.width = '85%';
            document.getElementById('stations_list').style.display = 'inline-block';
            stations_window = true;
    }
}





//function to create info window for markers
function dynamicStationData(marker) {
    $.getJSON('/station_availability/' + marker.station_number, null, function(data) {
                
                //closes info_window if open when clicking on a new marker
                if (prev_info_window) {
                    prev_info_window.close()
                }
        
                //closes directions div if open when clicking on a new marker
        //need to fix this diections div but im going to bed ///////////////////////////////////////////////////////////////////////////////////////////////////////////
                if (directionsWindow && !stations_window) { 
                    document.getElementById('directions').style.display = 'none';
                    document.getElementById('googleMap').style.width = '100%';
                }
        

        if ('stations' in data) {
            var dynamicData = data.stations
            var infowindow = new google.maps.InfoWindow();
            prev_info_window = infowindow; //this is needed so the info window can be closed above.


            // We have a scraper issue atm. Will be fixed by tuesday
            //this code changes the banking to no or yes
            if (dynamicData[0].banking == 0) {
                var banking = "No";

            } else {
                var banking = "Yes";

            };
            
            //
            var contentString = '<div id="content" class="stationInfoTitle"><h2 class="stationTitle">' + marker.title + '</h2><ul class="bikeInfo"><li>Available Bike Stands: ' + dynamicData[0].available_bike_stands + '</li><li>Available Bikes: ' + dynamicData[0].available_bikes + '</li><li>Banking Available: ' + banking + '</li><li>Number of Bike Stands: ' + dynamicData[0].bike_stands + '</li><li><div id="geo"><input type="button" id="nodeGoto" value="Click Here for Directions"/></div></li></ul></div>';
            
            
            
            //only shows the directions button if the user has enabled geolocation.
            infowindow.setContent(contentString);
            infowindow.open(marker.map, marker);
            
                if (show_direction_button != false) { //global variable
                document.getElementById('geo').style.display = 'inline-block';
            }


            // this can only happen if the button div is displayed (geolocation enabled)
            document.getElementById("nodeGoto").addEventListener("click", function() {
                document.getElementById('stations_list').style.display = 'none';
                stations_window = false;
                document.getElementById('googleMap').style.width = '65%';
                document.getElementById('directions').style.display = 'inline-block';
                directionsWindow = true;
                Directions(marker);

            });
        }
    })
}






function Directions(m) {

    var pointB = m.getPosition(), //this gets the lat and long of the current marker that was clicked on
        pointA = user_pos; //this is the users current location

    //these two lines show the directions and blue line when the show directions is clicked. They have been hiden when the marker is first clicked
    directionsDisplay.setMap(map);
    directionsDisplay.setPanel(document.getElementById('directions'));

    //function to calculate the directions between the two points
    calculateAndDisplayRoute(directionsService, directionsDisplay, pointA, pointB);

    function calculateAndDisplayRoute(directionsService, directionsDisplay, user_pos, marker) {
        directionsService.route({
            origin: user_pos,
            destination: marker,
            avoidTolls: false,
            avoidHighways: false,
            travelMode: google.maps.TravelMode.DRIVING
        }, function(response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                directionsDisplay.setDirections(response);
            } else {
                window.alert('Directions request failed due to ' + status);
            }
        });
    }
}





//function to draw chart
function drawAvailableBikeStandsDaily(marker) {
    $.getJSON("/occupancyOfAvailableBikeStandsDaily/" + marker.station_number, function(data) {

        data = JSON.parse(data.data);
        //        console.log('data', data);  
        //        var x = document.getElementById('graphs');
        //        if (x.style.display === "none") {
        //            x.style.display = "block";
        //        }

        var chart = new google.visualization.LineChart(document.getElementById('graphs'));

        var chart_data = new google.visualization.DataTable();
        chart_data.addColumn('datetime', 'Time of Day');
        chart_data.addColumn('number', '#');

        _.forEach(data, function(row) {
            chart_data.addRow([new Date(row[0]), row[1]]);
        });

        var options = {
            title: 'Available Stands by Day',
            colors: ['#ffe038', '#33ac71'],
            hAxis: {
                title: 'Day',
                format: "E",
                slantedText: true,
                slantedTextAngle: 30,
            },
            vAxis: {
                title: 'Available Stands'
            }
        };

        chart.draw(chart_data, options);
        document.getElementById('googleMap').style.height = "100%";

    }).fail(function() {
        console.log("error");
    })
}




//function to draw chart
function drawAvailableBikeStandsHourly(marker) {
    $.getJSON("/occupancyOfAvailableBikeStandsHourly/" + marker.station_number, function(data) {

        data = JSON.parse(data.data);
        //        console.log('data', data);  
        //        var x = document.getElementById('graphs');
        //        if (x.style.display === "none") {
        //            x.style.display = "block";
        //        }

        var chart = new google.visualization.LineChart(document.getElementById('graphs'));

        var chart_data = new google.visualization.DataTable();
        chart_data.addColumn('datetime', 'Time of Day');
        chart_data.addColumn('number', '#');

        _.forEach(data, function(row) {
            chart_data.addRow([new Date(row[0]), row[1]]);
        });

        var options = {
            title: 'Available Stands by Hour',
            colors: ['#ffe038', '#33ac71'],
            hAxis: {
                title: 'Time of Day',
                format: "E HH:mm",
                slantedText: true,
                slantedTextAngle: 30,
            },
            vAxis: {
                title: 'Available Stands'
            }
        };

        chart.draw(chart_data, options);
        document.getElementById('googleMap').style.height = "100%";

    }).fail(function() {
        console.log("error");
    })
}






//function to draw chart
function drawAvailableBikesDaily(marker) {
    $.getJSON("/occupancyOfAvailableBikesDaily/" + marker.station_number, function(data) {

        data = JSON.parse(data.data);
        //        console.log('data', data);  
        //        var x = document.getElementById('graphs');
        //        if (x.style.display === "none") {
        //            x.style.display = "block";
        //        }

        var chart = new google.visualization.LineChart(document.getElementById('graphs2'));

        var chart_data = new google.visualization.DataTable();
        chart_data.addColumn('datetime', 'Time of Day');
        chart_data.addColumn('number', '#');

        _.forEach(data, function(row) {
            chart_data.addRow([new Date(row[0]), row[1]]);
        });

        var options = {
            title: 'Available Bikes by Day',
            colors: ['#9575cd', '#33ac71'],
            hAxis: {
                title: 'Day',
                format: "E",
                slantedText: true,
                slantedTextAngle: 30,
            },
            vAxis: {
                title: 'Available Bikes'
            }
        };

        chart.draw(chart_data, options);
        document.getElementById('chartsDiv').style.display = "inline-block";

    }).fail(function() {
        console.log("error");
    })
}





//function to draw chart
function drawAvailableBikesHourly(marker) {
    $.getJSON("/occupancyOfAvailableBikesHourly/" + marker.station_number, function(data) {

        data = JSON.parse(data.data);
        //        console.log('data', data);  
        //        var x = document.getElementById('graphs');
        //        if (x.style.display === "none") {
        //            x.style.display = "block";
        //        }

        var chart = new google.visualization.LineChart(document.getElementById('graphs2'));

        var chart_data = new google.visualization.DataTable();
        chart_data.addColumn('datetime', 'Time of Day');
        chart_data.addColumn('number', '#');

        _.forEach(data, function(row) {
            chart_data.addRow([new Date(row[0]), row[1]]);
        });

        var options = {
            title: 'Available Bikes by Hour',
            colors: ['#9575cd', '#33ac71'],
            hAxis: {
                title: 'Time of Day',
                format: "E HH:mm",
                slantedText: true,
                slantedTextAngle: 30,
            },
            vAxis: {
                title: 'Available Bikes'
            }
        };

        chart.draw(chart_data, options);
        document.getElementById('chartsDiv').style.display = "inline-block";

    }).fail(function() {
        console.log("error");
    })
}






//function to close charts div
function closeCharts() {
    var x = document.getElementById("chartsDiv");
    if (x.style.display === "none") {
        x.style.display = "inline-block";
    } else {
        x.style.display = "none";
        document.getElementById('googleMap').style.height = "100%";
    }
}





//function to display information message upon loading page
function codeAddress() {
    alert('Welcome to DublinBikes. This web application is designed to provde you with real time information on DublinBikes, such as, the current number of bikes at a given station and the number of available bike stands at a station. We also provie you with predictions for the number of bikes available for a given day. Enjoy.\n\n To continue please hit CLOSE below ');
}






//function to display weather information
function weather() {
    //console.log("Entered weather function")
    $.getJSON("/weather", null, function(data) {
        if ('weather' in data) {
            var weather = data.weather
        }
        _.forEach(weather, function(weather) {
            
            var weatherInfo = "<table id ='weather_table'>";
            var tempMax_temp = weather.temp_max;
            var tempMax_float = tempMax_temp - 273.15; //calculates temp in celsius
            var tempMax = Math.round(tempMax_float);
            var tempMin_temp = weather.temp_min;
            var tempMin_float = tempMin_temp - 273.15; //calculates temp in celsius
            var tempMin = Math.round(tempMin_float);
            var Descrip = weather.description;
            var iconCode = weather.icon;
            var humidity = weather.humidity;

            
        weatherInfo += "<tr><td>" + "<img src='http://openweathermap.org/img/w/" + iconCode + ".png'>" + "</td><td>" + Descrip + "</td><td>Max Temp:" + tempMax + '°C' + "</td><td>Min Temp:" + tempMin + '°C' + "</td><td>Humidty: " + humidity + "%</td></tr>";

        weatherInfo += "</table>";  
        document.getElementById("weather").innerHTML = weatherInfo;

        })
    })
}




function displayWeather(){
    var x = document.getElementById("weather");
    if (toggleWeather == false){
        x.style.display="flex";
        toggleWeather = true;
        
    }
    else{
        x.style.display="none";
        toggleWeather = false;
    }
}




function toggleMyNavBar(){
    var x = document.getElementById("myNav");
    if (x.style.display==="none"){
        x.style.display="flex";
    }
    else{
        x.style.display="none";
        
    }
}



function changeToDayView(){
    var x = document.getElementById("day");
    var y = document.getElementById("predict");
    var z = document.getElementById("hour");
    
    if ( x.classList.contains('deactive') ){
        x.classList.remove('deactive');
        x.classList.add('active');
    }
    
    if ( y.classList.contains('active') ){
        y.classList.remove('active');
        y.classList.add('deactive');
        document.getElementById("predictions").style.display="none";
    }
    
    if ( z.classList.contains('active') ){
        z.classList.remove('active');
        z.classList.add('deactive');
    }
    
}




function changeToHourView(){
    var y = document.getElementById("day");
    var z = document.getElementById("predict");
    var x = document.getElementById("hour");
    
    if ( x.classList.contains('deactive') ){
        x.classList.remove('deactive');
        x.classList.add('active');
    }
    
    if ( y.classList.contains('active') ){
        y.classList.remove('active');
        y.classList.add('deactive');
    }
    
     if ( z.classList.contains('active') ){
        z.classList.remove('active');
        z.classList.add('deactive');
        document.getElementById("predictions").style.display="none";
    }
    
}




function changeToPredictionView(){
    var y = document.getElementById("day");
    var x = document.getElementById("predict");
    var z = document.getElementById("hour");
    
    if ( x.classList.contains('deactive') ){
        x.classList.remove('deactive');
        x.classList.add('active');
        document.getElementById("predictions").style.display="block";
    }
    
    if ( y.classList.contains('active') ){
        y.classList.remove('active');
        y.classList.add('deactive');
    }
    
    if ( z.classList.contains('active') ){
        z.classList.remove('active');
        z.classList.add('deactive');
    }
    
}


function displayPredictions(value) {
    if (value == null){
    }
    else{
        alert(value)
    }
}



//Function to create map and lister on markers to call functions to draw charts
var toggleWeather =false;
var stations_window = false; //stations window
var user_pos; //varible to hold users geolocaiton
var info_Window;
var map; //map varible
var show_direction_button; //used to indicate if user has enabled geolocation or not.
var marker_array=[]; //array used to store all the marker objects
var options = ""; // this is used to created the stations list 
var prev_info_window = false;//used to toggle open/close info_window when clicking on different markers
var directionsWindow = false;//used to toggle open/close directions when clicking on different markers

window.onload = codeAddress;

weather()

//var toggle = document.getElementById('toggle');
//toggle.onclick = displayWeather;
//Updates weather info over time
setInterval(function() {
    weather()
}, 1800000)

//Loads google charts library
google.charts.load('current', {
    packages: ['corechart']
});
//When google charts library is loaded my map function is called
google.charts.setOnLoadCallback(myMap);