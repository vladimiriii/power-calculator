async function getEstimates() {
    $("#spinner").show();

    const inputs = getInputs();
    try {
        const response = await calculateEstimates(inputs);
        clearCharts();
        displayResults(response['statistics']);
        createChart('chart-1', response['charts']['chartOne']);
        createChart('chart-2', response['charts']['chartTwo']);
        createChart('chart-3', response['charts']['chartThree']);
        renderFormulas(response['formulae']);
        addFormulaNotes(response['notes']);

        // Scroll to results section
        const offset = $("#results-container").offset();
        $('html, body').animate({
            scrollTop: offset.top,
            scrollLeft: offset.left
        });
    } catch {
        $("#error-modal-header").empty();
        $("#error-modal-body").empty();
        $("#error-modal-header").text("Something Went Wrong!");
        $("#error-modal-body").text("We couldn't process your request. Please check you have provided all the required inputs and try again.");
        $("#error-modal").modal('show');
    }

    $("#spinner").hide();
}

function getInputs() {
    const status = $("#status-list").val();
    const target = $("#target-list").val();

    let generalFields = optionMap[status][target]["compulsoryFields"]['oneOf'];
    generalFields = generalFields.concat(optionMap[status][target]["orFields"]['oneOf']);

    let sampleFields = optionMap[status][target]["compulsoryFields"]['perGroup'];
    sampleFields = sampleFields.concat(optionMap[status][target]["orFields"]['perGroup']);

    // Initiate results object
    const inputs = {'target': target};

    // General Fields
    for (let i = 0; i < generalFields.length; ++i) {
        inputs[generalFields[i]] = $("#" + generalFields[i]).val();
    }

    // Sample Fields
    inputs['sampleFields'] = [];
    for (let j = 1; j <= groups; ++j) {
        let sampleInputs = {};
        for (let i = 0; i < sampleFields.length; ++i) {
            let fieldName = sampleFields[i] + String(j)
            sampleInputs[sampleFields[i]] = $("#" + fieldName).val()
        }
        inputs['sampleFields'].push(sampleInputs);
    }

    return inputs;
}


function calculateEstimates(inputs) {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "POST",
            url: '/t-test-independent-samples-calc',
            data: JSON.stringify(inputs),
            contentType: 'application/json',
            success: (response) => {
                resolve(response);
            },
            error: (response) => {
                reject(response);
            }
        })
    })
}


function displayResults(results) {
    $("#results-table").empty();

    let table = '<table class="table table-bordered"><thead><tr>';
    table += '<th scope="col">Group</th>';
    table += '<th scope="col">One Sided Test</th>';
    table += '<th scope="col">Two Sided Test</th>';
    table += '</tr></thead><tbody>';

    for (let i = 0; i < results.length; ++i) {
        table += '<tr>';
        table += '<th scope="row">' + results[i]['label'].toLocaleString(undefined, {minimumFractionDigits: 0}) + '</th>';
        table += '<td>' + results[i]['one_sided_test'].toLocaleString(undefined, {minimumFractionDigits: 0}) + '</td>';
        table += '<td>' + results[i]['two_sided_test'].toLocaleString(undefined, {minimumFractionDigits: 0}) + '</td>';
        table += '</tr>';
    }

    table += '</tbody></table>'
    $("#results-table").append(table);
}
