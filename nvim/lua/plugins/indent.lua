return {
  "lukas-reineke/indent-blankline.nvim",
  main = "ibl",
  opts = {
    indent = {
      char = "│", -- Karakter garis yang mau dipakai
      tab_char = "│",
    },
    scope = { enabled = true }, -- Ini yang bikin garisnya fokus ke blok kode aktif
  },
}
