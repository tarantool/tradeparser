#!/usr/bin/env tarantool

local xmlparser = require 'xmlparser'
local json = require 'json'
local tap = require('tap')

local test = tap.test('xmlparser')
test:plan(22)

local function test_iso8601(str, result)
    local ts = xmlparser.iso8601_to_timestamp(str)
    local res = os.date("!%Y-%m-%dT%TZ",ts)
    test:is(res, result, "date: " .. result)
end

local function test_xml(str, result)
    local parsed = xmlparser.parse(str, nil)
    local encoded = json.encode(parsed)

    test:is(encoded, result, "xml: " .. result)
end


test_iso8601("2017-03-30", "2017-03-30T00:00:00Z")
test_iso8601("2017-03-30T00:00:00", "2017-03-30T00:00:00Z")
test_iso8601("2017-03-05T16:52:53", "2017-03-05T16:52:53Z")
test_iso8601("2017-03-05T16:52:53Z", "2017-03-05T16:52:53Z")
test_iso8601("2017-03-05T00:00:00", "2017-03-05T00:00:00Z")
test_iso8601("2017-03-05T00:00:00+03:00", "2017-03-04T21:00:00Z")


test_xml([[
<xml>
</xml>]],
'[]')

test_xml([[
<xml>baz</xml>]],
'{"xml":"baz"}')

test_xml([[
<xml>
    <foo>
    </foo>
</xml>]],
'[]')

test_xml([[
<xml>
    <foo>qux</foo>
</xml>]],
'{"xml":{"foo":"qux"}}')

test_xml([[
<xml>
    <foo>
    </foo>
    <foo>
    </foo>
</xml>]],
'{"xml":[]}')

test_xml([[
<xml>
    <foo>frob1</foo>
    <foo>frob2</foo>
</xml>]],
'{"xml":["frob1","frob2"]}')


test_xml([[
    <Cakes>
        <cake>
        </cake>
    </Cakes>]],
    '{"Cakes":[]}')


test_xml([[
    <xml>
        <foo>
            <Type>Integer</Type>
            <Value>1</Value>
        </foo>
    </xml>]],
'{"xml":{"foo":1}}')

test_xml([[
<xml>
    <foo>
        <Type>Integer</Type>
        <Value>true</Value>
    </foo>
</xml>]],
'[]')


test_xml([[
<xml>
    <foo>
        <Type>Double</Type>
        <Value>1.2345</Value>
    </foo>
</xml>]],
'{"xml":{"foo":1.2345}}')

test_xml([[
<xml>
    <foo>
        <Type>Double</Type>
        <Value>false</Value>
    </foo>
</xml>]],
'{"xml":{"foo":0}}')


test_xml([[
<xml>
    <foo>
        <Type>Boolean</Type>
        <Value>true</Value>
    </foo>
    <foo>
        <Type>Boolean</Type>
        <Value>True</Value>
    </foo>
    <foo>
        <Type>Boolean</Type>
        <Value>NotSoTrue</Value>
    </foo>
</xml>]],
'{"xml":[true,true,false]}')

test_xml([[
<xml>
    <foo>
        <Type>String</Type>
        <Value>A nice and long ASCII string</Value>
    </foo>
    <foo>
        <Type>String</Type>
        <Value></Value>
    </foo>
</xml>]],
'{"xml":["A nice and long ASCII string",""]}')

test_xml([[
<xml>
<foo>
<Type>String</Type>
<Value>Строка с UTF-8 символами</Value>
</foo>
</xml>
]],
'{"xml":{"foo":"Строка с UTF-8 символами"}}')


test_xml([[
<xml>
<foo>
<Type>DateTime</Type>
<Value>2017-03-05T00:00:00+03:00</Value>
</foo>
<foo>
<Type>DateTime</Type>
<Value>2017-03-05T00:00:00</Value>
</foo>
<foo>
<Type>DateTime</Type>
<Value>2017-03-05</Value>
</foo>
</xml>
]],
'{"xml":[1488661200,1488672000,1488672000]}')


test_xml([[
<AssetFlow>
    <id>
        <ParameterName>Идентификатор</ParameterName>
        <ParameterNameEng>ID</ParameterNameEng>
        <Type>Integer</Type>
        <Value>28652089</Value>
        <ValueDisplayed>28652089</ValueDisplayed>
        <ValueDisplayedEng>28652089</ValueDisplayedEng>
    </id>
    <FlowType>
        <ParameterName>Тип обязательства</ParameterName>
        <ParameterNameEng>Flow Type</ParameterNameEng>
        <Type>Integer</Type>
        <Value>3</Value>
        <ValueDisplayed>Physical</ValueDisplayed>
        <ValueDisplayedEng>Physical</ValueDisplayedEng>
    </FlowType>
    <Underlying>
        <ParameterName>Инструмент</ParameterName>
        <ParameterNameEng>Instrument</ParameterNameEng>
        <Type>Integer</Type>
        <Value>194382</Value>
        <ValueDisplayed>TITIM 6 09/30/34</ValueDisplayed>
        <ValueDisplayedEng>TITIM 6 09/30/34</ValueDisplayedEng>
    </Underlying>
</AssetFlow>
]],
    '{"AssetFlow":{"FlowType":3,"Underlying":194382,"id":28652089}}')

os.exit(test:check() == true and 0 or -1)
