{ pkgs ? import <nixos> {} }:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python310Packages.discordpy
    python310Packages.ffmpeg-python
    python310Packages.yt-dlp
    python310Packages.requests
  ];
}

