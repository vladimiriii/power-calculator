function recommendTests() {
    const inputs = readRecommenderInputs();
    const filteredTestList = filterTestList(inputs);
    generateLinks(filteredTestList, "filtered-test-list");
}


function readRecommenderInputs() {
    const recommenderInputs = {};
    for (let i = 0; i < recommenderFields.length; ++i) {
        recommenderInputs[recommenderFields[i]] = $("#" + recommenderFields[i] + "-list").val();
    }
    return recommenderInputs;
}


function filterTestList(inputs) {
    const suitableTests = [];
    for (let i = 0; i < testMap.length; ++i) {
        let suitable = true;
        let testAttributes = testMap[i]['attributes'];
        for (attribute in inputs) {
            if (inputs[attribute] !== 'na' && jQuery.inArray(inputs[attribute], testAttributes[attribute]) == -1) {
                suitable = false;
                break;
            }
        }
        if (suitable) {
            suitableTests.push(testMap[i]);
        }
    }
    return suitableTests;
}


function generateLinks(tests, div) {
    $("#" + div).empty();
    if (div == "filtered-test-list") {
        $('#' + div).append("<h3>Recommended Tests</h3>")
    }
    for (let i = 0; i < tests.length; ++i) {
        if (tests[i]['status'] === 'available') {
            $("#" + div).append(
                '<p class="test-link"><a href="' + tests[i]['url'] + '">' + tests[i]['name'] + '</a></p>'
            );
        } else {
            $("#" + div).append(
                '<p class="test-link disabled">' + tests[i]['name'] + '</p>'
            );
        }
    }
}
