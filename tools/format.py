import argparse
from concurrent import futures
from pathlib import Path
import subprocess

from termcolor import cprint


def _autoflake(f: Path):
    try:
        subprocess.run(
            f"autoflake --remove-all-unused-imports -i {f}",
            check=True,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        cprint(f"run autoflake failed: {e}", color="red")



def _dos2unix(f: Path):
    try:
        subprocess.run(f"python -m dos2unix {f} {f}", check=True,stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        cprint(f"run autoflake failed: {e}", color="red")


def main():
    parser = argparse.ArgumentParser(description='格式化')
    parser.add_argument(
        "--dos2unix", action="store_true", help="将DOS换行符转换为Unix换行符"
    )
    args = parser.parse_args()

    # git config --global core.autocrlf false
    py_files = [p for p in Path("src").rglob("*.py") if p.is_file()]
    if args.dos2unix:
        cprint("##### convert dos linefeeds (crlf) to unix (lf) #####", color="cyan")
        with futures.ProcessPoolExecutor() as executor:
            for _ in executor.map(_dos2unix, py_files):
                pass

    cprint("##### remove-all-unused-imports #####", color="cyan")
    with futures.ProcessPoolExecutor() as executor:
        for _ in executor.map(_autoflake, py_files):
            pass

    cprint("##### isort #####", color="cyan")
    subprocess.run("isort src", check=True)

    cprint("##### black #####", color="cyan")
    subprocess.run("black src", check=True)


if __name__ == "__main__":
    main()
