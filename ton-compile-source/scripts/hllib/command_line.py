import subprocess
from typing import Optional, List

from hllib.log import logger


def run(command: List[str], cwd: str = None) -> Optional[str]:
    """Run command and return output"""

    try:
        command = list(map(str, command))
        logger.debug(f"🐼 Run: {' '.join(command)}")
        get_output = subprocess.check_output(command, cwd=cwd)

        if get_output:
            answer = get_output.decode()
            logger.debug(f"🐼 Answer: {answer}")
            return answer
    except subprocess.CalledProcessError as exc:
        logger.error(f"Status : FAIL {exc.returncode} {exc.output}")
        raise exc
