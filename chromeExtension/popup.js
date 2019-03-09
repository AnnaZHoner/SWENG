var latitude;
var longitude;
var city;
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
                city = "";
                for (var i = 0, len = result.address_components.length; i < len; i++) {
                    var ac = result.address_components[i];
                   if (ac.types.indexOf("administrative_area_level_1") >= 0) city = ac.short_name;
                }
                if (city != '') {
                    console.log("Hello to you out there in "+city );
                    document.getElementById("showPosition").innerHTML="Your location is: "+latitude.toFixed(6)+","+longitude.toFixed(6)+"<br>"+"That's "+city;
                }
            }
        
        });
        var cityList = chrome.extension.getURL("data/world_cities.json");
        $.getJSON(cityList,function(json){
            for(var i =1;i<json.length;i++)
            {
                if(json[i].country!=json[i-1].country)
               {
                document.getElementById("selectCountry").innerHTML+= "<option value=\""+json[i-1].country+"\">" +json[i-1].country+ "</option>";
                }
            }

        });


        var dataurl = chrome.extension.getURL("data/data.json");
        $.getJSON(dataurl,function(json) {
            for(var i = 0; i < json.records.length ; i++)
            {
                var result = json.records[i];
                if(result.city== city)
                {
                    if(result.level == "dangerous")
                    {
                        document.getElementById("warningImage").innerHTML = "<img src = \"image/dangerous.png\" alt = \"dangerous\">";
                    }
                    else if(result.level == "warning")
                    {
                        document.getElementById("warningImage").innerHTML = "<img src = \"image/warning.png\" alt = \"warning\">";
                    }
                    else if(result.level == "notice")
                    {
                        document.getElementById("warningImage").innerHTML = "<img src = \"image/notice.png\" alt = \"notice\">";
                    }
                    document.getElementById("showWarnings").innerHTML+="Time: " +result.time +"<br>"+"Level: " +result.level+"<br>"+"Details: " +result.details;
                }
            }
            

        });
});




