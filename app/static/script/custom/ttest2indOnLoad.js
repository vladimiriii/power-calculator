const groups = 2;

$(document).ready(function(){

    // Run this to initiate a set of fields
    updateInputs()

    // Initialize Charts
    Chart.defaults.global.defaultFontFamily = 'Roboto';
    configOne = createChartConfig();
    configTwo = createChartConfig();
    chartOne = generateChart('chart-1', configOne);
    chartTwo = generateChart('chart-2', configTwo);


    $("#target-list").change(updateInputs);
    $("#go-btn").click(getEstimates);

});
