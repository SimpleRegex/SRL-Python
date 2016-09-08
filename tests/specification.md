# Specification

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

    >>> from srl.builder import Builder
    >>> builder = Builder()
    >>> query = builder.letter('a', 'f').exactly(4)
    >>> print query.get()
    [a-f]{4}
    >>> query.is_matching('abcd')
    True

Okay, let's dive into the different characters. Below, you can find a list of all available characters along with an example query.

### literally

    literally "string"

The `literally` character allows you to pass a string to the query that will be interpreted as exactly what you've requested. Nothing else will match, besides your string. Any special character will automatically be escaped. The sample code matches, since the test string contains "sample". Try removing it.

    >>> builder = Builder()
    >>> query = builder.literally("sample")
    >>> print query.get()
    (?:sample)
    >>> query.findall('this is a sample')
    ['sample']
    >>> query.findall('this is a maplecady')
    []

### one of

    one of "characters"

`literally` comes in handy if the string is known. But if there is a unknown string which may only contain certain characters, using `one of` makes much more sense. This will match one of the supplied characters.

    >>> builder = Builder()
    >>> query = builder.one_of('a%1')
    >>> print query.get()
    [a\%1]
    >>> query.is_matching('%')
    True
    >>> query.is_matching('$')
    False

### letter

    letter [from a to z]

This will help you to match a letter between a specific span, if the exact word isn't known. If you know you're expecting an letter, then go for it. If not supplying anything, a normal letter between a and z will be matched. Of course, you can define a span, using the `from x to y` syntax.

Please note, that this will only match one letter. If you expect more than one letter, use a quantifier.

    >>> builder = Builder()
    >>> query = builder.letter('a', 'f')
    >>> print query.get()
    [a-f]
    >>> query.is_matching('a')
    True
    >>> query.is_matching('z')
    False

### any character

    any character

Just like a letter, `any character` matches anything between A to Z, 0 to 9 and `_`, case insensitive. This way you can validate if someone for example entered a valid username.

    >>> builder = Builder()
    >>> query = builder.starts_with().any_character().once_or_more().must_end()
    >>> print query.get()
    ^\w+$
    >>> query.is_matching('aBcD0_1')
    True

### no character

    no character

The inverse to the any character-character is no character. This will match everything except a to z, A to Z, 0 to 9 and `_`.

    >>> builder = Builder()
    >>> query = builder.starts_with().no_character().once_or_more().must_end()
    >>> print query.get()
    ^\W+$
    >>> query.is_matching('/+$!')
    True
    >>> query.is_matching('azAZ09_')
    False

### digit

    digit [from 0 to 9]

When expecting a digit, but not a specific one, this comes in handy. Each digit matches only one digit, meaning you can only match digit from 0 to 9, but multiple times using a quantifier. Obviously, limiting the digit isn't a problem either. So if you're searching for a number from 5 to 7, go for it!

Note: `number` is an alias for `digit`.

    >>> builder = Builder()
    >>> query = builder.starts_with().digit(5, 7).exactly(2).must_end()
    >>> print query.get()
    ^[5-7]{2}$
    >>> query.is_matching('42')
    False
    >>> query.is_matching('56')
    True

### anything

    anything

Any character whatsoever. Well.. except for line breaks. This will match any character, except new lines. And, of course, only once. So don't forget to apply a quantifier, if necessary.

    >>> builder = Builder()
    >>> query = builder.anything()
    >>> print query.get()
    .
    >>> query.is_matching('a')
    True
    >>> query.is_matching('\n')
    False

### new line

    new line

Match a new line.

    >>> builder = Builder()
    >>> query = builder.new_line()
    >>> print query.get()
    \n
    >>> query.is_matching('\n')
    True

### [no] whitespace

    [no] whitespace

This matches any whitespace character. This includes a space, tab or new line. If using no whitespace everything except a whitespace character will match.

    >>> query = Builder().whitespace()
    >>> print query.get()
    \s
    >>> query.is_matching(' ')
    True
    >>> query = Builder().no_whitespace()
    >>> print query.get()
    \S
    >>> query.is_matching('y')
    True

### tab

    tab

If you want to match tabs, but no other whitespace characters, this might be for you. It will only match the tab character, and nothing else.

    >>> builder = Builder()
    >>> query = builder.tab()
    >>> print query.get()
    \t
    >>> query.is_matching('\t')
    True
    >>> not query.is_matching('    ')
    True

### raw

    raw "expression"

Sometimes, you may want to enforce a specific part of a regular expression. You can do this by using raw. This will append the given string without escaping it.

    >>> builder = Builder()
    >>> query = builder.literally('an').whitespace().raw('[a-zA-Z]')
    >>> print query.get()
    (?:an)\s[a-zA-Z]
    >>> query.is_matching('an Example')
    True

## Quantifiers

Quantifiers are probably one of the most important things here. If you've specified a character or a group in you query and now want to multiply it, you don't have to copy and paste all of it. Just tell them.

Oh, and don't be confused. Sometimes, you may find that these quantifiers don't match with the tinkered example. That's okay, since we're not forcing the string to start or end. Thus, even if only parts of that string are matching, the expression will be valid.

### exactly x times

    exactly x times

You're sure. You don't guess, you dictate. `exactly 4 times`. Not more, not less. The statement before has to match exactly x times.

