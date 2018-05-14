# symbol

This web app solves Sudoku problems in the browser.

You can find a live version of this site at:
http://mmweber2.pythonanywhere.com/

Usage:

Visit grid.html and enter your puzzle numbers in the boxes, then click Submit to solve.
You can use tab or the arrow keys to move around between empty cells.
The program automatically moves to the next cell when you enter a valid number.
Cells of invalid numbers are outlined in red.

OR

Visit grid.html and append '?puzzle=text', where 'text' is the string representing your puzzle.
Use zeroes to represent empty spaces. When it receives the request, the app will automatically attempt to solve your puzzle.
If the puzzle is valid, the page will display the finished puzzle. Otherwise, it will reload the page with an error message.