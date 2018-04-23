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

function checkRow(pos, formElements) {
    // Return duplicate's location
    let rowNum = pos[0];
    let cols = getOtherLine(pos[1]);
    let cellVal = formElements.namedItem(pos).value;
    for (let col of cols) {
        if (formElements.namedItem(rowNum + col).value == cellVal) {
            return rowNum + col;
        }
    }
}

function checkCol(pos, formElements) {
    let colNum = pos[1];
    let rows = getOtherLine(pos[0]);
    let cellVal = formElements.namedItem(pos).value;
    for (let row of rows) {
        if (formElements.namedItem(row + colNum).value == cellVal) {
            return row + colNum;
        }
    }
}

// Cells that share 3x3 boxes
var boxSets = [["00", "01", "02", "10", "11", "12", "20", "21", "22"],
["03", "04", "05", "13", "14", "15", "23", "24", "25"],
["06", "07", "08", "16", "17", "18", "26", "27", "28"],
["30", "31", "32", "40", "41", "42", "50", "51", "52"],
["33", "34", "35", "43", "44", "45", "53", "54", "55"],
["36", "37", "38", "46", "47", "48", "56", "57", "58"],
["60", "61", "62", "70", "71", "72", "80", "81", "82"],
["63", "64", "65", "73", "74", "75", "83", "84", "85"],
["66", "67", "68", "76", "77", "78", "86", "87", "88"],
]

function checkBox(pos, formElements) {
    let currVal = formElements.namedItem(pos).value;
    for (let box of boxSets) {
        if (!box.includes(pos)) {
            continue;
        }
        for (let cell of box) {
            if (cell != pos && formElements.namedItem(cell).value == currVal) {
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
        let formElements = document.forms[0].elements;
        let rowValid = checkRow(cell, formElements);
        if (rowValid != undefined) {
            input.setCustomValidity('This row already contains that number.');
            return;
        }
        let colValid = checkCol(cell, formElements);
        if (colValid != undefined) {
            input.setCustomValidity('This column already contains that number.');
            return;
        }
        let boxValid = checkBox(cell, formElements);
        if (boxValid != undefined) {
            input.setCustomValidity('This box already contains that number.');
            return;
        }
        // Input is fine -- reset the error message
        input.setCustomValidity('');
        // Auto advance to last cell (nothing happens if already in bottom right corner)
        if (input.value.length == 1) {
            let nextName = $('#' + input.name).data("next");
            let nextCell = formElements.namedItem(nextName);
            $(nextCell).focus();
        }
    }
}

function getCellValue(pos, puzzleString) {
    if (puzzleString == undefined) {
        return '';
    }
    // Elements beginning in 0 are on the first row and map directly
    let cellLoc = parseInt(pos);
    // Positions never end in 9, so every 10th positions is off by one more
    // Example: "10" = string index 9, "20" = index 18, "30" = index 27
    cellLoc -= parseInt(pos[0]);
    let cellValue = puzzleString[cellLoc];
    if (cellValue == "0") {
        return '';
    }
    return cellValue;
}

// Fill any non-zero cells specified in the URL
var puzzString = $('#puzzle').data("input");
jQuery("input[type='text']").each(function() {
    var cellValue = getCellValue(this.name, puzzString);
    this.value = cellValue;
});