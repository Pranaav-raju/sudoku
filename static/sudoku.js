function getOtherLine(pos) {
    var fullLine = [];
    var target = parseInt(pos);
    for (var i = 0; i < 9; i++) {
        if (i != target) {
            fullLine.push(i);
        }
    }
    return fullLine;
}

function checkRow(pos, form) {
    // Return duplicate's location
    let rowNum = pos[0];
    let cols = getOtherLine(pos[1]);
    let cellVal = form.elements.namedItem(pos).value;
    for (let col of cols) {
        if (form.elements.namedItem(rowNum + col).value == cellVal) {
            return rowNum + col;
        }
    }
}

function checkCol(pos, form) {
    let colNum = pos[1];
    let rows = getOtherLine(pos[0]);
    let cellVal = form.elements.namedItem(pos).value;
    for (let row of rows) {
        if (form.elements.namedItem(row + colNum).value == cellVal) {
            return row + colNum;
        }
    }
}

function checkBox(pos, form) {
    let boxSets = [["00", "01", "02", "10", "11", "12", "20", "21", "22"],
                    ["03", "04", "05", "13", "14", "15", "23", "24", "25"],
                    ["06", "07", "08", "16", "17", "18", "26", "27", "28"],
                    ["30", "31", "32", "40", "41", "42", "50", "51", "52"],
                    ["33", "34", "35", "43", "44", "45", "53", "54", "55"],
                    ["36", "37", "38", "46", "47", "48", "56", "57", "58"],
                    ["60", "61", "62", "70", "71", "72", "80", "81", "82"],
                    ["63", "64", "65", "73", "74", "75", "83", "84", "85"],
                    ["66", "67", "68", "76", "77", "78", "86", "87", "88"],
                    ]
    let currVal = form.elements.namedItem(pos).value;
    for (let box of boxSets) {
        if (!box.includes(pos)) {
            continue;
        }
        for (let cell of box) {
            if (cell != pos && form.elements.namedItem(cell).value == currVal) {
                return cell;
            }
        }
    }
}

function check(input, cell) {
    if (input.value == "" || input.value == "0") {
        input.setCustomValidity('');
    }
    else if (!(["1", "2", "3", "4", "5", "6", "7", "8", "9"].includes(input.value))) {
        input.setCustomValidity('Please enter a number in the range 1-9.');
    } else {
        let rowValid = checkRow(cell, document.forms[0]);
        if (rowValid != undefined) {
            input.setCustomValidity('This row already contains that number.');
            return;
        }
        let colValid = checkCol(cell, document.forms[0]);
        if (colValid != undefined) {
            input.setCustomValidity('This column already contains that number.');
            return;
        }
        let boxValid = checkBox(cell, document.forms[0]);
        if (boxValid != undefined) {
            input.setCustomValidity('This box already contains that number.');
            return;
        }
        // Input is fine -- reset the error message
        input.setCustomValidity('');
        // Auto advance to last cell (nothing happens if already in bottom right corner)
        if (input.value.length == 1) {
            let nextName = $('#' + input.name).data("next");
            let nextCell = document.forms[0].elements.namedItem(nextName);
            $(nextCell).focus();
        }
    }
}