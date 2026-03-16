-- for keybinds
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- init lua
require("config.lazy")
require("plugins.lualine")

-- garis penanda
vim.opt.number = true
vim.opt.cursorline = true

--fungsi tab dan dasar lain
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true
vim.opt.smartindent = true
vim.opt.encoding = 'utf-8'



--keymaps for telescope OR for other keybind
local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>ff', builtin.find_files, {}) -- Cari file
vim.keymap.set('n', '<leader>fg', builtin.live_grep, {})  -- Cari teks di dalam file
vim.keymap.set('n', '<leader>fb', builtin.buffers, {})    -- Cari buffer yang buka
