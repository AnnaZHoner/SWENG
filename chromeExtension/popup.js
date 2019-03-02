 navigator.geolocation.getCurrentPosition(function(pos,error){
    if(!navigator.geolocation) throw "geolocation not support";
        var latitude=pos.coords.latitude;                             
        var longitude=pos.coords.longitude;
        var accuracy=pos.coords.accuracy;
        document.getElementById("showPosition").innerHTML="your location is: "+latitude+","+longitude;
});
