#!/bin/bash
set -e

echo "Creating keys..."
mkdir -p /keys
openssl genpkey -algorithm RSA -out /keys/private_key.pem
openssl rsa -pubout -in /keys/private_key.pem -out /keys/public_key.pem

echo "Waiting for Database..." && sleep 20
task migrate
uvicorn 'pokeapi.main:app' --host=0.0.0.0 --port=8000 --reload
