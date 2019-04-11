var bg = chrome.extension.getBackgroundPage();
var latitude;
var longitude;
var city;


//getting user's location using HTML5 geolocation
navigator.geolocation.getCurrentPosition(function (pos, error) {
    

    if (!navigator.geolocation) throw "geolocation not support";
    while (typeof (bg.citySelectedStore) === "undefined") {
    }
    city = bg.citySelectedStore;
    if (city === "") {
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
                        findLatestEvent()
                }
            }

        });
    }
    else if (city != "") {

        console.log("Hello to you out there in " + city);
        document.getElementById("showPosition").innerHTML = "Your location is: " + bg.latitude + "," + bg.longitude + "<br>" + "That's " + city +
            "<br>" + "If it's not your location, please select below:";
            findLatestEvent()

    }


    var countrySSelectedStore = "";
    var citySelectedStore = "";












    //show all the countries in the country select listing, get them from countries Database
    var countriesDB = new PouchDB('https://fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix:e01ad0f8a3355ea74bf8efeb523cd6da8e8afe94f5a26b2e6af4a7112dd1d144@fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix.cloudantnosqldb.appdomain.cloud/countries');
    countriesDB.allDocs({
        include_docs: true,
    }).then(function (result) {
        console.log(result.rows[0].doc.name);
        for (var i = 0; i < result.rows.length; i++) {
            document.getElementById("selectCountry").innerHTML += "<option value=\"" + result.rows[i].doc._id + "\">" + result.rows[i].doc.name + "</option>";
        }
    }).catch(function (err) {
        console.log(err);
    });










});

//after user select country, select corresponding city here.
document.getElementById("selectCountry").onchange = function () {
    document.getElementById("selectCity").innerHTML = "";
    var citiesDB = new PouchDB('https://fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix:e01ad0f8a3355ea74bf8efeb523cd6da8e8afe94f5a26b2e6af4a7112dd1d144@fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix.cloudantnosqldb.appdomain.cloud/states');
    var options = $("#selectCountry");
    countrySelected = options.find("option:selected").val();

    //store selected country's short name
    bg.countrySSelectedStore = options.find("option:selected").text();
    console.log(parseInt(countrySelected));
    citiesDB.createIndex({
        index: { fields: ['country_id'] }
    });
    citiesDB.find({
        selector: {
            country_id: {$eq:parseInt(countrySelected)}
        },
        fields: ['name','_id']
    }).then(function (result) {
        console.log(result);
        for (var i = 0; i < result.docs.length; i++) {
            document.getElementById("selectCity").innerHTML += "<option value=\"" + result.docs[i]._id + "\">" + result.docs[i].name + "</option>";

        }


    }).catch(function (err) {
        console.log(err);
    });




}

document.getElementById("selectCity").onchange = function () {
    var options = $("#selectCity");
    citySelected = options.find("option:selected").text();
    citySelectedStore = citySelected;
    // using goole map api to get the longtitude and lagitude for the city.
    var requestCoor = "https://maps.googleapis.com/maps/api/geocode/json?address="+citySelected+","+bg.countrySSelectedStore+"&key=AIzaSyCUe-myHsErw9OjBwB7mIqlo4FzYX-qzkw"
    $.getJSON(requestCoor, function (json) {
        //check if the return json file is alright.
        if (json.status == "OK") {
            var location = json.results[0].geometry.location;
                document.getElementById("showPosition").innerHTML = "Your location is: " + location.lat + "," + location.lng + "<br>" + "That's " + citySelected +
                    "<br>" + "If it's not your location, please select below:";
                    bg.longitude = location.lng;
                    bg.latitude = location.lat;
                    bg.citySelectedStore = citySelected;
                    city = citySelected;
                    findLatestEvent()
                }
        else{
            document.getElementById("showPosition").innerHTML = "Your location is: " + citySelected +
                    "<br>" + "If it's not your location, please select below:";
                    bg.citySelectedStore = citySelected;

        }


    });

}




function findLatestEvent()
{
bg.alertsDB.find({
    selector: {
        country_id: {$eq:city}
    },
    fields: ['location','distressRatio','tweets']
}).then(function (theResult) {
    //show the last previous event
    var result = theResult.docs[theResult.docs.length-1];
    showLatestEvent(result)

}).catch(function (err) {
    document.getElementById("warningImage").innerHTML = "";
    document.getElementById("showWarnings").innerHTML = "no info now.";
  });
}

function showLatestEvent(result)
{
    if (result.location === city) {
        if (result.distressRatio >=50) {
            //show warning image.
            document.getElementById("warningImage").innerHTML = "<img src = \"image/dangerous.png\" alt = \"dangerous\">";
        }
        else if (result.distressRatio <50 && result.distressRatio >20) {
            document.getElementById("warningImage").innerHTML = "<img src = \"image/warning.png\" alt = \"warning\">";
        }
        else if (result.distressRatio <20) {
            document.getElementById("warningImage").innerHTML = "<img src = \"image/notice.png\" alt = \"notice\">";
        }
        document.getElementById("showWarnings").innerHTML = "Location: " + result.location + "<br>" + "Distress Ratio: " + result.distressRatio + "<br>" + "Tweets: "+"<br>"+" ";
        for(var j=0;j<result.tweets.length;j++)
        {
        document.getElementById("showWarnings").innerHTML += "<br>"+j+". " + result.tweets[j] + "<hr>";
        }
    }
}