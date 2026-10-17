# Bounded CLI process handling

Run from the repository under review. Put temporary briefs, final messages and event captures outside it. Build argv as a list of arguments, not a shell string; do not interpolate the brief into a shell command.

Use a process group with a maximum of 1800 seconds for each invocation and its children. A tool yield returning a live session is only a yield, not a reason to kill the review. Python's timeout works on macOS without GNU `timeout`:

```python
import os
from pathlib import Path
import signal
import subprocess

# Supply argv, review_repo, review_capture, and brief_text from the chosen route.
# brief_text is None for Muse, which reads its temporary prompt file.
process = subprocess.Popen(
    argv,
    cwd=review_repo,
    stdin=subprocess.PIPE if brief_text is not None else subprocess.DEVNULL,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    start_new_session=True,
)
timed_out = False
try:
    stdout, stderr = process.communicate(input=brief_text, timeout=1800)
except subprocess.TimeoutExpired:
    timed_out = True
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass  # The process group exited between the timeout and the signal.
    stdout, stderr = process.communicate()
Path(review_capture).write_text(stdout, encoding="utf-8")
Path(str(review_capture) + ".stderr").write_text(stderr, encoding="utf-8")
```

`communicate` closes stdin once the brief is written; Muse receives `DEVNULL` because its prompt is a file. Check `timed_out`, the exit status, the provider-specific completion metadata and the final answer before reporting success. A timed-out invocation is failed even if it captured plausible text. Keep the partial capture only for diagnosis, and report the failure.

Retry once for a transport or internal-server failure. Do not retry authentication, quota, billing, rate-limit, unavailable-model or permission rejection. Confirm that the previous process and its children have stopped before retrying; do not leave duplicate reviews running.
