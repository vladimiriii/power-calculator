function renderFormulas(formulae) {
    $("#formulae").empty();
    for (var i = 0; i < formulae.length; i++) {
        let cleanFormula = formulae[i].replace(/{{/g, "{").replace(/}}/g, "}");
        $("#formulae").append(`<p>Step ${i + 1}: <span class='math'>${formulae[i]}</span></p>`);
    }

    const math = document.getElementsByClassName('math');
    for (var i = 0; i < math.length; i++) {
        katex.render(math[i].textContent, math[i]);
    }
}


function addFormulaNotes(notes) {
    $("#notes").empty();
    if (notes.length > 0){
        $("#notes").append('<h4 class="subheader">Notes</h4>')
        for (var i = 0; i < notes.length; i++) {
            $("#notes").append(`<p class="notes">${i + 1}. ${notes[i]}</p>`);
        }
    }
}
