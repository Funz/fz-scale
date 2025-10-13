# Contributing to fz-scale

Thank you for your interest in contributing to the fz-scale plugin!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Funz/fz-scale.git
   cd fz-scale
   ```

2. Install the fz framework:
   ```bash
   pip install git+https://github.com/Funz/fz.git
   ```

3. (Optional) Install SCALE for testing:
   - SCALE is proprietary software and requires a license
   - Set `SCALE_HOME` environment variable to your installation path

## Plugin Structure

```
fz-scale/
├── .fz/
│   ├── models/              # Model definitions (JSON)
│   │   ├── Scale-keno.json
│   │   ├── Scale-tsunami.json
│   │   └── Scale-xsdrnpm.json
│   └── calculators/         # Calculator scripts
│       ├── Scale-keno.sh
│       ├── Scale-tsunami.sh
│       ├── Scale-xsdrnpm.sh
│       ├── Localhost_Scale-keno.json
│       ├── Localhost_Scale-tsunami.json
│       └── Localhost_Scale-xsdrnpm.json
├── examples/                # Example input files
│   ├── Scale-keno/
│   └── example_usage.py
└── README.md
```

## Model Files (.fz/models/*.json)

Model files define:
- **Variable syntax**: How parameters are marked in input files
- **Formula syntax**: How calculated values are defined
- **Comment syntax**: How comments are marked
- **Output parsing**: Shell commands to extract results from output files

Example structure:
```json
{
    "id": "Scale-keno",
    "varprefix": "&",
    "formulaprefix": "@",
    "delim": "()",
    "commentline": "'",
    "output": {
        "variable_name": "shell command to extract value"
    }
}
```

## Calculator Scripts (.fz/calculators/*.sh)

Calculator scripts:
- Accept input file or directory as first argument
- Execute SCALE calculations
- Handle process management (PID files)
- Verify successful completion

Key requirements:
- Must be executable (`chmod +x`)
- Must handle both file and directory inputs
- Should check for SCALE installation
- Should validate output (e.g., "Congratulations" message)

## Calculator Configuration (.fz/calculators/*.json)

Calculator configuration files define:
- **Execution method**: Local shell, SSH, etc.
- **Parallelism**: Number of concurrent workers
- **Model mapping**: Which script handles which model

Example:
```json
{
    "uri": "sh://",
    "n": 1,
    "models": {
        "Scale-keno": "bash .fz/calculators/Scale-keno.sh"
    }
}
```

## Adding New Output Variables

To add a new output variable to a model:

1. Identify the pattern in SCALE output files
2. Create a shell command to extract the value
3. Add to the model's `output` section:

```json
"output": {
    "new_variable": "grep 'pattern' *.out | awk '{print $N}' 2>/dev/null || echo default_value"
}
```

Tips:
- Use `2>/dev/null` to suppress errors
- Provide a default value with `|| echo default_value`
- Use `head -1` if multiple matches are possible
- Test extraction commands manually on sample output files

## Testing

### Manual Testing

1. Create a test input file with variables
2. Run using fz:
   ```python
   import fz
   results = fz.fzr("test.inp", {"var": [1, 2, 3]}, "Scale-keno", "Localhost_Scale-keno")
   print(results)
   ```

### Testing Without SCALE

You can test the plugin structure without SCALE by:
- Using `fz.fzi()` to parse variables
- Using `fz.fzc()` to compile inputs
- Checking that model and calculator files are valid JSON

## Code Style

- Use clear, descriptive variable names
- Add comments for complex logic
- Follow existing patterns in the codebase
- Keep shell scripts POSIX-compatible when possible

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-output-variable`)
3. Make your changes
4. Test your changes (if possible)
5. Update documentation (README.md) if needed
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Questions?

- Open an issue on GitHub
- Check the [fz documentation](https://github.com/Funz/fz)
- Review existing model files for examples

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
