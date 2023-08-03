#!/bin/bash
set -euo pipefail

if [ -v MIGRATE ]; then
    alembic upgrade head
fi

exec waitress-serve gpyt_eventbus.injection.injector:app
