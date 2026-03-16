return {
  "nvim-telescope/telescope.nvim",
  dependencies = { "nvim-lua/plenary.nvim" },
  config = function()
    local builtin = require('telescope.builtin')
    
    -- Setup standar
    require('telescope').setup({
      defaults = {
        -- Biar kursor di bawah pas ngetik
        prompt_prefix = " ",
        selection_caret = " ",
      }
    })

    -- Keybind simpel buat cari file
    vim.keymap.set('n', '<leader>ff', builtin.find_files, {})
    -- Keybind buat cari teks di dalam file
    vim.keymap.set('n', '<leader>fg', builtin.live_grep, {})
  end
}
