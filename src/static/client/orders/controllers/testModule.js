if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position){
    	var pos = {
    		lat: position.coords.latitude,
    		lng: position.coords.longitude,
    	}
    	console.log(pos);
    	vm.lat = pos.lat;
    	vm.lng = pos.lng;
    });
}
else {
    vm.error = "Geolocation is not supported by this browser.";
}