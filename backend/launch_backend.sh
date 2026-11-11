
#!/bin/bash

chmod +x ./launch_backend.sh
uv sync
uv run uvicorn app.main:app --reload