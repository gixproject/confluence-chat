#!/bin/bash

set -ef -o pipefail

setup() {
  echo "[ Setup ] Creating a temporary python virtual environment and installing packages."
  poetry env use python3.12
  poetry install
}

setup_env() {
  echo "[ Setup ] Setting environments variables."
  if [ ! -f ".env.example" ] && [ ! -f ".env" ]; then
    cp .env.example .env
  elif [ ! -f ".env.example" ]; then
    echo "[ Setup ] Error, file '.env.example' does not exist."
    exit
  fi

  echo "[ Setup ] Environment variables are set."
}

setup_hook() {
  poetry run pre-commit install
  poetry run pre-commit run
}

setup_env
setup
setup_hook

printf "\033[92m[ Setup ] Setup is finished. You don't need to run this script anymore.\n"
