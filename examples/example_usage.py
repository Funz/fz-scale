#!/usr/bin/env python3
"""
Example usage of the fz-scale plugin for SCALE calculations.

This example demonstrates how to run a parametric study on the
Godiva critical sphere benchmark with varying radii.

Note: This requires SCALE to be installed. If SCALE is not available,
this script will fail during execution but demonstrates the plugin structure.
"""

import fz

# Example 1: Scale-keno (KENO criticality calculation)
def example_keno():
    """Run a KENO parametric study with varying sphere radius."""
    
    print("=" * 70)
    print("Example 1: SCALE KENO - Godiva Critical Sphere")
    print("=" * 70)
    
    # Define parameter values
    # Testing radii around the critical radius of 8.741 cm
    input_variables = {
        "r": [8.5, 8.6, 8.7, 8.741, 8.8, 8.9, 9.0]
    }
    
    try:
        # Run parametric calculation
        results = fz.fzr(
            input_path="examples/Scale-keno/godiva.inp",
            input_variables=input_variables,
            model="Scale-keno",
            calculators="Localhost_Scale-keno",
            results_dir="results/godiva_study"
        )
        
        # Display results
        print("\nResults:")
        print(results[['r', 'mean_keff', 'sigma_keff', 'status']])
        
        # Find critical radius (k-eff closest to 1.0)
        results['delta_k'] = abs(results['mean_keff'] - 1.0)
        critical = results.loc[results['delta_k'].idxmin()]
        print(f"\nClosest to critical: r={critical['r']} cm, k-eff={critical['mean_keff']}")
        
    except Exception as e:
        print(f"\nError running calculation: {e}")
        print("Note: This requires SCALE to be installed.")


# Example 2: Using fzi to identify variables
def example_fzi():
    """Parse input file to identify variables."""
    
    print("\n" + "=" * 70)
    print("Example 2: Parse Input File for Variables")
    print("=" * 70)
    
    # Parse the input file to find variables
    variables = fz.fzi(
        "examples/Scale-keno/godiva.inp",
        "Scale-keno"
    )
    
    print(f"\nVariables found in godiva.inp: {list(variables.keys())}")


# Example 3: Using fzc to compile input files
def example_fzc():
    """Compile input files with specific parameter values."""
    
    print("\n" + "=" * 70)
    print("Example 3: Compile Input Files")
    print("=" * 70)
    
    import tempfile
    import os
    
    # Create temporary directory for compiled files
    with tempfile.TemporaryDirectory() as tmpdir:
        # Compile input with specific radius
        fz.fzc(
            "examples/Scale-keno/godiva.inp",
            {"r": 8.741},
            "Scale-keno",
            output_dir=tmpdir
        )
        
        # Show compiled file
        compiled_file = os.path.join(tmpdir, "godiva.inp")
        if os.path.exists(compiled_file):
            print(f"\nCompiled file content (r=8.741):")
            with open(compiled_file, 'r') as f:
                for i, line in enumerate(f, 1):
                    if i <= 15:  # Show first 15 lines
                        print(f"  {line.rstrip()}")


def main():
    """Run all examples."""
    
    # Check if examples directory exists
    import os
    if not os.path.exists("examples/Scale-keno/godiva.inp"):
        print("Error: Example files not found.")
        print("Please run this script from the fz-scale repository root.")
        return 1
    
    # Run examples
    example_fzi()
    example_fzc()
    example_keno()
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
