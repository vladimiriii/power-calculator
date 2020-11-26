const groups = 2;

$(document).ready(function(){

    // Run this to initiate a set of fields
    updateTargetSelector();

    // Initialize Charts Font
    Chart.defaults.global.defaultFontFamily = 'Roboto';

    $("#status-list").change(updateTargetSelector);
    $("#go-btn").click(getEstimates);

});
