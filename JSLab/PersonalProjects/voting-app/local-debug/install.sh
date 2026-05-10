#!/usr/bin/env bash
set -euo pipefail

HOSTS_FILE="/etc/hosts"
ENTRIES=(
    "vote.test"
    "result.test"
)

echo "Configuring /etc/hosts for voting-app portless domains..."
echo

to_add=()

for host in "${ENTRIES[@]}"; do
    # Match: optional leading whitespace, an IP/hostname (non-comment),
    # whitespace, then our hostname as a whole word.
    if grep -qE "^[[:space:]]*[^#[:space:]]+[[:space:]]+${host}([[:space:]]|$)" "$HOSTS_FILE"; then
        echo "  ✓ ${host} already configured"
    else
        echo "  + ${host} will be added"
        to_add+=("$host")
    fi
done

if [ ${#to_add[@]} -eq 0 ]; then
    echo
    echo "All entries already present. Nothing to do."
    exit 0
fi

echo
echo "Updating ${HOSTS_FILE} (requires sudo)..."

{
    echo ""
    echo "# voting-app portless domains"
    for host in "${to_add[@]}"; do
        echo "127.0.0.1 ${host}"
    done
} | sudo tee -a "$HOSTS_FILE" > /dev/null

echo
if [ ${#to_add[@]} -eq 1 ]; then
    echo "✓ Added 1 entry to ${HOSTS_FILE}"
else
    echo "✓ Added ${#to_add[@]} entries to ${HOSTS_FILE}"
fi
echo
echo "Next:  docker-compose up -d"
