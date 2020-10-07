async function getEstimates() {
    $("#spinner").show();

    const inputs = getInputs();
    const data = await calculateEstimates(inputs);
    displayResults(data);

    $("#spinner").hide();
}

function getInputs() {
    const target = $("#target-list").val();
    const generalFields = optionMap[target]['generalFields'];
    const sampleFields = optionMap[target]['sampleFields'];

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
            url: '/t-test-2-sample-ind-calc',
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
    $("#results").empty();
    let header = "<h3>One Sided Test</h3>";
    $("#results").append(header);
    for (key in results['one_sided_test']) {
        let newLine = "<p>" + key + ": " + String(results['one_sided_test'][key]) + "</p>";
        $("#results").append(newLine);
    }

    header = "<h3>Two Sided Test</h3>";
    $("#results").append(header);
    for (key in results['two_sided_test']) {
        let newLine = "<p>" + key + ": " + String(results['two_sided_test'][key]) + "</p>";
        $("#results").append(newLine);
    }
}
