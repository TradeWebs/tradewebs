#!/bin/bash
# Pulls the DNS-scoped Cloudflare API token from macOS Keychain into the
# environment for this shell session. Source it, don't execute it:
#   source cloudflare-env.sh
# Token itself is never written to disk - only Keychain holds it.
export CLOUDFLARE_DNS_TOKEN
CLOUDFLARE_DNS_TOKEN=$(security find-generic-password -a "$USER" -s "cloudflare-dns-token" -w)
