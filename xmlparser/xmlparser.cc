#include "rapidxml.hpp"

static rapidxml::xml_document<> doc;

extern "C" {
  #include <lua.h>
  #include <lualib.h>
  #include <lauxlib.h>
  #include <tarantool/module.h>

  static int
  parse(struct lua_State *L)
  {
    if (lua_gettop(L) != 1)
      luaL_error(L, "Usage: parse(str: string)");

    const char* str = lua_tostring(L, 1);

    if (str == NULL)
      luaL_error(L, "Usage: parse(str: string)");

    try {
      doc.parse<rapidxml::parse_non_destructive>(const_cast<char*>(str));

      rapidxml::xml_node<> *node = 0;

      node = doc.first_node("foobar");

      //printf("%s\n", str);
    }
    catch (rapidxml::parse_error & ex) {
      printf("%s\n", ex.what());
    }



    lua_pushinteger(L, 1);
    return 1;
  }

  LUA_API int
  luaopen_xmlparser_lib(lua_State *L)
  {
    lua_newtable(L);
    static const struct luaL_reg meta [] = {
      {"parse", parse},
      {NULL, NULL}
    };
    luaL_register(L, NULL, meta);
    return 1;
  }
}
