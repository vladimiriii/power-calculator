const groups = 2;

$(document).ready(function(){

    // Run this to initiate a set of fields
    updateInputs();

    // Initialize Charts
    Chart.defaults.global.defaultFontFamily = 'Roboto';
    configOne = createChartConfig();
    configTwo = createChartConfig();
    configThree = createChartConfig();
    chartOne = generateChart('chart-1', configOne);
    chartTwo = generateChart('chart-2', configTwo);
    chartThree = generateChart('chart-3', configThree);

    $("#target-list").change(updateInputs);
    $("#go-btn").click(function() {
        getEstimates();
        const offset = $("#results-container").offset();
        $('html, body').animate({
            scrollTop: offset.top,
            scrollLeft: offset.left
        });
    });

});
