/**
 * Get a list of the other elements in this line.
 *
 * For example, if pos is 1, the returned list will contain
 *  [0, 2, 3, 4, 5, 6, 7, 8].
 *
 * @param {string} pos A string of a number in the range 0-8 (inclusive)
 *                      indicating the current position.
 *
 * @return {array} A list of the other numbers in the set.
*/
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

/**
 * Search this row for duplicate elements.
 *
 * Check the rest of the row for elements that share this value.
 *
 * @param {string} pos A length-two string indicating the current position in the grid.
 * @param {list} formElements A list of form elements from the call document.forms[x].elements.
 *
 * @return {string} A length-two string indicating the position of the first duplicate found,
 *                  or undefined if no duplicates are found.
 */
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

/**
 * Search this column for duplicate elements.
 *
 * Check the rest of the column for elements that share this value.
 *
 * @param {string} pos A length-two string indicating the current position in the grid.
 * @param {list} formElements A list of form elements from the call document.forms[x].elements.
 *
 * @return {string} A length-two string indicating the position of the first duplicate found,
 *                  or undefined if no duplicates are found.
 */
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

/**
 * Search this box for duplicate elements.
 *
 * Check the rest of the box for elements that share this value.
 *
 * @param {string} pos A length-two string indicating the current position in the grid.
 * @param {list} formElements A list of form elements from the call document.forms[x].elements.
 *
 * @return {string} A length-two string indicating the position of the first duplicate found,
 *                  or undefined if no duplicates are found.
 */
function checkBox(pos, formElements) {
    let currVal = formElements.namedItem(pos).value;
    for (let box of boxSets) {
        if (!box.includes(pos)) {
            // No mapping from pos to box, so search all boxes for the right one
            continue;
        }
        for (let cell of box) {
            if (cell != pos && formElements.namedItem(cell).value == currVal) {
                return cell;
            }
        }
    }
}

/**
 * Advance focus to the next cell.
 *
 * Use the item's 'next' value to find its value and move the cursor there.
 *
 * @param {string} inputName The identifying name for the current position.
 */
function moveToNext(inputName) {
    let nextName = $('#' + inputName).data("next");
    let nextCell = document.forms[0].elements.namedItem(nextName);
    $(nextCell).focus();
}

// Pass in key.code, we want the code, not the keypress itself because we can't mimic that
function move(inputName, key) {
    let nextName;
    switch (key) {
        case "ArrowRight": // Right arrow
            // Next values are already defined, so use those
            nextName = $('#' + inputName).data("next");
            break;
        case "ArrowLeft":
            nextName = parseInt(inputName) - 1;
            if (nextName % 10 == '9') {
                // Went to the end of the previous row, so correct the index from x9 to x8
                nextName -= 1;
            }
            if (nextName < 9) {
                // Went from row 1 to row 0, so correct 'x' to '0x'
                nextName = "0" + nextName;
            }
            break;
        case "ArrowDown":
            nextName = parseInt(inputName) + 10;
            break;
        case "ArrowUp":
            nextName = parseInt(inputName) - 10;
            if (nextName < 9) {
                // Went from row 1 to row 0, so correct 'x' to '0x'
                nextName = "0" + nextName;
            }
            break;
    }
    let nextCell = document.forms[0].elements.namedItem(nextName);
    if (nextCell != undefined) {
        // If cell is undefined (up from top row, for example), ignore it
        $(nextCell).focus();
    }
}

/**
 * Perform validity checking on this cell.
 *
 * Check this cell for invalid, blank, or duplicate values and set its validity
 *  accordingly, with a specific error message if one applies.
 * The priority of the error checking is as follows:
 *  Cell is blank or contains a 0. (There is no error in this case.)
 *  Cell contains a non-digit character or multiple digits.
 *  Row contains a duplicate value.
 *  Column contains a duplicate value.
 *  Box contains a duplicate value.
 *
 * If none of the above conditions are met, set a blank (non) error message
 *  and advance focus to the next cell.
 *
 * @param {HTMLInputElement} input The cell object to check.
 * @param {string} pos The length-two string representing the current cell location.
 */
function check(input, pos) {
    if (input.value == "" || input.value == "0") {
        input.setCustomValidity('');
    }
    else if (!(["1", "2", "3", "4", "5", "6", "7", "8", "9"].includes(input.value))) {
        input.setCustomValidity('Please enter a number in the range 1-9.');
    } else {
        let formElements = document.forms[0].elements;
        let rowValid = checkRow(pos, formElements);
        if (rowValid != undefined) {
            input.setCustomValidity('This row already contains that number.');
            return;
        }
        let colValid = checkCol(pos, formElements);
        if (colValid != undefined) {
            input.setCustomValidity('This column already contains that number.');
            return;
        }
        let boxValid = checkBox(pos, formElements);
        if (boxValid != undefined) {
            input.setCustomValidity('This box already contains that number.');
            return;
        }
        // Input is fine; reset the error message
        input.setCustomValidity('');
        // Auto advance to next cell (nothing happens if already in bottom right corner)
        moveToNext(input.name);
    }
}

/**
 * Get the value for this cell.
 *
 * Given a puzzle string, find the appropriate value for the given cell.
 * pos is formatted for a 2D array and puzzleString is a single string, so the
 *  positions require translation between the two formats.
 * If puzzleString is undefined or empty, this function will return an empty string.
 *
 * @param {string} pos The position of the cell to check.
 * @param {string} puzzleString A length-81 string representing a full puzzle.
 *
 * @return {string} A single character matching pos's cell value in puzzleString,
 *                  or an empty string if that cell is blank or not specified.
 */
function getCellValue(pos, puzzleString) {
    if (puzzleString == undefined || puzzleString == "") {
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

/**
 * Check a form for validity and submit.
 *
 * The browser blocks form submission for the default submit button if there
 *  are errors in the form, but doesn't appear to do so for custom submit buttons.
 * This function does not check the input values themselves, but whether they are
 *  marked with a validity error.
 *
 * @param {string} name The name of the form to submit, as labeled in its html tag.
 */
function submitForm(name) {
    var inputs = document.getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
      if(inputs[i].type == 'text') {
          var isValid = inputs[i].checkValidity();
          if (!isValid) {
              // Reproduce browser popup if input was from a puzzle string
              inputs[i].reportValidity();
              return false;
          }
      }
    }
    $(name).submit();
}

/**
 * Check the validity of every text input field on the page.
 *
 * Scans all of the text input objects and checks their validity,
 *  marking them as appropriate.
 */
function checkAll() {
    jQuery("input[type='text']").each(function() {
        check(this, this.name);
    });
}

// When page has fully loaded:
$(function() {
    // Populate and validate cell input received from URL
    var puzzString = $('#puzzle').data("input");
    if (puzzString == "") {
        // Skip this step if there is no puzzle string (all values would be '')
        return;
    }
    jQuery("input[type='text']").each(function() {
        this.value = getCellValue(this.name, puzzString);
    });
});