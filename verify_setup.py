#!/usr/bin/env python3
"""Week 11 environment check. Run: python verify_setup.py"""
import shutil
import subprocess
import sys
from pathlib import Path

assert sys.version_info >= (3, 10), f"Need Python 3.10+, got {sys.version}"
root = Path(".").resolve()
for d in ["services", "agents", "deploy", "docs", "tests", "fixtures"]:
    (root / d).mkdir(parents=True, exist_ok=True)
print("OK module4-capstone folders ready")

if shutil.which("docker"):
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        print("OK docker available (optional this week)")
    except Exception as e:
        print("WARN docker present but failed:", e)
else:
    print("WARN docker not on PATH (optional for Tuesday testing focus)")

r = subprocess.run([sys.executable, "-m", "pytest", "-q"], capture_output=True, text=True)
print("pytest exit", r.returncode, "(empty suite exit 5 is OK until Tuesday Lab 1)")
print("Week 11 base OK; Python", sys.version.split()[0])