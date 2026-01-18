{
  pkgs,
  lib,
  ...
}:

{
  files = {
    ".yamllint.yaml".yaml = {
      extends = "default";
      rules = {
        document-start = "disable";
        truthy = "disable";
        comments = "disable";
        line-length.max = 120;
      };
    };
    ".ruff.toml".toml = {
      target-version = "py313";
      line-length = 120;
      lint = {
        fixable = [ "ALL" ];
        ignore = [
          "D100"
          "D105"
          "D107"
          "D212"
          "D413"
          "SIM117"
        ];
        select = [ "ALL" ];
        isort = {
          combine-as-imports = true;
        };
        per-file-ignores = {
          "test_app.py" = [
            "INP001"
            "S101"
          ];
          "__init__.py" = [
            "D104"
          ];
        };
      };
      format = {
        docstring-code-format = false;
        docstring-code-line-length = "dynamic";
        indent-style = "space";
        line-ending = "lf";
        quote-style = "double";
        skip-magic-trailing-comma = false;
      };
    };
  };

  # https://devenv.sh/basics/
  env.GREET = "devenv";

  # https://devenv.sh/packages/
  packages = with pkgs; [
    taplo
    ls-lint
    trufflehog
  ];

  # https://devenv.sh/languages/
  languages = {
    nix = {
      enable = true;
      lsp.enable = true;
    };
  };

  # https://devenv.sh/processes/
  # processes.dev.exec = "${lib.getExe pkgs.watchexec} -n -- ls -la";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/scripts/
  scripts = {
    taplo-lint.exec = ''
      echo "Running taplo"
      ${lib.getExe pkgs.taplo} --version
      ${lib.getExe pkgs.taplo} lint --default-schema-catalogs
    '';
    ls-lint-check.exec = ''
      echo "Running ls-lint"
      ${lib.getExe pkgs.ls-lint} --version
      ${lib.getExe pkgs.ls-lint}
    '';
    uv_lock_check.exec = ''
      echo "Running uv-lock"
      ${lib.getExe pkgs.uv} --version
      ${lib.getExe pkgs.uv} lock --check
    '';
    ruff-check.exec = ''
      echo "Running ruff"
      ${lib.getExe pkgs.ruff} --version
      ${lib.getExe pkgs.ruff} check --output-format sarif --output-file ruff.sarif .
    '';
  };

  # https://devenv.sh/basics/
  enterShell = ''
    git --version
  '';

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  # enterTest = ''
  #   echo "Running tests"
  #   git --version | grep --color=auto "${pkgs.git.version}"
  # '';

  # https://devenv.sh/git-hooks/
  git-hooks.hooks = {
    action-validator.enable = true;
    actionlint.enable = true;
    nixfmt.enable = true;
    check-added-large-files.enable = true;
    check-builtin-literals.enable = true;
    check-case-conflicts.enable = true;
    check-docstring-first.enable = true;
    check-json.enable = true;
    check-merge-conflicts.enable = true;
    check-python.enable = true;
    check-toml.enable = true;
    check-vcs-permalinks.enable = true;
    check-xml.enable = true;
    check-yaml.enable = true;
    comrak.enable = true;
    deadnix.enable = true;
    detect-private-keys.enable = true;
    # lychee.enable = true;
    markdownlint.enable = true;
    mixed-line-endings.enable = true;
    name-tests-test.enable = true;
    prettier.enable = true;
    python-debug-statements.enable = true;
    ripsecrets.enable = true;
    ruff.enable = true;
    ruff-format.enable = true;
    statix.enable = true;
    taplo.enable = true;
    trim-trailing-whitespace.enable = true;
    trufflehog.enable = true;
    uv-check.enable = true;
    uv-lock.enable = true;
    yamllint.enable = true;
    hadolint.enable = true;
  };

  treefmt = {
    enable = true;
    config = {
      programs = {
        ruff-format.enable = true;
        ruff-check.enable = true;
        actionlint.enable = true;
        dockfmt.enable = true;
        # dprint = {
        #   enable = true;
        #   settings = {
        #     newLineKind = "lf";
        #   };
        # };
        jsonfmt.enable = true;
        nixf-diagnose.enable = true;
        nixfmt.enable = true;
        oxipng.enable = true;
        prettier.enable = true;
        shellcheck.enable = true;
        shfmt.enable = true;
        statix.enable = true;
        taplo.enable = true;
        xmllint.enable = true;
        yamlfmt.enable = true;
      };
      settings = {
        formatter = {
          taplo-format = {
            command = "${lib.getExe pkgs.taplo}";
            options = [ "format" ];
            includes = [ "*.toml" ];
            excludes = [
              ".git/*"
              ".devenv/*"
            ];
          };
        };
      };
    };
  };
  # See full reference at https://devenv.sh/reference/options/
}
