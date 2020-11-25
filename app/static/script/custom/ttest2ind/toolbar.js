function updateTargetSelector() {
    resetOptionsAndResults();
    $("#target-select").empty();

    const status = $("#status-list").val();
    let options = `<p>What do you want to calculate?</p>`;
    options += `<select id="target-list" class="form-control eco-select">`;
    for (key in optionMap[status]) {
        options += `<option value="${key}">${optionMap[status][key]['displayName']}</option>`;
    }
    options += `</select>`;
    $("#target-select").append(options);
    $("#target-list").change(updateInputOptions);
    updateInputOptions();
}

function updateInputOptions() {
    resetOptionsAndResults();
    const status = $("#status-list").val();
    const target = $("#target-list").val();
    addOptionFields(status, target, "compulsoryFields", false);
    addOptionFields(status, target, "orFields", true);
}

function addOptionFields(status, target, div, orField) {
    const oneOffFields = optionMap[status][target][div]['oneOf'];
    const optionRowClass = "option-row";
    const headerClass = "option-header";
    $("#" + div).empty();

    // General Fields
    for (let i = 0; i < oneOffFields.length; ++i) {
        let f = oneOffFields[i];
        let label = "";

        let min_clause = "";
        if ('min' in fieldMap[f]) {
            min_clause = ' min="' + String(fieldMap[f]["min"]) + '" ';
        }

        let max_clause = "";
        if ('max' in fieldMap[f]) {
            max_clause = ' max="' + String(fieldMap[f]["max"]) + '" ';
        }

        let required = "";
        if (fieldMap[f]['required']) {
            required = " required";
        }

        label += '<form class="' + optionRowClass + '" onSubmit="return false;">';
        label += '<label for="' + f + '">' + fieldMap[f]['label'] + '</label>';
        label += '<input type="number" id="' + f + '" step=' + String(fieldMap[f]['step']) + ' value=' + String(fieldMap[f]['default']) + min_clause + max_clause + required + '>';
        label += "</form>";
        $("#" + div).append(label);
    }

    // Sample Fields (need to be repeated X times)
    const perGroupFields = optionMap[status][target][div]['perGroup'];
    if (perGroupFields.length > 0) {
        if (orField) {
            $("#" + div).append('<h4 class="' + headerClass + '"> — OR —</h4>');
        }
        for (let j = 1; j <= groups; ++j) {
            $("#" + div).append("<h4 class=" + headerClass + ">Group " + String(j) + "</h4>");
            for (let i = 0; i < perGroupFields.length; ++i) {
                let f = perGroupFields[i];
                let label = "";
                label += '<form class="' + optionRowClass + '" onSubmit="return false;">';
                label += '<label for="' + f + String(j) + '">' + fieldMap[f]['label'] + '</label>';
                label += '<input type="number" id="' + f + String(j) + '" step=' + String(fieldMap[f]['step']) + '>';
                label += "</form>";
                $("#" + div).append(label);
            }
        }
    }
}

function resetOptionsAndResults() {
    $("#results-table").empty();
    $("#formulae").empty();
    initializeCharts();
    $("#compulsoryFields").empty();
    $("#orFields").empty();
}
