function changeMolding(cl) {
    document.getElementById("painting").className = "painting-big molded " + cl;
}

function HideMoldings() {
    document.getElementById("painting").className = "painting-big";
    document.getElementById("moldings").style.display = "none";
}

function ShowMoldings(cl) {
    document.getElementById("painting").className = "painting-big molded " + cl;
    document.getElementById("moldings").style.display = "block";
}

$(function() {
    $("#moldings").wrapInner("<table cellspacing='30'><tr>");
    $(".molding").wrap("<td>");
});