{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Python Environment
    python3Packages.python              # Explicitly include python interpreter
    python3Packages.pip

    # Core Libraries (using python3Packages for consistency)
    python3Packages.requests        # For downloading PDFs
    python3Packages.python-dotenv   # For loading .env files
    python3Packages.networkx        # For graph manipulation
    python3Packages.openai          # For LLM interaction (initial choice)

    # Visualization
    python3Packages.matplotlib
    python3Packages.pyvis

    # Development Tools from nixpkgs
    black                           # Code formatter
    ruff                            # Linter
    git

    # System dependencies (if needed by Python libs, e.g., for Pillow if used later)
    # Example: zlib, libjpeg

    # Add other development tools as needed
    # sqlitebrowser # If you decide to use SQLite later
  ];

  shellHook = ''
    echo "Entering Nix shell for Past Paper Analyzer..."
    # Set PYTHONPATH to include the src directory
    export PYTHONPATH=$(pwd)/src:$PYTHONPATH
    echo "PYTHONPATH set to: $PYTHONPATH"
    # You could add commands here to automatically create directories if they don't exist
    # mkdir -p data downloads
    # echo "Ensured data/ and downloads/ directories exist."
  '';
}
