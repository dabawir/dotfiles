{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    gcc
    gnumake
    pkg-config
  ];

  buildInputs = with pkgs; [
    libX11
    libXft
    libXinerama
    fontconfig
    alacritty
  ];

  shellHook = ''
    echo "--- Lab SIMBLE: Simple Stable Window Manager ---"
    echo "Ketik 'make' buat compile, 'make run' buat ngetes di Xephyr."
  '';
}
