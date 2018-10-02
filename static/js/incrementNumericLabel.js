// A function to increment the numeric value of a label with a provided ID by a provided amount

function incrementNumericLabel(labelID, incrementValue) {
    let label = document.getElementById(labelID);
    let labelValue = parseInt(label.innerText);
    labelValue += incrementValue;
    label.innerText = labelValue;
}