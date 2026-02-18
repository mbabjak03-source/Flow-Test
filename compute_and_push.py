# compute_and_push.py
# pip install -r requirements.txt

import os
import time
import json
import requests
from CoolProp.CoolProp import PropsSI

BASE_URL  = "https://api.flowengineering.com/rest/v1"  # from docs
ORG       = os.getenv("FLOW_ORG_ALIAS", "<your_orgAlias>")
PROJECT   = os.getenv("FLOW_PROJECT_ALIAS", "<your_projectAlias>")
REFRESH   = os.getenv("FLOW_REFRESH_TOKEN")            # set in GitHub Secrets

def get_access_token(refresh_token: str) -> str:
    """Exchange refresh token for access token (per Flow docs)."""
    # POST /auth/exchange returns { "accessToken": "...", "expiresIn": "..." }
    # https://api.flowengineering.com/rest/v1/docs
    url = f"{BASE_URL}/auth/exchange"
    res = requests.post(url, json={"refreshToken": refresh_token})
    res.raise_for_status()
    return res.json()["accessToken"]  # per docs shape

def auth_hdr(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def load_design_inputs(token: str) -> tuple[float, float]:
    """
    Read design values for inlet P/T.
    Strategy: list & filter client-side (docs note pagination generally not enabled).
    """
    # Open "Values" in the docs to copy the exact GET endpoint for design values.
    # Examples vary by tenant; paste yours:
    design_get = f"{BASE_URL}/org/{ORG}/project/{PROJECT}/YOUR_VALUES_DESIGN_GET_ENDPOINT"
    r = requests.get(design_get, headers=auth_hdr(token))
    r.raise_for_status()
    values = r.json()

    # Adjust keys/fields to your schema; below assumes { key, value } pairs.
    P_key = "compressor.inlet_pressure"
    T_key = "compressor.inlet_temperature"

    def pick(key):
        return next(v for v in values if v.get("key") == key)

    P_inlet = pick(P_key)["value"]  # adapt if value is nested (e.g., ["value"]["number"])
    T_inlet = pick(T_key)["value"]
    return float(P_inlet), float(T_inlet)

def push_model_value(token: str, key: str, value: float, unit: str = "kg/m^3") -> dict:
    # Paste the exact PUT endpoint for MODEL values from "Values" in your docs.
    model_put = f"{BASE_URL}/org/{ORG}/project/{PROJECT}/YOUR_VALUES_MODEL_PUT_ENDPOINT"

    # Adjust JSON shape to what your docs show for model values.
    payload = {
        "key": key,
        "value": value,
        "unit": unit,
        "metadata": {
            "source": "GitHub Actions + CoolProp",
            "note":   "Computed from design P/T via PropsSI",
            "run_at": int(time.time())
        }
    }
    r = requests.put(model_put, headers=auth_hdr(token), json=payload)
    try:
        r.raise_for_status()
    except requests.HTTPError:
        print("Server response:", r.text)
        raise
    return r.json()

def main():
    assert REFRESH, "Set FLOW_REFRESH_TOKEN as an environment variable/secret."
    token = get_access_token(REFRESH)

    # 1) Read design inputs from Flow (Design Values)
    P_inlet, T_inlet = load_design_inputs(token)

    # 2) Your calc (the snippet you posted)
    rho_air = PropsSI("D", "T", T_inlet, "P", P_inlet, "Air")

    # 3) Write back as a MODEL value (NOT a Design value)
    result = push_model_value(token,
                              key="analysis.air_density_at_inlet",
                              value=rho_air,
                              unit="kg/m^3")
    print("Updated model value:", json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
