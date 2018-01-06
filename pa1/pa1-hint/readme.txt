                      Programming Languages - Wes Weimer 
                            (Assignment Version 3)

This package shows the same simple program written in many languages. The
program reads lines from standard input and outputs them in reverse sorted
order. This is somewhat similar to what you are asked to do for PA1. 
Notably, it shows you how all of the languages handle string input, 
lists, and sorting (with higher-order functions, when applicable). 

All of the files are heavily commented. However, it is still your
responsibility to read language tutorials and documentation; this 
package will not teach you everything you need to know. 

The files are: 

readme.txt      This explanation.
example.list    Example input file 
unsort-c.c      C version
unsort-cool.cl  Cool version
unsort-js.js    JavaScript version
unsort-ml.ml    OCaml version 
unsort-py.py    Python version
unsort-rb.rb    Ruby version
unsort-hs.hs    Haskell version

Using the Ruby Version:

        $ ruby unsort-rb.rb < example.list

Using the JavaScript Version:

        $ node unsort-js.js < example.list

Using the Python Version:

        $ python unsort-py.py < example.list

Using the OCaml Version:

        $ ocaml unsort-ml.ml < example.list

Using the C Version:
        
        $ gcc -o unsort-c unsort-c.c
        $ ./unsort-c < example.list 

Using the Cool Version:

        $ cool unsort-cool.cl < example.list 

Using the Haskell Version:
        
        $ ghc -o unsort-hs unsort-hs.hs
        $ ./unsort-hs < example.list 

C is not an interpreted languages -- you have to compile it first. For our
purposes, Haskell is not an interpreted language either. 

Hint: read the C one last. It's 5-10 times larger than the others. 

All of the versions should give the same output:

        $ ocaml unsort-ml.ml < example.list
        ruby
        python
        javascript
        ocaml
        cool
        c
