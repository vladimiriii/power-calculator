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
    const groupLabel = optionMap[status][target]["groupName"];
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

        label += `<form class="${optionRowClass}" onSubmit="return false;">`;
        label += `<label for="${f}">${fieldMap[f]['label']}</label>`;
        label += `<input type="number" id="${f}" step=${String(fieldMap[f]['step'])} value=${ String(fieldMap[f]['default'])}${min_clause}${max_clause}${required}>`;
        label += "</form>";
        $("#" + div).append(label);
    }

    // Sample Fields (need to be repeated X times)
    const perGroupFields = optionMap[status][target][div]['perGroup'];
    if (perGroupFields.length > 0) {
        if (orField) {
            $("#" + div).append(`<h4 class="${headerClass}"> — OR —</h4>`);
            $("#" + div).append(addCheckBox("binary-cb", "Binary Outcome?"));
            $("#binary-cb").click(binaryOutcomeChecked);
        }
        for (let j = 1; j <= groups; ++j) {
            $("#" + div).append(`<h4 class="${headerClass}">${groupLabel} ${String(j)}</h4>`);
            for (let i = 0; i < perGroupFields.length; ++i) {
                let f = perGroupFields[i];
                let label = "";
                label += `<form class="${optionRowClass}" onSubmit="return false;">`;
                label += `<label for="${f + String(j)}">${fieldMap[f]['label']}</label>`;
                label += `<input type="number" id="${f + String(j)}" step=${String(fieldMap[f]['step'])}>`;
                label += "</form>";
                $("#" + div).append(label);
                $("#" + div).on("change", updateCohensD);
            }
        }
    }
}


// AUTOMATED COHENS D
function meanAndStdInputsValid(){
    const values = [];
    values.push($('#mean1').val());
    values.push($('#mean2').val());
    values.push($('#stdDev1').val());
    values.push($('#stdDev2').val());
    if (values.every(function(i) { return !isNaN(i) && i.trim() != "" })) {
        return true;
    } else {
        return false;
    }
}


function sampleSizeFieldsValid(){
    const values = [];
    values.push($('#n1').val());
    values.push($('#n2').val());
    if (values.every(function(i) { return !isNaN(i) && i.trim() != "" })) {
        return true;
    } else {
        return false;
    }
}


function updateCohensD() {
    if (meanAndStdInputsValid()) {
        $("#effectSize").prop('disabled', true);
        const mean_diff = Math.abs(parseFloat($('#mean1').val()) - parseFloat($('#mean2').val()));
        const sd1 = parseFloat($('#stdDev1').val());
        const sd2 = parseFloat($('#stdDev2').val());
        if (sampleSizeFieldsValid()) {
            const n1 = parseInt($('#n1').val());
            const n2 = parseInt($('#n2').val());
            sdPooled = (((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2))**0.5;
        } else {
            sdPooled = ((sd1**2 + sd2**2)/2)**0.5;
        }

        const d = (mean_diff / sdPooled).toFixed(8);
        $("#effectSize").val(d);
    }
    else {
        $("#effectSize").prop('disabled', false);
    }
}


// BINARY FIELD FUNCTIONS
function addCheckBox(id, label) {
    let checkbox = `<div class="form-check">`
    checkbox += `<input class="form-check-input" type="checkbox" value="binary" id="${id}">`
    checkbox += `<label class="form-check-label" for="${id}">${label}</label></div>`
    return checkbox
}


function binaryOutcomeChecked() {
    const isChecked = $("#binary-cb").is(":checked");
    for (let i = 1; i <= 2; i++) {
        $("#stdDev" + String(i)).val("");
        $("#stdDev" + String(i)).prop('disabled', isChecked);
        let mean = $("#mean" + String(i)).val();
        if (isChecked) {
            updateStdDev(i);
            $("#mean" + String(i)).on("change", function() { updateStdDev(i); });
        } else {
            $("#mean" + String(i)).off("change");
        }
    }
}


function updateStdDev(i) {
    const mean = $("#mean" + String(i)).val();
    const isValidValue = mean != "" && !isNaN(mean) && mean >= 0 && mean <= 1;
    if (isValidValue) {
        const std = ((mean * (1 - mean))**0.5).toFixed(8);
        $("#stdDev" + String(i)).val(std);
    }
}


// RESET FIELDS
function resetOptionsAndResults() {
    $("#results-table").empty();
    $("#formulae").empty();
    $("#compulsoryFields").empty();
    $("#orFields").empty();
    clearCharts();
}
