#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    # Setup Python
    python -m virtualenv .env --prompt "[brainstorm] "
    find .env -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .env/bin/pip install -U pip
    .env/bin/pip install -r requirements.txt

    # Setup NodeJs
    sudo apt install -y nodejs
    sudo apt install -y npm
    npm update
    (cd brainstorm/gui/app/ && npm install)

    # Setup GUI server files
    (cd brainstorm/gui/app/ && npm run build)
}


main "$@"
