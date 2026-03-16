return {
  "L3MON4D3/LuaSnip",
  config = function()
    local ls = require("luasnip")
    ls.add_snippets("nix", {
      ls.parser.parse_snippet("hom", "PEMBACA MASA DEPAN"),
    })
  end
}
