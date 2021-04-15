const server_adders = JSON.parse(document.getElementById('server').textContent);
const apikey=JSON.parse(document.getElementById('key').textContent);
const server=`http://${server_adders}/`
const api=`${server}api/`;
const api_place=`${api}place/`;
const api_harmed=`${api}harmed/`;
const api_vehicle=`${api}vehicle/`;
const api_station=`${api}station/`;
const  api_place_with_borough=`${api_place}/?borough=`;
var jsElm = document.createElement("script");
jsElm.type = "application/javascript";
jsElm.src=`https://maps.googleapis.com/maps/api/js?key=${apikey}&callback=initMap`
document.head.appendChild(jsElm);

