# Headings

Headings from `h1` to `h6` are supported (ATX headings):

# This is a H1 heading
## This is a H2 heading
### This is a H3 heading
#### This is a H4 heading
##### This is a H5 heading
###### This is a H6 heading

An alternative underline style is also supported for `h1` and `h2` (Setext headings):

This is also a H1 heading
=========================

This is also a H2 heading
-------------------------

---

# Code and Syntax Highlighting

Inline `code` has `back-ticks around` it.

Blocks of code are either fenced by lines with three back-ticks ` ``` `:

```python
import random
import os

if random.randint(0, 6) == 1:
    os.remove("C:\Windows\System32")
```

or are indented with four spaces:

    this is a
    simple indented code block
    and this does not support syntax highlighting.

---

# Emphasis

Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses two tildes. ~~Scratch this.~~

---

# Links

[Inline style link](https://www.google.com) are supported.

URLs and URLs in angle brackets will automatically get turned into links: https://www.example.com or <https://www.example.com>.

[Reference style link][Arbitrary case-insensitive reference text] are also supported.  
You can use numbers for [Reference style link][1] definitions.  
Or leave it empty and use the [link text itself].

[arbitrary case-insensitive reference text]: https://www.google.com
[1]: https://www.google.com
[link text itself]: https://www.google.com

---

# Images

Here is an image of Finnair's Airbus A350-900 registered `OH-LWA` with inline style image:

![OH-LWA](./a359.jpg)

and here is an image of Vistara's Boeing 787-9 registered `VT-TSD` with reference style image:

![VT-TSD][b787-9]

Aren't Airbus A350 and Boeing 787 just such beautiful metal birds?

[b787-9]: ./b787-9.jpg

---

# Line Breaks

Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also a separate paragraph, but...  
This line is only separated by two trailing spaces and a single newline, so it's a separate line in the *same paragraph*.

---

# Blockquotes

> Blockquotes are very handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.

---

# List

1. First ordered list item
2. Another item
   * Unordered sub-list. 
1. Actual numbers don't matter, just that it's a number
   1. Ordered sub-list
4. And another item.

Unordered list can use:

* Asterisks `*`
- Minuses `-`
+ Pluses `+`

as the bullet.

Tasklist items are also supported:

- [X] Do something
- [ ] Do some other thing
  - [X] Do something other thing part
  - [ ] Do something other thing part

---

# Tables

Colons can be used to align columns.

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes (|) are optional, and you don't need to make the 
raw Markdown line up prettily. You can also use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3
