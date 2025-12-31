from pathlib import Path
import subprocess

from termcolor import cprint

# git config --global core.autocrlf false
# cprint("##### convert dos linefeeds (crlf) to unix (lf) #####", color="cyan")
# for f in [p for p in Path("src").rglob("*.py") if p.is_file()]:
#     subprocess.run(f"python -m dos2unix {f} {f}", check=True)

cprint("##### remove-all-unused-imports #####", color="cyan")
for f in [p for p in Path("src").rglob("*.py") if p.is_file()]:
    subprocess.run(f"autoflake --remove-all-unused-imports -i {f}", check=True)

cprint("##### isort #####", color="cyan")
subprocess.run("isort src", check=True)

cprint("##### black #####", color="cyan")
subprocess.run("black src", check=True)
