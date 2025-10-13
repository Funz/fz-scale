# Migration Guide: From plugin-scale to fz-scale

This document explains the changes from the old Java-based `plugin-scale` to the new Python-based `fz-scale`.

## Overview of Changes

The plugin has been completely restructured to work with the modern [fz](https://github.com/Funz/fz) framework:

### Old Structure (plugin-scale)
```
plugin-scale/
├── src/
│   ├── main/
│   │   ├── io/
│   │   │   ├── Scale-keno.ioplugin      # Variable and output definitions
│   │   │   ├── Scale-tsunami.ioplugin
│   │   │   └── Scale-xsdrnpm.ioplugin
│   │   └── scripts/
│   │       ├── Scale-keno.sh            # Calculation scripts
│   │       ├── Scale-tsunami.sh
│   │       └── Scale-xsdrnpm.sh
│   └── test/
└── build.xml
```

### New Structure (fz-scale)
```
fz-scale/
├── .fz/
│   ├── models/
│   │   ├── Scale-keno.json              # Model definitions (JSON)
│   │   ├── Scale-tsunami.json
│   │   └── Scale-xsdrnpm.json
│   └── calculators/
│       ├── Scale-keno.sh                # Calculator scripts
│       ├── Scale-tsunami.sh
│       ├── Scale-xsdrnpm.sh
│       ├── Localhost_Scale-keno.json    # Calculator configs
│       ├── Localhost_Scale-tsunami.json
│       └── Localhost_Scale-xsdrnpm.json
├── examples/
│   ├── Scale-keno/
│   │   └── godiva.inp
│   └── example_usage.py
├── README.md
├── CONTRIBUTING.md
└── .gitignore
```

## Key Differences

### 1. Configuration Format

**Old (.ioplugin)**:
```properties
variableStartSymbol=&
variableLimit=(...)
formulaStartSymbol=@
formulaLimit={...}
commentLineChar='

output.mean_keff.get=grep("(.*).out","best estimate system k-eff") >> get(0) >> between("k-eff","+ or -") >> asNumeric()
```

**New (.json)**:
```json
{
    "varprefix": "&",
    "formulaprefix": "@",
    "delim": "()",
    "commentline": "'",
    "output": {
        "mean_keff": "grep 'best estimate system k-eff' *.out | head -1 | awk '{...}' || echo 1.0"
    }
}
```

### 2. Output Parsing

The old plugin used a custom DSL (Domain Specific Language) for output parsing:
```properties
output.mean_keff.get=grep("(.*).out","best estimate system k-eff") >> get(0) >> between("k-eff","+ or -") >> asNumeric()
```

The new plugin uses standard shell commands:
```json
"mean_keff": "grep 'best estimate system k-eff' *.out | head -1 | awk '{for(i=1;i<=NF;i++) if($i==\"k-eff\") print $(i+1)}' 2>/dev/null || echo 1.0"
```

Benefits:
- More flexible and powerful
- Easier to test and debug
- Standard Unix tools
- Default values with `|| echo`

### 3. Calculator Scripts

Calculator scripts are now more flexible:

**Improvements**:
- Accept both file and directory inputs
- Better error handling
- Environment variable support (`SCALE_HOME`)
- More descriptive error messages

### 4. Usage

**Old (Java-based Funz)**:
```java
// Complex Java API
RunDesign design = new RunDesign(inputFile, model, calculators);
design.setVariables(variables);
Results results = design.run();
```

**New (Python-based fz)**:
```python
import fz

results = fz.fzr(
    input_path="godiva.inp",
    input_variables={"r": [8.5, 8.6, 8.7]},
    model="Scale-keno",
    calculators="Localhost_Scale-keno",
    results_dir="results"
)
```

Benefits:
- Simpler API
- Python ecosystem integration
- Pandas DataFrames for results
- Better parallel execution
- Caching support

## Feature Comparison

| Feature | Old Plugin | New Plugin |
|---------|-----------|-----------|
| Language | Java | Python |
| Config Format | .ioplugin (properties) | .json |
| Output Parsing | Custom DSL | Shell commands |
| Variable Syntax | `&(...)` | `&(...)` ✓ Same |
| Formula Syntax | `@{...}` | `@{...}` ✓ Same |
| Comment Char | `'` | `'` ✓ Same |
| Models | 3 (keno, tsunami, xsdrnpm) | 3 ✓ Same |
| Parallel Execution | Yes | Yes ✓ Improved |
| Remote Execution | Yes | Yes ✓ SSH |
| Caching | Limited | Yes ✓ Enhanced |
| Results Format | Custom | Pandas DataFrame |

## Migration Steps

If you have existing workflows using the old plugin:

### 1. Install fz Framework
```bash
pip install git+https://github.com/Funz/fz.git
```

### 2. Update Your Scripts

**Old workflow**:
```bash
# Old Funz command line (example)
funz run -m Scale-keno -if godiva.inp -iv r=[8.5,8.6,8.7]
```

**New workflow**:
```python
import fz

results = fz.fzr(
    "godiva.inp",
    {"r": [8.5, 8.6, 8.7]},
    "Scale-keno",
    "Localhost_Scale-keno"
)
print(results)
```

### 3. Update Input Files

Good news: **No changes needed!** The variable syntax remains the same:
- `&(variable)` for variables
- `@{formula}` for formulas
- `'` for comments

### 4. Output Variables

All original output variables are preserved:

**Scale-keno**:
- `mean_keff`, `sigma_keff`
- `mean_E_lethargy`, `sigma_E_lethargy`
- `mean_nubar`, `sigma_nubar`
- `mean_free_path`, `sigma_free_path`

**Scale-tsunami**: Same as Scale-keno plus sensitivity coefficients

**Scale-xsdrnpm**:
- `lambda`

## Benefits of the New Plugin

1. **Modern Python Ecosystem**
   - Easy installation with pip
   - Integration with scientific Python (NumPy, Pandas, Matplotlib)
   - Better error messages and debugging

2. **Improved Flexibility**
   - Shell commands for output parsing (use any tool)
   - Easy to add new output variables
   - Custom calculators for different environments

3. **Better Performance**
   - Smarter caching based on file hashes
   - Improved parallel execution
   - Thread-safe calculator locking

4. **Enhanced Developer Experience**
   - JSON configuration (easy to edit and validate)
   - Clear documentation
   - Example scripts included
   - Contributing guide

5. **New Features**
   - Pandas DataFrame results
   - SSH remote execution
   - Interrupt handling (Ctrl+C)
   - Progress tracking
   - Flexible caching strategies

## Backward Compatibility

While the plugin structure has changed, we've maintained compatibility where it matters:

✅ **Same variable syntax**: `&(variable)`
✅ **Same formula syntax**: `@{formula}`  
✅ **Same comment character**: `'`
✅ **Same output variables**: All original outputs preserved
✅ **Same SCALE versions**: Compatible with SCALE 6.2+

❌ **Different API**: New Python API (simpler and more powerful)
❌ **Different config format**: JSON instead of .ioplugin

## Getting Help

- **Documentation**: See [README.md](README.md)
- **Examples**: Check [examples/](examples/)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Issues**: https://github.com/Funz/fz-scale/issues
- **FZ Framework**: https://github.com/Funz/fz

## Example Conversion

### Old Plugin Usage (Conceptual)

```java
// Old Java-based approach (conceptual)
String[] radii = {"8.5", "8.6", "8.7", "8.741"};
Map<String, String[]> variables = new HashMap<>();
variables.put("r", radii);

RunDesign design = new RunDesign("godiva.inp", "Scale-keno", "local");
design.setVariables(variables);
Results results = design.run();
```

### New Plugin Usage

```python
import fz

# New Python approach
results = fz.fzr(
    input_path="godiva.inp",
    input_variables={"r": [8.5, 8.6, 8.7, 8.741]},
    model="Scale-keno",
    calculators="Localhost_Scale-keno",
    results_dir="results"
)

# Results as Pandas DataFrame
print(results[['r', 'mean_keff', 'sigma_keff']])

# Easy plotting
import matplotlib.pyplot as plt
plt.plot(results['r'], results['mean_keff'], 'o-')
plt.xlabel('Radius (cm)')
plt.ylabel('k-eff')
plt.show()
```

## Conclusion

The new `fz-scale` plugin offers a modern, flexible, and powerful alternative to the old `plugin-scale`. While the API has changed, the migration is straightforward, and the benefits are significant.

For most users, the main change is switching from Java-based Funz to Python-based fz, which brings the plugin into the modern scientific Python ecosystem.