Note: since `exactly x times` is pretty much to write, short terms exist. Instead of `exactly 1 time`, you can write `once`, and for 2, take `twice`.

    >>> builder = Builder()
    >>> query = builder.digit().exactly(3).letter().twice()
    >>> print query.get()
    [0-9]{3}[a-z]{2}
    >>> query.is_matching('123ab')
    True

### between x and y times

    between x and y times

For a specific number of repetitions between a span of x to y, you may use this quantifier. It will make sure the previous character exists between x and y times.

Note: since `between x and y times` is pretty much to write, you can get rid of the times: `between 1 and 5`

    >>> builder = Builder()
    >>> query = builder.starts_with().digit().between(3, 5).letter().twice()
    >>> print query.get()
    ^[0-9]{3,5}[a-z]{2}
    >>> query.is_matching('1234ab')
    True

### optional

    optional

You can't always be sure that something exists. Sometimes it's okay if something is missing. In that case, the optional quantifier comes in handy. It will match, if it's there, and ignore it, if it's missing.

    >>> builder = Builder()
    >>> query = builder.digit().optional().letter().twice()
    >>> print query.get()
    [0-9]?[a-z]{2}
    >>> query.is_matching('ab')
    True

### once/never or more

    once/never or more

If something has to exist at least once, or never, but if it does, then it may exist multiple times, the quantifiers `once or more` and `never or more` will do the job.

    >>> builder = Builder()
    >>> query = builder.starts_with().letter().once_or_more().must_end()
    >>> print query.get()
    ^[a-z]+$
    >>> query.is_matching('abcdefghijklmnopqrstuvwxyz')
    True

### at least x times

    at least x times

Something may exist in an infinite length, but must exist at least x times.

    >>> builder = Builder()
    >>> query = builder.letter().at_least(10)
    >>> print query.get()
    [a-z]{10,}
    >>> query.is_matching('invalid')
    False
    >>> query.is_matching('nowthisisvalid')
    True

## Groups

Groups are a powerful tool of regular expressions. You can capture matches, join or summarize them.

To make things easier for you, think of groups as sub-queries. Everything in between a group could be a standalone expression which will later be combined.

Every group allows you to supply either a sub-query using parentheses, or just a literal string using quotes instead.

### capture ... as

    capture (condition) [as "name"]

To go beyond simply validating input, a capture group comes in handy. You can capture any condition and return it by the engine. This helps you to filter inputs and only get the parts you care about.

If you're trying to get more than one match, capture names are useful, too. This is completely optional, but you can supply a name for a capture group using the as "name" syntax.

    >>> builder = Builder()
    >>> query = builder.capture(lambda q: q.anything().once_or_more(), 'first').literally(' - ').capture('second part', 'second')
    >>> print query.get()
    (?P<first>.+)(?:\ \-\ )(?P<second>(?:second\ part))
    >>> query.is_matching('first part - second part')
    True
    >>> query.get_matches('first part - second part')
    ['first part', 'second part']

### any of

    any of (condition)

If you're not exactly sure which part of the condition will match, use any of. Every statement you supply in that sub-query, could be a match.

As you can see, you can feel free to nest multiple groups and even parentheses. If you would have removed the parentheses around the `digit once or more`, the expression would be invalid, since you can't match either a digit, or "once or more".

Note: `either of` is a synonym of `any of`.

    >>> builder = Builder()
    >>> query = builder.capture(lambda q: q.any_of(lambda q: q.literally('sample') & (lambda q: q.digit().once_or_more())))
    >>> print query.get()
    ((?:(?:sample)|(?:[0-9]+)))
    >>> query.is_matching('sample')
    True
    >>> query.is_matching('1234')
    True

### until

    until (condition)

Sometimes you want to match or capture a specific expression until some other condition meets. This can be achieved using the until group.

In the example below, we'll provide a string as a condition. However, this would work as well using a more complex expression, just like above.

    >>> builder = Builder()
    >>> query = builder.begin_with().capture(lambda q: q.anything().once_or_more()).until('m')
    >>> print query.get()
    ^(.+?)(?:m)
    >>> query.is_matching('this is an exam')
    True
    >>> query.is_matching('this is an example')
    True

### if followed by / if not followed by

    if [not] followed by

Sometimes, you may only want to match a certain condition if it is directly followed by a given other condition.

This can be done using lookahead. In SRL, a lookahead can be positive (if followed by) or negative (if not followed by). The example below will only capture the number, if it's no more followed by any other number.

    >>> builder = Builder()
    >>> query = builder.capture(lambda q: q.digit()).if_not_followed_by(lambda q: q.anything().once_or_more().digit())
    >>> print query.get()
    ([0-9])(?!.+[0-9])
    >>> query.get_matches('This example contains 3 numbers. 2 should not match. Only 1 should.')
    ['1']

### if already had / if not already had

    if [not] already had

Just like a lookahead, the lookbehind, which can be positive and negative as well, matches the characters exactly before that condition.

For example, you may only want to match bar if it's directly following foo:

    >>> builder = Builder()
    >>> query = builder.capture('bar').if_already_had('foo')
    >>> print query.get()
    (?<=(?:foo))((?:bar))
    >>> query.get_matches('foobar')
    ['bar']
