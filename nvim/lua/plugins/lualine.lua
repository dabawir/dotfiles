return {
  "nvim-lualine/lualine.nvim",
  dependencies = { "nvim-tree/nvim-web-devicons" },
  config = function()
    local gray_theme = {
      normal = {
        a = { bg = '#333333', fg = '#ffffff', gui = 'bold' },
        b = { bg = '#444444', fg = '#cccccc' },
        c = { bg = '#222222', fg = '#aaaaaa' },
      },
      insert = {
        a = { bg = '#333333', fg = '#ffffff', gui = 'bold' },
        b = { bg = '#444444', fg = '#cccccc' },
        c = { bg = '#222222', fg = '#aaaaaa' },
      },
      visual = {
        a = { bg = '#333333', fg = '#ffffff', gui = 'bold' },
        b = { bg = '#444444', fg = '#cccccc' },
        c = { bg = '#222222', fg = '#aaaaaa' },
      },
    }

    require('lualine').setup({
      options = {
        theme = gray_theme,
        globalstatus = true,
        section_separators = { left = '', right = '' },
        component_separators = { left = '', right = '' },
      },
      sections = {
        lualine_a = { 'mode' },
        lualine_b = { 'branch', 'diff', 'diagnostics' },
        lualine_c = { 'filename' },
        lualine_x = { 'encoding', 'fileformat', 'filetype' },
        lualine_y = { 'progress' },
        lualine_z = { 'location' }
      }
    })
  end
}
