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
    out_dir = str(root / "docs" / version)
    template_dir = str(root / "doc_template")

    if version != "./" and version != VERSION:
        # Use an isolated environment per old version so their (older)
        # dependencies don't clobber the current venv.
        tarball = str(root / "dist" / f"pamda-{version}.tar.gz")
        subprocess.run(
            [
                "uv", "run", "--isolated",
                "--with", tarball,
                "--with", "pdoc",
                "pdoc", "-o", out_dir, "-t", template_dir, "pamda",
            ],
            check=True,
            env=env,
            cwd=str(root),
        )
    else:
        subprocess.run(
            [sys.executable, "-m", "pdoc", "-o", out_dir, "-t", template_dir, "pamda"],
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
