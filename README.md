# Fast specialized XML trade parser

## Deprecation note

This is not a general purpose module: the parser is specialized for particular
input XML format. We suggest more general [luarapidxml][luarapidxml] solution.

[luarapidxml]: https://github.com/tarantool/luarapidxml

## Overview

This parser consumes equity trades in a proprietory format and turns
them into Lua dictionaries. The primary feature of this parser is
speed. It can do 200 MB/sec on a single CPU core.

Example input:

```xml
<root>
    <value1>
        <Type>Integer</Type>
        <Value>1</Value>
    </value1>
    <value2>
        <Type>Double</Type>
        <Value>1.2345</Value>
    </value2>
    <value3>
        <Type>Boolean</Type>
        <Value>true</Value>
    </value3>
    <value4>
        <Type>String</Type>
        <Value>Строка в UTF-8</Value>
    </value4>
    <value5>
        <Type>DateTime</Type>
        <Value>2017-03-05T00:00:00+03:00</Value>
    </value5>
    <a_list>
      <item>foo</item>
      <item>bar</item>
      <item>qux</item>
    </a_list>
</root>
```

Example output:

```json
{
  "root": {
    "value1": 1,
    "value2": 1.2345,
    "value3": true,
    "value4": "Строка в UTF-8",
    "value5": 1488661200,
    "a_list": [
      "foo",
      "bar",
      "qux"
    ]
  }
}
```

## Usage

```lua
local parser = require('tradeparser')
local json = require('json')

local xmltext = io.open("example.xml", "r"):read("*a")

local root = parser.parse(xmltext)
print(json.encode(root))
```
