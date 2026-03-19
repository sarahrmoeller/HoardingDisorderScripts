{
  description = "Python development environment";

  nixConfig = {
    extra-substituters = "https://nixpkgs-python.cachix.org";
    extra-trusted-public-keys = "nixpkgs-python.cachix.org-1:hxjI7pFxTyuTHn2NkvWCrAUcNZLNS3ZAvfYNuYifcEU=";
  };

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    nixpkgs-python.url = "github:cachix/nixpkgs-python";
  };

  outputs = { self, nixpkgs, nixpkgs-python }: 
    let
      system = "x86_64-linux";
      # system = "x86_64-rwin";

      pythonVersion = "3.10.19";


      pkgs = import nixpkgs { inherit system; };
      myPython = nixpkgs-python.packages.${system}.${pythonVersion};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          myPython
        ];
        shellHook = ''
          python --version
          exec zsh
        '';
      };
    };
}
