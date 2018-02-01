The most tricky part for lexer is handling strings, commments, keywords. For
other tokens and lexeme, we can just use normal ways to deal with.

(1) handling strings:
We build a state machine to handle strings. Every time, regular expression
matches a r'\"', the state will transfer to "string" state. Then we need to deal
with backslashes in strings, and we found a insteresting way. We use the
regular expression to match the quote with odd and even number of backslashes before
itself. If it matches the qoute with odd number of backslashes, then we regard it is
chars construct the string. Then we re-enter the "string" state and continue
match. If it matches qoute with even number of backslashes, we think that we have
got the end of a string. Then the lexer will accept it as a string. Before the
lexer accept a string, it also need to check the size of a string, the NUL in
string, newline in string. Checking the NUL in string, we just use search the
whole string to see whether the char's ASCII value is 0. We just don't know what
NUL represents in the string. The string state machine also need to handle the
EOF, and if lexer could't find any end of a string until the EOF, it will report
the error.

(2) handling comments:
For the comments, we also need to creat a state machine to handle it. We use
the level to indicate which comment level the lexer enter and get out. If lexer
matches the '(*', increase level by 1, and if it matches '*)' decrease the level
by 1. Only when the lexer finds the level equal to 0, it go the INITIAL state
and record all the comments. Handling the eof of COMMENT, it needs to calculate
the righ line number. We need add the line number by numbers of newline (this
is also our last bug, so I think it is necessary to write down. Many people may
ignore this problem as we did). 

(3) handling keywords:
In cool, the token type of some keywords are recognized as "type", and the lexer
can't recognize them as identifier. However, those types are case insensitive
except for "true" and "false". In this situation, when judging whether it is
an identifier or type, we used the lower() to cast it into lowercase to make
sure they didn't belong to reserved tokens, which could simplify our regular
expression.

For the tasecases, I think the reason why we can pass the autograder so quickly
is that we throughly discussed all the corner cases especially cases for
'string' and comments. 

(1) tricky test cases for string:
nested strings with comments, strings has lots of backslashes, string with '\0'
(details, please see our testcase good.cl), long string which exceeds the
maximum length in cool, 

(2) tricky test for comments:
nested comments with strings, multi-level comments, comment reaches the eof

(3) tricky test for keywords:
random combination of uppercase and lowercase of keywords

(4) other test cases:
integer range, special notations, 
