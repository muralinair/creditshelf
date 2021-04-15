(function(){
    'use strict';
    var app=angular.module("creditshelf",[]);
    app.controller("rootController",function ($scope,$rootScope, $http) {
        var result = [];
        var map=null;
        var allBoroughLocation=[];
        var invalid_killed=0;
        var invalid_injured=0;
        var actual_killed=0;
        var actual_injured=0
        $rootScope.highlighters = [];
        $rootScope.highlighters_parking = [];
        angular.element(document).ready(function (){
            map = new google.maps.Map(document.getElementById("googleMap"), {
                zoom: 15,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
            });
        })
        $http.get(api_place).then((response) => {
            let value = null;
            let obj = response.data;
            for (let i = 0; i < obj.length; i++) {
                value = obj[i]["borough"];
                if (!result.includes(value)) {
                    result.push(value);
                }
            }
            $scope.dropdown = result;
            return obj;
        });
        $scope.updateLocations = function () {
            let locations = [];
            if ($scope.bInvalidLocations) {
                let rootLocations = $rootScope.location.slice()
                for (let l = 0; l < rootLocations.length; l++) {
                    if (rootLocations[l].lat !== 0 && rootLocations[l].lng !== 0) {
                        locations.push(rootLocations[l]);
                    }
                }
                $rootScope.location = locations;
                $scope.no_of_killed=$scope.no_of_killed-invalid_killed;
                $scope.no_of_injured=$scope.no_of_injured-invalid_injured;
            } else {
                $scope.dropdown = result;
                $rootScope.location=allBoroughLocation;
                $scope.no_of_killed=actual_killed;
                $scope.no_of_injured=actual_injured;
            }
            $scope.updateMaps();

        };
        $scope.getBorough = function () {
            let no_of_killed = 0;
            let no_of_injured = 0;
            let harmed = [];
            let harmed_at_borough = [];
            let location = []
            $http.get(`${api_place_with_borough}${$scope.borough}`).then(function (response) {
                harmed_at_borough = response.data;
            }).then(function () {
                $http.get(api_harmed).then(function (response) {
                    harmed = response.data;
                }).then(function () {
                    harmed_at_borough.forEach(function (value, index) {
                        harmed.forEach(function (value_harmed, index) {
                            if (value_harmed.collision_id === value.collision_id) {
                                no_of_killed = no_of_killed + value_harmed.cycl_killed;
                                no_of_injured = no_of_injured + value_harmed.cycl_injured;
                                if(parseFloat(value.location_lat) === 0 || parseFloat(value.location_log) ===0 ){
                                    invalid_killed=invalid_killed + value_harmed.cycl_killed;
                                    invalid_injured=invalid_injured + value_harmed.cycl_injured;
                                }
                                if (value_harmed.cycl_killed > 0 || value_harmed.cycl_injured > 0) {

                                    location.push({
                                        lat: parseFloat(value.location_lat),
                                        lng: parseFloat(value.location_log),
                                        name: value.on_street
                                    });
                                }
                            }
                        })
                    });
                }).then(function () {
                    $scope.no_of_killed = no_of_killed;
                    $scope.no_of_injured = no_of_injured;
                    actual_killed=no_of_killed;
                    actual_injured=no_of_injured;
                    $rootScope.location = location;
                    allBoroughLocation=location;
                }).then(function (){
                    $scope.updateMaps();
                });
            });
        }

        var createHighlighter = function (location,markerObj,icon=null, title=null) {
                const marker = new google.maps.Marker({
                    position: location,
                    icon: icon,
                    map: map,
                    title: title,
                });
                markerObj.push(marker);
                return marker;
            }

        var deleteMarkers = function (markerObj) {
            for (let i = 0; i < markerObj.length; i++) {
                markerObj[i].setMap(null);
            }
        }

        $scope.updateMaps = function () {
            deleteMarkers($rootScope.highlighters);
            $rootScope.highlighters.length=0;
            $rootScope.location.forEach(function (value) {
                createHighlighter(value,$rootScope.highlighters);
                let loc = $rootScope.highlighters[0].getPosition();
                map.setCenter(loc);
            });
        };

        $scope.updateStations=function (){
            if($scope.bShowStations) {
                $scope.test_from_then="Hello"
                var directionsDisplay=[];
                $http.get(api_station).then(function (response) {
                    $scope.test_from_then="World"
                    let icon = DJANGO_PARKING_ICON;
                    $scope.station_to_map=[];
                    let station_to_map=[];
                    response.data.forEach(function (value) {
                        let marker_location=new google.maps.LatLng(parseFloat(value.location_lat), parseFloat(value.location_log));
                        var parkingInfo = createHighlighter(marker_location,$rootScope.highlighters_parking,icon, value.station_name);
                        google.maps.event.addListener(parkingInfo, 'click', () => {
                            const divNode = document.getElementById("panel")
                            while (divNode.firstChild) {
                                divNode.firstChild.remove()
                            }
                            for(let i=0;i<directionsDisplay.length;i++){
                                directionsDisplay[i].setMap(null);
                            }
                            directionsDisplay=[];
                            $rootScope.location.forEach(function (value, index) {
                                let distance=0;
                                var directionsService = new google.maps.DirectionsService();
                                directionsDisplay[index] = new google.maps.DirectionsRenderer();
                                directionsDisplay[index].setMap(map);
                                var request = {
                                    origin: parkingInfo.position,
                                    destination: new google.maps.LatLng(value.lat, value.lng),
                                    travelMode: "BICYCLING",
                                    unitSystem: google.maps.UnitSystem.METRIC,
                                };
                                directionsService.route(request, function (response, status) {
                                    if (status === google.maps.DirectionsStatus.OK) {
                                        var jsElm = document.createElement("h5");
                                        directionsDisplay[index].setDirections(response);
                                        distance=(response.routes[0].legs[0].distance.value)/1000
                                        $scope.test_outside=`From ${parkingInfo.title} to ${value.name} ${(response.routes[0].legs[0].distance.value)/1000} KM`;
                                        jsElm.innerText=`From '${parkingInfo.title}' to '${value.name}' : ${(response.routes[0].legs[0].distance.value)/1000} KM`
                                        divNode.appendChild(jsElm);
                                        return distance;
                                    }
                                });
                            });
                            $scope.station_to_map=station_to_map;
                        });
                        $rootScope.highlighters_parking.push(parkingInfo);
                    });
                });
            }else{
                $rootScope.highlighters_parking.forEach(function (highlighter){
                    highlighter.setMap(null);
                });
            }
        }
    });
})()