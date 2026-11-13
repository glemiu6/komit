{
  description = "Komit - AI-powered Git commit message generator";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f (import nixpkgs { inherit system; }));

      project = (builtins.fromTOML (builtins.readFile ./pyproject.toml)).project;

    in
    {
      packages = forAllSystems (
        pkgs:
        let
          python = pkgs.python313Packages;
          komit = python.buildPythonApplication {
            pname = project.name;
            version = project.version;
            src = ./.;

            pyproject = true;
            build-system = [ python.setuptools ];
            dependencies = with python; [
              argcomplete
              httpx
              ollama
              platformdirs
              requests
              rich
            ];

            doCheck = false;
            pythonImportsCheck = [ "komit" ];

            meta = {
              description = project.description;
              homepage = "https://github.com/glemiu6/komit";
              license = pkgs.lib.licenses.asl20;
              mainProgram = "komit";
            };
          };
        in
        {
          default = komit;
          inherit komit;
        }
      );
    };
}
