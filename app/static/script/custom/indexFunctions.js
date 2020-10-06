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
            suitableTests.push({"name": testMap[i]["name"], "url": testMap[i]["url"]});
        }
    }
    return suitableTests;
}


function generateLinks(tests, div) {
    $("#" + div).empty();
    for (let i = 0; i < tests.length; ++i) {
        $("#" + div).append(
            '<p class="test-link"><a href="' + tests[i]['url'] + '">' + tests[i]['name'] + '</a></p>'
        );
    }
}
