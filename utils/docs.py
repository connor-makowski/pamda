import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).parent.parent
pamda_init = root / "pamda" / "__init__.py"

VERSION = "2.10.0"
OLD_DOC_VERSIONS = ["1.0.0", "0.0.14"]

env = {
    **os.environ,
    "version_options": " ".join([VERSION] + OLD_DOC_VERSIONS),
}


def generate_docs(version):
    if version != "./" and version != VERSION:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", str(root / "dist" / f"pamda-{version}.tar.gz")],
            check=True,
        )
    subprocess.run(
        [sys.executable, "-m", "pdoc", "-o", str(root / "docs" / version), "-t", str(root / "doc_template"), "pamda"],
        check=True,
        env=env,
    )


# Build __init__.py from README
readme = (root / "README.md").read_text()
pamda_init.write_text(f'"""\n{readme}\n"""\nfrom .pamda import pamda\n')

generate_docs("./")
generate_docs(VERSION)
for version in OLD_DOC_VERSIONS:
    generate_docs(version)

# Reinstall current package as editable
subprocess.run([sys.executable, "-m", "pip", "install", "-e", str(root)], check=True)
