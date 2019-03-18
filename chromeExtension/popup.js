var bg = chrome.extension.getBackgroundPage();
var latitude;
var longitude;
var city;


//getting user's location using HTML5 geolocation
navigator.geolocation.getCurrentPosition(function (pos, error) {

    if (!navigator.geolocation) throw "geolocation not support";
    while(typeof(bg.citySelectedStore) == "undefined")
    {
    }
    city = bg.citySelectedStore;
    if (city == "") {
        //get latitude and longitude.
        bg.latitude = pos.coords.latitude;
        bg.longitude = pos.coords.longitude;
        latitude = bg.latitude;
        longitude = bg.longitude;
        //using google map API getting user's city name by latitude and longitude
        var geocodingAPI = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + latitude + "," + longitude + "&key=AIzaSyCUe-myHsErw9OjBwB7mIqlo4FzYX-qzkw";
        $.getJSON(geocodingAPI, function (json) {
            //check if the return json file is alright.
            if (json.status == "OK") {
                //Check result 0
                var result = json.results[0];
                //look for locality tag and administrative_area_level_1
                city = "";
                //search for city name
                for (var i = 0, len = result.address_components.length; i < len; i++) {
                    var ac = result.address_components[i];
                    if (ac.types.indexOf("administrative_area_level_1") >= 0) { city = ac.short_name; bg.citySelectedStore = city; }
                }
                //print user's location
                if (city != '') {
                    console.log("Hello to you out there in " + city);
                    document.getElementById("showPosition").innerHTML = "Your location is: " + latitude.toFixed(6) + "," + longitude.toFixed(6) + "<br>" + "That's " + city +
                        "<br>" + "If it's not your location, please select below:";
                }
            }

        });
    }
    else if (city != "") {

        console.log("Hello to you out there in " + city);
        document.getElementById("showPosition").innerHTML = "Your location is: " + bg.latitude + "," + bg.longitude+ "<br>" + "That's " + city +
            "<br>" + "If it's not your location, please select below:";

    }

    var cityList = chrome.extension.getURL("data/countries.json");

    $.getJSON(cityList, function (json) {
        //show all the countries, look up countries short name start from "AA" to "ZZ", and set the select list.
        for (var i=65;i<=90;i++) {
            for(var j=65;j<=90;j++)
            {
                //this is city short name
                var cSname= "";
                cSname = String.fromCharCode(i);
                cSname +=String.fromCharCode(j); 
                if(typeof(json[cSname])!="undefined")
                {
                document.getElementById("selectCountry").innerHTML += "<option value=\"" + cSname+ "\">" + json[cSname].name + "</option>";
                }
            }
            
        }


    });





//show the warning content.
    var dataurl = chrome.extension.getURL("data/data.json");
    $.getJSON(dataurl, function (json) {
        //looking for the last warning info.
        for (var i = 0; i < json.records.length; i++) {
            var result = json.records[i];
            if (result.city == city) {
                if (result.level == "dangerous") {
                    //show warning image.
                    document.getElementById("warningImage").innerHTML = "<img src = \"image/dangerous.png\" alt = \"dangerous\">";
                }
                else if (result.level == "warning") {
                    document.getElementById("warningImage").innerHTML = "<img src = \"image/warning.png\" alt = \"warning\">";
                }
                else if (result.level == "notice") {
                    document.getElementById("warningImage").innerHTML = "<img src = \"image/notice.png\" alt = \"notice\">";
                }
                document.getElementById("showWarnings").innerHTML += "Time: " + result.time + "<br>" + "Level: " + result.level + "<br>" + "Details: " + result.details;
            }
        }


    });
});

//after user select country, select corresponding city here.
document.getElementById("selectCountry").onchange = function () {
    document.getElementById("selectCity").innerHTML = "";
    var cityList = chrome.extension.getURL("data/cities.json");
    $.getJSON(cityList, function (json) {
        var options = $("#selectCountry");
        countrySelected = options.find("option:selected").val();
        //store selected country's short name
        bg.countrySSelectedStore = countrySelected;

        for (var i = 0; i < json.length; i++) {
            if (json[i].country == countrySelected) {
                document.getElementById("selectCity").innerHTML += "<option value=\"" + json[i].name + "\">" + json[i].name + "</option>";
            }

        }

    });
}

document.getElementById("selectCity").onchange = function () {
    var options = $("#selectCity");
    citySelected = options.find("option:selected").text();
    citySelectedStore = citySelected;
    var cityList = chrome.extension.getURL("data/cities.json");
    console.log(bg.countrySSelectedStore);
    $.getJSON(cityList,function(json){
      for(var i=0;i<json.length;i++)
      {
          if(json[i].country == bg.countrySSelectedStore && json[i].name == citySelected)
          {
            document.getElementById("showPosition").innerHTML = "Your location is: " + json[i].lat + "," + json[i].lng + "<br>" + "That's " + citySelected +
            "<br>" + "If it's not your location, please select below:";
              break;
          }
      }
      bg.longitude = json[i].lng;
      bg.latitude = json[i].lat;
      bg.citySelectedStore = citySelected;
    });


}

document.getElementById("refreshButton").onclick = function ()
{
    //show the warning content.
    var dataurl = chrome.extension.getURL("data/data.json");
    $.getJSON(dataurl, function (json) {
        //looking for the last warning info.
        for (var i = 0; i < json.records.length; i++) {
            var result = json.records[i];
            if (result.city == bg.citySelectedStore) {
                if (result.level == "dangerous") {
                    //show warning image.
                    document.getElementById("warningImage").innerHTML = "<img src = \"image/dangerous.png\" alt = \"dangerous\">";
                }
                else if (result.level == "warning") {
                    document.getElementById("warningImage").innerHTML = "<img src = \"image/warning.png\" alt = \"warning\">";
                }
                else if (result.level == "safe") {
                    document.getElementById("warningImage").innerHTML = "<img src = \"image/notice.png\" alt = \"notice\">";
                }
                document.getElementById("showWarnings").innerHTML = "Time: " + result.time + "<br>" + "Level: " + result.level + "<br>" + "Details: " + result.details;
            break;
            }
        }
        if(i == json.records.length)
        {
            document.getElementById("showWarnings").innerHTML = "no info now, try click the refresh button to check the latest new."
        }


    });
}