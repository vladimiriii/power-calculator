const groups = 2;

$(document).ready(function(){

    // Run this to initiate a set of fields
    updateInputs()

    $("#target-list").change(updateInputs);
    $("#go-btn").click(getEstimates);

});
