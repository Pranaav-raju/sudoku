# symbol

This web app solves Sudoku problems in the browser.

Usage:

Visit grid.html and enter your puzzle numbers in the boxes, then click Submit to solve.
You can use tab or the arrow keys to move around between cells.
Cells of invalid numbers will be outlined in red.

OR

Visit grid.html and append '?puzzle=text', where 'text' is the string representing your puzzle.
Use zeroes to represent empty spaces. When it receives the request, the app will automatically attempt to solve your puzzle.
If the puzzle is valid, the page will display the finished puzzle. Otherwise, it will reload the page with an error message.