$('.onlyEng').bind('keypress', function (event) {
    var regex = new RegExp("^[a-zA-Z0-9_]+$");
    var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
    if (!regex.test(key)&&event.charCode!=13) {
		alert('you can type her only [a-zA-Z0-9]_');
    	event.preventDefault();
    	return false;
    }
    if(event.charCode==13)
    {    	
    	//kode for pressing enter...
    }    	
});