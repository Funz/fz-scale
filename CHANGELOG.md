# Changelog

All notable changes to the fz-scale plugin will be documented in this file.

## [Unreleased]

### Added
- Support for CSAS-Shift sequence (csas5-shift, csas6-shift)
  - Scale-shift.json model definition for Shift Monte Carlo solver
  - Scale-shift.sh calculator script for executing CSAS-Shift calculations
  - Localhost_Scale-shift.json calculator configuration
  - Godiva example input file using csas6-shift
  - Documentation and usage examples for CSAS-Shift in README.md
- Enhanced test suite to validate Scale-shift model and calculator

## [1.0.0] - 2025-01-13

### Added
- Initial port from old plugin-scale (Java-based) to new fz framework (Python-based)
- Three model definitions in JSON format:
  - Scale-keno.json for KENO criticality calculations (csas5, csas6)
  - Scale-tsunami.json for TSUNAMI sensitivity analysis (tsunami-3d)
  - Scale-xsdrnpm.json for XSDRNPM transport calculations (xsdrnpm, csas1x)
- Three calculator shell scripts:
  - Scale-keno.sh for executing KENO calculations
  - Scale-tsunami.sh for executing TSUNAMI calculations
  - Scale-xsdrnpm.sh for executing XSDRNPM calculations
- Three calculator configuration files for localhost execution
- Godiva critical sphere example with parametric input file
- Python usage example script demonstrating fz.fzi(), fz.fzc(), and fz.fzr()
- Comprehensive test suite (test_plugin.py)
- GitHub Actions CI workflow for automated testing
- Complete documentation:
  - README.md with usage examples and configuration details
  - CONTRIBUTING.md for developers
  - MIGRATION.md guide for users of the old plugin
  - LICENSE (BSD 3-Clause)
  - .gitignore for repository cleanliness

### Changed
- Configuration format: .ioplugin (properties) → .json
- Output parsing: Custom DSL → Shell commands (grep, awk, etc.)
- API: Java-based Funz → Python-based fz framework

### Maintained
- Variable syntax: &(variable) remains unchanged
- Formula syntax: @{formula} remains unchanged
- Comment character: ' (single quote) remains unchanged
- All output variables from original plugin preserved
- SCALE version compatibility (6.2+)

### Technical Details
- 18 files created across 9 directories
- All JSON files validated
- All shell scripts syntax-checked and made executable
- All tests passing
- Compatible with Python 3.6+
- Integrates with fz framework for modern Python scientific computing

## Notes

This version represents a complete modernization of the SCALE plugin while
maintaining backward compatibility in terms of input file syntax and output
variables. The new structure leverages the fz framework's capabilities for
parallel execution, caching, and result management.

For users migrating from the old plugin-scale, please refer to MIGRATION.md
for detailed guidance on updating your workflows.
