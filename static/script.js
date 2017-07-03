// Food, Places, Chapters

function d(smthg) {
	console.log(smthg)
}


$(document).ready(function() {
	d('ready');
	$(".type-1").hide();
    $(".type-2").hide();

	$('#ques_type').change(function() {
    var selection = $(this).val();

    switch (selection) {
        case "Food":
        case "Places":
        case "Chapters":
        	$(".type-1").hide();
            $(".type-2").show();            
            break;

        case "Faculty":
        case "Admissions":
        case "FFCS":
        case "General":
        	$(".type-1").show();
            $(".type-2").hide();
            break;

        default:
        	$(".type-1").hide();
    		$(".type-2").hide();
            break;
    }
	});
});


