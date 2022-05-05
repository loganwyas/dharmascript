# Programming Languages Spring 2022 Final Project - Logan Wyas

The language I have created is called **DHARMAScript**. This is a language that is similar to JavaScript in syntax, but is different in many other ways. To use the DHARMAScript parser, run the following command:

```
python dharma.py FILENAME
```

where `FILENAME` is the file you would like to parse.

Here are some notes about the language:

## Value Types

### Boolean

A boolean can be defined by the following:

- **Linus** - equivalent to `true` in JavaScript.
- **Gale** - equivalent to `false` in JavaScript.
- **lie** BOOL - equivalent to `not` in Python; returns the opposite value of a boolean.
- BOOL **and** BOOL - equivalent to `and` in Python; returns `Linus` if both booleans are true, and returns `Gale` otherwise.
- BOOL **or** BOOL - equivalent to `or` in Python; returns `Linus` if either boolean is true, and returns `Gale` otherwise.
- ==, >=, <=, >, and < can be used to compare two values, and it will return a boolean.

### String

A string is just any value with a quotation mark on both sides of it: `"string"`.

### Number

A number is defined as any signed number, like `15` and `4.2`.

- The +, -, \*, and / operators can be used on numbers to perform calculations.

## General Syntax

- Every file must start with `>: 4 8 15 16 23 42`.
- All lines that include an assignment or a function call must end with a "?", similar to ";" in JavaScript.

## If, Else If, and Else Statements

If statements, along with else if and else statements, have the same syntax as JavaScript. In DHARMAScript, they are written as:

```
if (BOOL) {
  # statements go here
}
else if (BOOL) {
  # more statements go here
}
else {
  # even more statements go here
}
```

## For Loops

In DHARMAScript, for loops are written as:

```
for (var? start? end? step?) {
  # statements go here
}
```

- **var** - variable to assign the loop's number count to
- **start** - the number to start at
- **end** - the number to end at
- **step**? (_optional_) - the amount that the loop's number should increase

## While Loops

While loops, similar to JavaScript, are written in DHARMAScript as:

```
while (BOOL) {
  # statements go here
}
```

## Functions

### Built-in Functions

- execute
  - Prints its arguments to the console
  - Allows unlimited arguments

### Creating Functions

The following syntax is used to create functions in DHARMAScript:

```
make functionName(arg1, arg2, ..., argN) {
  # statements go here
}
```

### Calling Functions

Calling functions is the same in DHARMAScript as it is for JavaScript. For example, if you wanted to run the `execute` function, you would type the following:
`execute("Hello World")?`
