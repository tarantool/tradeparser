local clib = require('xmlparser.lib')

local function parse(a)
    return clib.parse(a)
end

return {
    parse = parse;
}
