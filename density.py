#!/usr/bin/env python3
# density.py
# Usage examples:
#   python density.py 288.15
#   python density.py 15 --unit C           # 15 °C
#   python density.py 300 --pressure 120000 # different pressure
#   python density.py 288.15 --fluid Air --out outputs.json

import argparse, json, sys
from CoolProp.CoolProp import PropsSI

def parse_args():
    p = argparse.ArgumentParser(
        description="Compute density from temperature using CoolProp (default fluid=Oxygen, P=101325 Pa)."
    )
    p.add_argument("temperature", type=float, help="Temperature value (Kelvin by default, see --unit).")
    p.add_argument("--unit", choices=["K", "C"], default="K", help="Temperature unit (K or C). Default: K.")
    p.add_argument("--pressure", type=float, default=101325.0, help="Pressure in Pa. Default: 101325.")
    p.add_argument("--fluid", default="Oxygen", help='Fluid name (CoolProp). Default: "Oxygen".')
    p.add_argument("--out", help="Optional path to write JSON output.")
    return p.parse_args()

def main():
    args = parse_args()

    # Convert temperature to Kelvin if needed
    T_K = args.temperature if args.unit == "K" else (args.temperature)
    P_Pa = float(args.pressure)
    fluid = args.fluid

    # Compute density ρ using CoolProp: PropsSI("D", "T", T, "P", P, fluid)
    rho = float(PropsSI("D", "T", T_K, "P", P_Pa, fluid))  # kg/m^3

    result = {
        "fluid": fluid,
        "inputs": {"temperature": args.temperature, "unit": args.unit, "pressure_Pa": P_Pa},
        "outputs": {"density_kg_per_m3": rho}
    }

    # Print to stdout
    print(json.dumps(result, indent=2))

    # Optionally write to file
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"✅ Wrote results to {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()
