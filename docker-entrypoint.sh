#!/bin/bash
echo "Waiting for Database..." && sleep 20
set -e
task migrate
uvicorn 'pokeapi.main:app' --host=0.0.0.0 --port=8000 --reload
