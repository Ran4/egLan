#egLan

Easy Graphics Language (egLan): a simple graphics scripting language, built as a scripting layer on top of Python

##Installation

    git clone https://github.com/Ran4/egLan.git && cd egLan
    virtualenv --python=python2.7 .venv
    source .venv/bin/activate
    pip install -r requirements.txt


##Usage:

`python eglan.py file.eglan`

`python eglan.py -i`

###Example:

`python eglan.py testcode/test.eglan`


##Functions

*(The latest instructions can be found by typing the `help` command in the interpreter)*

    circle [X, Y, [RADIUS, [COLOR]]]]
            Draws a circle with radius RADIUS and color COLOR to position X, Y
    cls
            Clears the screen
    echo variablename
            Prints the value of a variable
    help [function]
            Shows help
    line [X, Y, [X2, Y2, [COLOR]]]
            Draws a line from (X,Y) to (X2,Y2) with color COLOR
    quit
    exit
    :q
            Quits, discarding unsaved changes
    save [FILENAME]
            Saves image to file with name filename (default: FILENAME variable)
    show
            Shows current image (without writing it to disk)
    hline [Y, [COLOR]]
    vline [X, [COLOR]]
            Draws a horizontal or vertical line with color COLOR with position X/Y
