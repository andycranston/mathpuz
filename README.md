# mathpuz

A web based simple maths puzzle.

## Quick start

Click on this link to play the puzzle:

[Maths Puzzle](http://cranstonhub.com/cgi-bin/mathpuz.py)

## Instructions / rules

Firstly enter a game number starting from 1 in the game number box and
click on the `Generate puzzle` button. The puzzle will be displayed. You
have to enter single digit numbers from 1 to 9 in each of the boxes in
the puzzle grid. To
help get you started one of the numbers has already been filled in
for you.

Each of the single digit numbers should be used only once.

When the puzzle is correctly completed each row and column calculation
should match the number in the box to the right of the row or the bottom
of the column.

For example if the top row looked like:

```
+---+---+---+---+---+    +----+
|   |   |   |   |   |    |    |
| 5 | * | 4 | - | 7 |    | 13 |
|   |   |   |   |   |    |    |
+---+---+---+---+---+    +----+
```

is correct because 5 multiplied by 4 is 20 and take 7 from 20
leaves the result of 13.

Note that the calulation is strict left to right for rows and top to bottom
for colunms.  For example:

```
+---+
| 3 |
+---+
| + |
+---+
| 5 |
+---+
| / |
+---+
| 2 |
+---+

+---+
| 4 |
+---+
```

is correct because 3 plus 5 is 8 and divide this by 2 leaves the
result of 4.

Strict mathematicians would say the division (/) should be
performed first because division has a higher `precedence` that addition (+)
but what do they know :-)

For the purposes of this puzzle do the sums left to right/top to bottom.

## Checking your answers

When you think you have completed the puzzle click on the `Check answers`
button. If you are correct a message:

```
You have solved the puzzle
```

will be displayed.

If the puzzle is not yet solved correctly a different message such as:

```
One or more answers are incorrect
```

will be displayed.

## I want to run this on my web server

Configure your web server to have files with the `.py` file extension
to be exectuted as CGI scripts with a Python 3 interpreter.

Copy the `mathpuz.py` and `mathpuz.css` files in the repository to a
directory on your web server that allows CGI scripts to run. You may need
to make the `mathpuz.py` file `executable` in your environment. From
a web browser enter the URL to your web server that matches where you
have copied the files to.

For example I have a web server on my network called:

```
swstore
```

The document root directory of the server is:

```
/home/andyc/www
```

and I copied the `mathpuz.py` and `mathpuz.css` files to the following
directory:

```
/home/andyc/www/projects/mathpuz
```

So the URL I enter in my web browser on my network is:

```
http://swstore/projects/mathpuz/mathpuz.py
```

## Contact me

If you have found an error in the puzzle or have ideas for improving it
you can send me an email:

```
andy [at] cranstonhub [dot] com
```

Change the [at] to @ and the [dot] to . and take out the spaces :-)

I use this form of email address on public internet pages to try and stop my
real email address from being used by spammers.

-------------------------------------------------------

End of README.md


