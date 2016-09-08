SRL.py
======

A Python Implementation of [Simple Regex](https://simple-regex.com/).

## How to install

    $ pip install srl

## How to use

    >>> from srl import SRL
    >>> regex_object = SRL('digit exactly 3 times')
    >>> matched = regex_object.search('123') # Exactly same API with class re.RegexObject
    >>> matched.group()
    '123'

## How to test

    $ pip install nose
    $ nosetests -c ./nose.cfg

## Documentation Overview

This is the documentation space for the SRL Query Language. We're trying our best to give you a complete overview about what's possible. Please read through these basic syntax rules first:

SRL is case insensitive. Thus, `LITERALLY "test"` is exactly the same as `literally "test"`. But please beware, that everything inside a string is in fact case sensitive. `LITERALLY "TEST"` does NOT equal `literally "test"`.
The comma separating statements is completely optional and has no effect whatsoever. In fact, it gets removed before interpreting. But since it helps the human eye to distinct between different statements, it's allowed.
Strings are interpreted as literal characters and will be escaped. They can either be defined using 'single' or "double" quotation marks. Escaping them using a backslash is possible as well.
Parentheses should only be used when building a sub-query, for example while using a capture or non-capture group to, for example, apply a quantifier to multiple items.
Comments are currently not supported and may be implemented in the future.
In the navigation on the left you can find a few main groups in which all commands can be divided. A short explanation for each group would be:

Characters are everything that matches the string directly. This group contains `letter`, `digit` and `literally`.
Quantifiers are quantifying the statement before. They indicate how often something is allowed to occur.
Groups basically group characters and quantifiers. They are used for applying quantifiers to a whole pattern or to capture and return some specific expressions. Everything in between these groups can be seen as a sub-query.
Lookarounds allow a more complex way of dealing with groups and matches. That way you can define a group to match only if a certain pattern will apply.
Flags apply to the complete query and indicate a specific mode. For instance, setting the `case insensitive` flag, will tell the whole query to ignore case mismatches.
Anchors are pretty easy. They define whether a string must start or end now.

## Characters

Characters are everything that matches the string directly. They are the groundwork to which quantifiers will apply. The syntax always looks as follows:

    character [specification] [quantifier] [others]

As you can see, characters always come first. They start a new statement, and everything that follows defines the previous character. Some characters allow a specification: `letter`, for example, allows you to define a span of allowed letters: `from a to f`

Every character or character set can be quantified. You may want to match exactly four letters `from a to f`. This would match abcd, but not abcg. You can do that by supplying `exactly 4 times` as a quantifier:

SRL Builder:

    >>> srl = SRL('letter from a to f exactly 4 times')
    >>> print srl
    [a-f]{4}
    >>> bool(srl.match('abcd'))
    True

Okay, let's dive into the different characters. Below, you can find a list of all available characters along with an example query.

### literally

    literally "string"

The `literally` character allows you to pass a string to the query that will be interpreted as exactly what you've requested. Nothing else will match, besides your string. Any special character will automatically be escaped. The sample code matches, since the test string contains "sample". Try removing it.

    >>> srl = SRL('literally "sample"')
    >>> print srl
    (?:sample)
    >>> srl.findall('this is a sample')
    ['sample']
    >>> srl.findall('this is a maplecady')
    []

### one of

    one of "characters"

`literally` comes in handy if the string is known. But if there is a unknown string which may only contain certain characters, using `one of` makes much more sense. This will match one of the supplied characters.

    >>> srl = SRL('one of "a%1"')
    >>> print srl
    [a\%1]
    >>> bool(srl.match('%'))
    True
    >>> bool(srl.match('$'))
    False

### letter

    letter [from a to z]

This will help you to match a letter between a specific span, if the exact word isn't known. If you know you're expecting an letter, then go for it. If not supplying anything, a normal letter between a and z will be matched. Of course, you can define a span, using the `from x to y` syntax.

Please note, that this will only match one letter. If you expect more than one letter, use a quantifier.

    >>> srl = SRL('letter from a to f')
    >>> print srl
    [a-f]
    >>> bool(srl.match('a'))
    True
    >>> bool(srl.match('z'))
    False

### uppercase letter

    uppercase letter [from A to Z]

This of course behaves just like the normal letter, with the only difference, that uppercase letter only matches letters that are written in uppercase. Of course, if the case insensitive flag is applied to the query, these two act completely the same.

    >>> srl = SRL('uppercase letter from A to F')
    >>> print srl
    [A-F]
    >>> bool(srl.match('E'))
    True

### any character

    any character

Just like a letter, `any character` matches anything between A to Z, 0 to 9 and `_`, case insensitive. This way you can validate if someone for example entered a valid username.

    >>> srl = SRL('starts with any character once or more, must end')
    >>> print srl
    ^\w+$
    >>> bool(srl.match('aBcD0_1'))
    True

### no character

    no character

The inverse to the any character-character is no character. This will match everything except a to z, A to Z, 0 to 9 and `_`.

    >>> srl = SRL('starts with no character once or more, must end')
    >>> print srl
    ^\W+$
    >>> bool(srl.match('/+$!'))
    True
    >>> bool(srl.match('azAZ09_'))
    False

### digit

    digit [from 0 to 9]

When expecting a digit, but not a specific one, this comes in handy. Each digit matches only one digit, meaning you can only match digit from 0 to 9, but multiple times using a quantifier. Obviously, limiting the digit isn't a problem either. So if you're searching for a number from 5 to 7, go for it!

Note: `number` is an alias for `digit`.

    >>> srl = SRL('starts with digit from 5 to 7 exactly 2 times, must end')
    >>> print srl
    ^[5-7]{2}$
    >>> bool(srl.match('42'))
    False
    >>> bool(srl.match('56'))
    True

### anything

    anything

Any character whatsoever. Well.. except for line breaks. This will match any character, except new lines. And, of course, only once. So don't forget to apply a quantifier, if necessary.

    >>> srl = SRL('anything')
    >>> print srl
    .
    >>> bool(srl.match('any-% th1ng!'))
    True

### new line

    new line

Match a new line.

    >>> srl = SRL('new line')
    >>> print srl
    \n
    >>> bool(srl.match('\n'))
    True

### [no] whitespace

    [no] whitespace

This matches any whitespace character. This includes a space, tab or new line. If using no whitespace everything except a whitespace character will match.

    >>> srl = SRL('whitespace')
    >>> print srl
    \s
    >>> bool(srl.match(' '))
    True

    >>> srl = SRL('no whitespace')
    >>> print srl
    \S
    >>> bool(srl.match('y'))
    True

### tab

    tab

If you want to match tabs, but no other whitespace characters, this might be for you. It will only match the tab character, and nothing else.

    >>> srl = SRL('tab')
    >>> print srl
    \t
    >>> bool(srl.match('\t'))
    True
    >>> bool(srl.match(' '))
    False

### raw

    raw "expression"

Sometimes, you may want to enforce a specific part of a regular expression. You can do this by using raw. This will append the given string without escaping it.

    >>> srl = SRL('literally "an", whitespace, raw "[a-zA-Z]"')
    >>> print srl
    (?:an)\s[a-zA-Z]
    >>> bool(srl.match('an Example'))
    True

## Quantifiers

Quantifiers are probably one of the most important things here. If you've specified a character or a group in you query and now want to multiply it, you don't have to copy and paste all of it. Just tell them.

Oh, and don't be confused. Sometimes, you may find that these quantifiers don't match with the tinkered example. That's okay, since we're not forcing the string to start or end. Thus, even if only parts of that string are matching, the expression will be valid.

### exactly x times

    exactly x times

You're sure. You don't guess, you dictate. `exactly 4 times`. Not more, not less. The statement before has to match exactly x times.

Note: since `exactly x times` is pretty much to write, short terms exist. Instead of `exactly 1 time`, you can write `once`, and for 2, take `twice`.

    >>> srl = SRL('digit exactly 3 times, letter twice')
    >>> print srl
    [0-9]{3}[a-z]{2}
    >>> bool(srl.match('123ab'))
    True

### between x and y times

    between x and y times

For a specific number of repetitions between a span of x to y, you may use this quantifier. It will make sure the previous character exists between x and y times.

Note: since `between x and y times` is pretty much to write, you can get rid of the times: `between 1 and 5`

    >>> srl = SRL('starts with digit between 3 and 5 times, letter twice')
    >>> print srl
    ^[0-9]{3,5}[a-z]{2}
    >>> bool(srl.match('1234ab'))
    True

### optional

    optional

You can't always be sure that something exists. Sometimes it's okay if something is missing. In that case, the optional quantifier comes in handy. It will match, if it's there, and ignore it, if it's missing.

    >>> srl = SRL('digit optional, letter twice')
    >>> print srl
    [0-9]?[a-z]{2}
    >>> bool(srl.match('ab'))
    True

### once/never or more

    once/never or more

If something has to exist at least once, or never, but if it does, then it may exist multiple times, the quantifiers `once or more` and `never or more` will do the job.

    >>> srl = SRL('starts with letter once or more, must end')
    >>> print srl
    ^[a-z]+$
    >>> bool(srl.match('abcdefghijklmnopqrstuvwxyz'))
    True

### at least x times

    at least x times

Something may exist in an infinite length, but must exist at least x times.

    >>> srl = SRL('letter at least 10 times')
    >>> print srl
    [a-z]{10,}
    >>> bool(srl.match('invalid'))
    False
    >>> bool(srl.match('nowthisisvalid'))
    True

## Groups

Groups are a powerful tool of regular expressions. You can capture matches, join or summarize them.

To make things easier for you, think of groups as sub-queries. Everything in between a group could be a standalone expression which will later be combined.

Every group allows you to supply either a sub-query using parentheses, or just a literal string using quotes instead.

### capture ... as

    capture (condition) [as "name"]

To go beyond simply validating input, a capture group comes in handy. You can capture any condition and return it by the engine. This helps you to filter inputs and only get the parts you care about.

If you're trying to get more than one match, capture names are useful, too. This is completely optional, but you can supply a name for a capture group using the as "name" syntax.

    >>> srl = SRL('capture (anything once or more) as "first", literally " - ", capture "second part" as "second"')
    >>> print srl
    (?P<first>.+)(?:\ \-\ )(?P<second>(?:second\ part))
    >>> bool(srl.match('first part - second part'))
    True
    >>> srl.findall('first part - second part')
    [('first part', 'second part')]

### any of

    any of (condition)

If you're not exactly sure which part of the condition will match, use any of. Every statement you supply in that sub-query, could be a match.

As you can see, you can feel free to nest multiple groups and even parentheses. If you would have removed the parentheses around the `digit once or more`, the expression would be invalid, since you can't match either a digit, or "once or more".

Note: `either of` is a synonym of `any of`.

    >>> srl = SRL('capture (any of (literally "sample", (digit once or more)))')
    >>> print srl
    ((?:(?:sample)|(?:[0-9]+)))
    >>> bool(srl.match('sample'))
    True
    >>> bool(srl.match('1234'))
    True

### until

    until (condition)

Sometimes you want to match or capture a specific expression until some other condition meets. This can be achieved using the until group.

In the example below, we'll provide a string as a condition. However, this would work as well using a more complex expression, just like above.

    >>> srl = SRL('begin with capture (anything once or more) until "m"')
    >>> print srl
    ^(.+?)(?:m)
    >>> bool(srl.match('this is an example'))
    True

### if followed by / if not followed by

    if [not] followed by

Sometimes, you may only want to match a certain condition if it is directly followed by a given other condition.

This can be done using lookahead. In SRL, a lookahead can be positive (if followed by) or negative (if not followed by). The example below will only capture the number, if it's no more followed by any other number.

    >>> srl = SRL('capture (digit) if not followed by (anything once or more, digit)')
    >>> print srl
    ([0-9])(?!.+[0-9])
    >>> srl.findall('This example contains 3 numbers. 2 should not match. Only 1 should.')
    ['1']

### if already had / if not already had

    if [not] already had

Just like a lookahead, the lookbehind, which can be positive and negative as well, matches the characters exactly before that condition.

For example, you may only want to match bar if it's directly following foo:

    >>> srl = SRL('capture "bar" if already had "foo"')
    >>> print srl
    (?<=(?:foo))((?:bar))
    >>> srl.search('foobar').group()
    'bar'

## Flags

Flags apply to the whole expression generated and can be included at any point. It mostly makes sense to either add them on the beginning or the end of the query to not confuse the reader.

### case insensitive

    case insensitive

By default, regular expressions are case sensitive. That means, if you supply something like letter or literally it's important that the case matches. literally "foo" won't match FOO. Using the case insensitive flag however, will tell the engine to ignore case mismatches.

    >>> srl = SRL('letter from a to b twice, case insensitive')
    >>> print srl
    [a-b]{2}
    >>> import re
    >>> srl.flags == re.IGNORECASE
    True
    >>> bool(srl.match('Ab'))
    True

### multi line

    multi line

If you want to match more than one line, supply the multi line flag. This will make the must end and begin with anchors

match the end/beginning of one line, instead of the complete string.

    >>> srl = SRL('begin with literally "a"')
    >>> srl.findall('a book\na tree')
    ['a']
    >>> srl = SRL('begin with literally "a" multi line')
    >>> srl.findall('a book\na tree')
    ['a', 'a']

### all lazy

    all lazy

Matching in regular expression is greedy by default, meaning it will try to match the last occurrence. You can force this on a single quantifier by using the first match statement. If you want this to apply to the whole expression, use all lazy.

In the example below, you can see that each letter is a new match. If you try removing the all lazy flag, it will match until the end of the word.

    >>> srl = SRL('capture (letter once or more) all lazy')
    >>> print srl
    ([a-z]+?)
    >>> srl.findall('this is a sample')
    ['t', 'h', 'i', 's', 'i', 's', 'a', 's', 'a', 'm', 'p', 'l', 'e']

## Anchors

Anchors help us to enforce the beginning or ending of a string or line and make sure that the expression will only match if everything is covered, instead of just parts of the string to test.

### begin/starts with

begin with / starts with
Forcing the string to start is probably most of the time a great idea. For example, try matching an email address. You certainly don't want to match @my@email.com just because a part of it is correct.

But try for yourself. Remove the starts with anchor and play around.

Note: begin with is a synonym and behaves just like starts with.

    >>> srl = SRL('starts with literally "match"')
    >>> print srl
    ^(?:match)
    >>> bool(srl.match('no match!'))
    False
    >>> bool(srl.match('match!'))
    True

### must end

    must end

Just like the above, you often want to force the string to end. must end will stop matching if the string does not end after the given match.


    >>> srl = SRL('literally "match" must end')
    >>> print srl
    (?:match)$
    >>> bool(srl.match('match!'))
    False
    >>> bool(srl.match('match'))
    True
