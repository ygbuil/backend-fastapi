#!/bin/bash
uv sync
uv run pre-commit install --hook-type pre-commit --hook-type pre-push

uv run python db_init.py