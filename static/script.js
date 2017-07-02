// Food, Places, Chapters

function d(smthg) {
	console.log(smthg)
}


$(document).ready(function() {
	d('ready');
	$("#quesD").hide();
    $("#ansD").hide();
    $("#fpname").hide();
    $("#rating").hide();
    

	$('#ques_type').change(function() {
    var selection = $(this).val();

    d('hi');

    switch (selection) {
        case "Food":
        case "Places":
        case "Chapters":
        	$("#quesD").hide();
            $("#ansD").hide();
            $("#fpname").show();
            $("#rating").show();            
            break;

        case "Faculty":
        case "Admissions":
        case "FFCS":
        case "General":
        	$("#quesD").show();
            $("#ansD").show();
            $("#fpname").hide();
            $("#rating").hide();
            break;

        default:
            $("#quesD").hide();
            $("#ansD").hide();
            $("#fpname").hide();
            $("#rating").hide();
            break;
    }
	});
});


