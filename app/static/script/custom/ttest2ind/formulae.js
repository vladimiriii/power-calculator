function renderFormulas(formulae) {
    console.log(formulae);
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
