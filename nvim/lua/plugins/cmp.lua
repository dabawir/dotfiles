return {
  "hrsh7th/nvim-cmp",
  dependencies = {
    "hrsh7th/cmp-nvim-lsp",
    "hrsh7th/cmp-buffer",
    "hrsh7th/cmp-path",
    "L3MON4D3/LuaSnip",
    "onsails/lspkind.nvim", -- Biar ada ikon di menu
  },
  config = function()
    local cmp = require("cmp")
    local lspkind = require("lspkind")

    cmp.setup({
      snippet = { expand = function(args) require("luasnip").lsp_expand(args.body) end },
      formatting = {
        format = lspkind.cmp_format({ mode = 'symbol_text', menu = ({ buffer = "[Buf]", luasnip = "[Snip]" }) }),
      },
      mapping = cmp.mapping.preset.insert({
        ['<C-Space>'] = cmp.mapping.complete(), -- Panggil menu manual
        ['<CR>'] = cmp.mapping.confirm({ select = true }),
      }),
      sources = cmp.config.sources({
        { name = 'luasnip' }, -- Utamakan snippet kamu
        { name = 'nvim_lsp' },
        { name = 'buffer' }, -- Ini yang bikin dia tebak kata dari file
        { name = 'path' },
      })
    })
  end
}
