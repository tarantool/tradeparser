#include "rapidxml.hpp"
#include <string>
#include <list>
#include <algorithm>
#include <time.h>
#include <stdlib.h>

extern "C" {
  #include <lua.h>
  #include <lualib.h>
  #include <lauxlib.h>
  #include <tarantool/module.h>
}

static const char *prefix_array[] = {"NS1:Envelope", "NS1:Body", "ns4:WSIBConnect",
                                     "message", "body"};

static std::list<std::string> prefix(
    prefix_array,
    prefix_array + sizeof(prefix_array) / sizeof(*prefix_array));


static rapidxml::xml_document<> doc;


time_t iso8601_to_timestamp(const char* str, size_t len) {
  // parses dates like "2014-11-12T19:12:14.505Z"
  char buf[64];

  if (len >= sizeof(buf))
      return 0;

  strncpy(buf, str, len);
  buf[len] = 0;

  int res = 0;

  int y=0,M=0,d=0,h=0,m=0;
  int tz_h = 0, tz_m = 0;
  float s=0;

  res = sscanf(buf, "%d-%d-%dT%d:%d:%f+%d:%d", &y, &M, &d, &h, &m, &s, &tz_h, &tz_m);

  if (res != 3 and res != 6 and res != 8)
    return 0;

  struct tm time;

  time.tm_year = y - 1900;
  time.tm_mon = M - 1;
  time.tm_mday = d;
  time.tm_hour = h;
  time.tm_min = m;
  time.tm_sec = (int)s;
  time.tm_gmtoff = tz_h * 60 + tz_m;
  time.tm_isdst = 0;

  time_t timestamp = 0;

  if (tz_h == 0 and tz_m == 0)
    timestamp = timegm(&time);
  else
    timestamp = mktime(&time);

  return timestamp;
}

bool node_is_list(rapidxml::xml_node<>* node) {
  if (node == 0)
    return false;

  int name_size = node->name_size();
  char* name = node->name();

  if (name_size < 1)
    return false;

  rapidxml::xml_node<>* child = node->first_node();

  if (child == 0)
    return false;

  int child_name_size = child->name_size();
  char *child_name = child->name();

  if (child_name_size == name_size - 1 &&
      strncasecmp(name, child_name, child_name_size) == 0 &&
      name[child_name_size] == 's') {
    return true;
  }

  rapidxml::xml_node<>* second_child = child->next_sibling();

  if (second_child == 0)
    return false;

  int second_child_name_size = second_child->name_size();
  char *second_child_name = second_child->name();

  if (second_child_name_size != child_name_size)
    return false;

  if (strncmp(child_name, second_child_name, child_name_size) == 0)
    return true;

  return false;
}

bool node_is_value(rapidxml::xml_node<> *node) {
  if (node == 0)
    return false;

  rapidxml::xml_node<> *child = node->first_node();
  int i = 0;

  bool has_type = false;
  bool has_value = false;

  while (child != 0 && i < 10) {
    char * child_name = child->name();
    int child_name_size = child->name_size();

    if (child_name_size == strlen("Type") &&
        strncasecmp(child_name, "Type", strlen("Type")) == 0)
      has_type = true;

    if (child_name_size == strlen("Value") &&
        strncasecmp(child_name, "Value", strlen("Value")) == 0)
      has_value = true;

    child = child->next_sibling();
    i++;
  }

  if (has_type && has_value)
    return true;

  return false;
}

bool node_is_simple_value(rapidxml::xml_node<> *node) {
  if (node == 0)
    return false;

  rapidxml::xml_node<> *child = node->first_node();

  if (child == 0)
    return false;

  if (child->first_node() != 0)
    return false;

  if (child->name_size() != 0)
    return false;

  if (child->value_size() > 0)
    return true;

  return false;
}

bool add_node(struct lua_State *L, rapidxml::xml_node<> * node);
bool add_dict_node(struct lua_State *L, rapidxml::xml_node<> * node);
bool add_list_node(struct lua_State *L, rapidxml::xml_node<> * node);
bool add_value_node(struct lua_State *L, rapidxml::xml_node<> * node);
bool add_simple_value_node(struct lua_State *L, rapidxml::xml_node<> * node);

