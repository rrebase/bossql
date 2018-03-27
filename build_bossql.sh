#!/bin/bash
set -eo pipefail
IFS=$'\n\t'

REPO_URL="https://github.com/rrebase/bossql.git"
TARGET=bossql

if [ -n "$1" ]; then
    TARGET="$1"
fi

git clone "$REPO_URL" "$TARGET"
cd "$TARGET"
git checkout develop
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
./manage.py migrate
echo "from accounts.models import CustomUser; CustomUser.objects.create_superuser('admin', 'admin@bossql.com', 'kalamees')" | ./manage.py shell
