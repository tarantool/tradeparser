local clib = require('xmlparser.lib')

local function parse(a)
    return clib.parse(a)
end

return {
    parse = clib.parse,
    iso8601_to_timestamp = clib.iso8601_to_timestamp
}
