{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell
{
    nativeBuildInputs = with pkgs; [
        (python312.withPackages (ps: [ 
            ps.pyside6
            ps.pillow
            ps.psutil
            ps.pulsectl
        ]))
    ];

    shellHook = ''
        fish
    '';
}
