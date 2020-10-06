$(document).ready(function(){

    // Run this to initiate a set of fields
    updateInputs()

    $("#target-list").change(updateInputs);
    $("#go-btn").click(calculateEstimate);

});
