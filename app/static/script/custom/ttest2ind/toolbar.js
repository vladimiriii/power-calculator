function updateInputs() {
    const target = $("#target-list").val();
    $("#options").empty()
    addOptionFields(target, groups);
}


function addOptionFields(target, groups) {
    const headerClass = "option-header";
    const generalFields = optionMap[target]["generalFields"];
    const sampleFields = optionMap[target]["sampleFields"];

    // Header
    $("#options").append("<h4 class=" + headerClass + ">General</h4>");

    // General Fields
    for (let i = 0; i < generalFields.length; ++i) {
        let f = generalFields[i];
        let label = "";
        label += '<form onSubmit="return false;">';
        label += '<label for="' + f + '">' + fieldMap[f]['label'] + '</label>';
        label += '<input type="number" id="' + f + '" step=' + String(fieldMap[f]['step']) + ' value=' + String(fieldMap[f]['default']) + '>';
        label += "</form>";
        $("#options").append(label);
    }

    // If we are showing both an effect size field and sample fields, need to explain
    if (generalFields.indexOf("effectSize") >= 0 && sampleFields.indexOf("mean") >= 0) {
        let text = "<h4 class=" + headerClass + ">Note</h4>";
        text += "<p>You can choose to either specify an effect size above OR add sample means and standard deviations below. ";
        text += "If both are provided, the sample information will be used.</p>";
        $("#options").append(text);
    }

    // Sample Fields (need to be repeated X times)
    for (let j = 1; j <= groups; ++j) {
        $("#options").append("<h4 class=" + headerClass + ">Sample " + String(j) + "</h4>");
        for (let i = 0; i < sampleFields.length; ++i) {
            let f = sampleFields[i];
            let label = "";
            label += '<form onSubmit="return false;">';
            label += '<label for="' + f + String(j) + '">' + fieldMap[f]['label'] + '</label>';
            label += '<input type="number" id="' + f + String(j) + '" step=' + String(fieldMap[f]['step']) + '>';
            label += "</form>";
            $("#options").append(label);
        }
    }
}
