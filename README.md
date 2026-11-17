# Verify an agent handoff

Two scripted worker reports both say they are done. One gives 240 active records. The other gives 300 by mixing in 60 historical records. The inputs are synthetic. No model, API, or paid service is required.

Run with Python 3 from this folder:

```sh
python3 verify.py reports/wrong.json --format-only
python3 verify.py reports/wrong.json
python3 verify.py reports/correct.json
```

Expected exit codes are 0, 1, and 0. The format-only mode accepts a well-shaped handoff. The default mode independently counts active rows in the source inventory before accepting the report. The experiment demonstrates one failure pattern and one check for it. It does not measure how often agents make this error.
