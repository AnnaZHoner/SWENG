var latitude;
var longitude;
var countrySSelectedStore = "";
var citySelectedStore = "";
const dataurl = chrome.extension.getURL("data/alerts.json");
set = 0;
// connect to alerts database
var alertsDB = new PouchDB('https://fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix:e01ad0f8a3355ea74bf8efeb523cd6da8e8afe94f5a26b2e6af4a7112dd1d144@fc535eaf-52c1-47a3-acf6-c990cfa80dfd-bluemix.cloudantnosqldb.appdomain.cloud/alerts');
// this contains the latestEvent in json
var latestEvent;







alertsDB.changes({
    since: 'now',
    live: true,
    include_docs: true
  }).on('change', function (change) {
    if(!change.deleted)
    {
        latestEvent = change.doc;
        if(latestEvent.distressRatio >= 100)
        {
            alert("warning");
        }
    }
  }).on('error', function (err) {
    // handle errors
  });


