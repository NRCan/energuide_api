#!/bin/bash

if test ! $(which brew); then
    echo "ERROR: It looks like you need to install Homebrew first."
    exit 1 # terminate with error
fi

# Update homebrew recipes
echo "----> Updating Homebrew"
brew update

# Pyenv
if [[ ! $(brew ls pyenv --versions) ]]; then
    echo "----> Installing pyenv with Homebrew"
    brew install pyenv

    echo ''
    echo ''
    echo '**IMPORTANT**'
    echo 'Please make sure to put '"'"'eval "$(pyenv init -)"'"'"' near the bottom of your shell configuration file (eg, ~/.bash_profile or ~/.zshrc).'
    echo 'For more information, refer to pyenv installation instructions.'
    echo ''
    echo ''
    eval "$(pyenv init -)"

    PYTHON_VERSION=3.6.4

    if [[ ! $(python --version) = "Python ${PYTHON_VERSION}" ]]; then
      echo "----> Installing Python ${PYTHON_VERSION}"
      exit 0
      pyenv install $PYTHON_VERSION
      pyenv local $PYTHON_VERSION
    fi
fi

# MongoDB
if [[ ! $(brew ls mongodb --versions) ]]; then
  echo "----> Installing mongodb with Homebrew"
  brew install mongodb
fi

# Install homebrew services (does nothing if already installed)
brew tap homebrew/services

echo "----> Run 'make setup' to import the test data"
echo "----> export NRCAN_ENGINE_API_KEY='your_api_key'"
echo "----> Run 'make run' to boot up the API"
exit 0
