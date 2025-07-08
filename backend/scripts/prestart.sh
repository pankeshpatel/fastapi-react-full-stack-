#! /usr/bin/env bash

set -e
set -x

# Let the DB start
poetry run python backend/utils/backend_pre_start.py


# Create initial data in DB
poetry run python backend/utils/initial_data.py
