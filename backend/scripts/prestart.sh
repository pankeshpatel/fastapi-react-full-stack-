#! /usr/bin/env bash

set -e
set -x

# Let the DB start
poetry run python backend/config/backend_pre_start.py


# Create initial data in DB
poetry run python backend/config/initial_data.py
