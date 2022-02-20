import subprocess
from typing import Optional, List


def run(command: List[str], cwd: str = None) -> Optional[str]:
    """Run command and return output"""
    get_output = subprocess.check_output(command, cwd=cwd)

    if get_output:
        return get_output.decode()


