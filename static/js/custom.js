function showFlashMessage(message) {
	// var template = "{% include 'alert.html' with message='" + message + "' %}"
	var template = "<div class='container container-alert-flash'>" + 
	"<div class='col-sm-3 col-sm-offset-8'> " + 
	"<div class='alert alert-success alert-dismissible' role='alert'>" + 
	"<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
	"<span aria-hidden='true'>&times;</span></button>" 
	+ message + "</div></div></div>"
	$("body").append(template);
	$(".container-alert-flash").fadeIn();
	setTimeout(function(){ 
		$(".container-alert-flash").fadeOut();
	}, 1800);

}