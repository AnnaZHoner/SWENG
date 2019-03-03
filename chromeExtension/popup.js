var latitude;
var longitude;
navigator.geolocation.getCurrentPosition(function(pos,error){
    if(!navigator.geolocation) throw "geolocation not support";
        latitude=pos.coords.latitude;                             
        longitude=pos.coords.longitude;
        var geocodingAPI = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+latitude+","+longitude+"&key=AIzaSyCUe-myHsErw9OjBwB7mIqlo4FzYX-qzkw";
        $.getJSON(geocodingAPI, function (json) {
            if (json.status == "OK") {
                //Check result 0
                var result = json.results[0];
                //look for locality tag and administrative_area_level_1
                var city = "";
                var state = "";
                for (var i = 0, len = result.address_components.length; i < len; i++) {
                    var ac = result.address_components[i];
                   if (ac.types.indexOf("administrative_area_level_1") >= 0) state = ac.short_name;
                }
                if (state != '') {
                    console.log("Hello to you out there in "+state );
                    document.getElementById("showPosition").innerHTML="your location is: "+latitude+","+longitude+"  That's "+state;
                }
            }
        
        });
});