bool add_value_node(struct lua_State *L, rapidxml::xml_node<> * node) {
  char buf[64];

  if (node == 0)
    return false;

  rapidxml::xml_node<>* type = node->first_node("Type");
  rapidxml::xml_node<>* value = node->first_node("Value");

  if (type == 0 or value == 0)
    return false;

  strncpy(buf, type->value(), type->value_size());
  buf[type->value_size()] = 0;

  if (strncmp(type->value(), "Integer", type->value_size()) == 0) {
    if (value->value_size() > sizeof(buf))
      return false;

    strncpy(buf, value->value(), value->value_size());
    buf[value->value_size()] = 0;

    errno = 0;
    long val = strtol(buf, 0, 10);

    if (errno == ERANGE or errno == EINVAL)
      return false;

    lua_pushinteger(L, val);
    return true;
  }
  else if (strncmp(type->value(), "Double", type->value_size()) == 0) {
    if (value->value_size() > sizeof(buf))
      return false;


    strncpy(buf, value->value(), value->value_size());
    buf[value->value_size()] = 0;

    errno = 0;
    double val = strtod(buf, 0);
    if (errno == ERANGE or errno == EINVAL)
      return false;

    lua_pushnumber(L, val);
    return true;
  }
  else if (strncmp(type->value(), "Boolean", type->value_size()) == 0) {
    if (value->value_size() > sizeof(buf))
      return false;

    int val = 0;
    if (value->value_size() == strlen("true") &&
        strncasecmp(value->value(), "true", strlen("true")) == 0)
      val = 1;

    lua_pushboolean(L, val);
    return true;
  }
  else if (strncmp(type->value(), "String", type->value_size()) == 0) {
    lua_pushlstring(L, value->value(), value->value_size());
    return true;
  }
  else if (strncmp(type->value(), "DateTime", type->value_size()) == 0) {
    long val = iso8601_to_timestamp(value->value(), value->value_size());

    lua_pushinteger(L, val);
    return true;
  }
  return false;
}

bool add_simple_value_node(struct lua_State *L, rapidxml::xml_node<> * node) {
  if (node == 0)
    return false;

  rapidxml::xml_node<> *child = node->first_node();

  if (child == 0)
    return false;

  lua_pushlstring(L, child->value(), child->value_size());

  return true;
}


bool add_list_node(struct lua_State *L, rapidxml::xml_node<> * node) {
  if (node == 0)
    return false;

  lua_newtable(L);

  rapidxml::xml_node<> *child = node->first_node();
  int i = 1;
  while (child != 0) {
    bool res = add_node(L, child);

    if (res) {
      lua_rawseti(L, -2, i);
    }

    child = child->next_sibling();
    i++;
  }

  return true;
}

bool add_dict_node(struct lua_State *L, rapidxml::xml_node<> * node) {
  if (node == 0)
    return false;

  lua_newtable(L);

  rapidxml::xml_node<> *child = node->first_node();
  int num_children = 0;
  while (child != 0) {
    lua_pushlstring(L, child->name(), child->name_size());
    bool res = add_node(L, child);

    if (res) {
      num_children++;
      lua_settable(L, -3);
    }
    else {
      lua_pop(L, 1);
    }

    child = child->next_sibling();
  }

  if (num_children == 0) {
    lua_pop(L, 1);
    return false;
  }

  return true;
}


bool add_node(struct lua_State *L, rapidxml::xml_node<> * node) {
  if (node == 0)
    return false;

  if (node_is_simple_value(node)) {
    return add_simple_value_node(L, node);
  }

  if (node_is_value(node)) {
    return add_value_node(L, node);
  }

  if (node_is_list(node)) {
    return add_list_node(L, node);
  }

  if (node->first_node() == 0) {
    return false;
  }

  return add_dict_node(L, node);
}


extern "C" {

  static int
  parse(struct lua_State *L)
  {
    if (lua_gettop(L) == 0)
      luaL_error(L, "Usage: parse(str: string, str: path)");

    const char* path = 0;
    const char* str = lua_tostring(L, 1);

    if (str == NULL)
      luaL_error(L, "Usage: parse(str: string, str: path)");

    if (lua_gettop(L) == 2) {
      path = lua_tostring(L, 1);
      if (str == NULL)
        luaL_error(L, "Usage: parse(str: string, str: path)");
    }

    try {
      doc.parse<rapidxml::parse_non_destructive>(const_cast<char*>(str));

      rapidxml::xml_node<> *node = 0;

      node = doc.first_node();

      bool res = add_node(L, &doc);
      if (res) {
        return 1;
      }
      else {
        lua_newtable(L);
        return 1;
      }
    }
    catch (rapidxml::parse_error & ex) {
      printf("%s\n", ex.what());
    }

    return 0;
  }

  static int
  lua_iso8601_to_timestamp(struct lua_State *L)
  {
    if (lua_gettop(L) != 1)
      luaL_error(L, "Usage: parse(str: string)");

    const char* str = lua_tostring(L, 1);

    if (str == NULL)
      luaL_error(L, "Usage: parse(str: string)");

    long timestamp = iso8601_to_timestamp(str, strlen(str));

    lua_pushinteger(L, timestamp);
    return 1;
  }


  LUA_API int
  luaopen_xmlparser_lib(lua_State *L)
  {
    lua_newtable(L);
    static const struct luaL_Reg meta [] = {
      {"parse", parse},
      {"iso8601_to_timestamp", lua_iso8601_to_timestamp},
      {NULL, NULL}
    };
    luaL_register(L, NULL, meta);
    return 1;
  }
}
