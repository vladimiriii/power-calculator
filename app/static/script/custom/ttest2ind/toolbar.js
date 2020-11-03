function updateInputs() {
    const target = $("#target-list").val();
    addOptionFields(target, "compulsoryFields", false);
    addOptionFields(target, "orFields", true);
}


function addOptionFields(target, div, orField) {
    const oneOffFields = optionMap[target][div]['oneOf'];
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
    const perGroupFields = optionMap[target][div]['perGroup'];
    if (perGroupFields.length > 0) {
        if (orField) {
            $("#" + div).append('<h4 class="' + headerClass + '"> — OR —</h4>');
        }
        for (let j = 1; j <= groups; ++j) {
            $("#" + div).append("<h4 class=" + headerClass + ">Sample " + String(j) + "</h4>");
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
