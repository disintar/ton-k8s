import subprocess
from typing import Optional, List

from hllib.log import logger


def run(command: List[str], cwd: str = None) -> Optional[str]:
    """Run command and return output"""

    try:
        output_good = False

        while not output_good:
            command = list(map(str, command))
            logger.debug(f"🐼 Run: {' '.join(command)}")
            get_output = subprocess.check_output(command, cwd=cwd)
            answer = get_output.decode()

            if 'PosixError' in answer:
                logger.error(f"🐗 Answer is not good: {answer}")
                continue
            else:
                get_output = True

            if get_output:
                logger.debug(f"🐼 Answer: {answer}")
                return answer
    except subprocess.CalledProcessError as exc:
        logger.error(f"Status : FAIL {exc.returncode} {exc.output}")
        raise exc
