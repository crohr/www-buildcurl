#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
test_root="$(mktemp -d)"
cache_bump="build-success-test-$$"
fingerprint="$(printf '%s' "$cache_bump|pkgr|sles:16|/usr/local|deadbeef" | sha1sum | cut -d ' ' -f 1)"
cache_file="/tmp/$fingerprint.tgz"
trap 'rm -rf "$test_root"; rm -f "$cache_file"' EXIT

mkdir -p "$test_root/bin" "$test_root/ruby" "$test_root/payload"
printf 'ok\n' > "$test_root/payload/result"

cat > "$test_root/bin/ssh" <<'EOF'
#!/usr/bin/env bash
echo "compile succeeded" >&2
tar -czf - -C "$FAKE_SSH_PAYLOAD" .
EOF
chmod +x "$test_root/bin/ssh"

cat > "$test_root/ruby/dotenv.rb" <<'EOF'
module Dotenv
  def self.load(*)
  end
end
EOF

response="$test_root/response"
PATH="$test_root/bin:$PATH" \
  RUBYLIB="$test_root/ruby" \
  FAKE_SSH_PAYLOAD="$test_root/payload" \
  SOURCE="$repo_root/app" \
  CACHE_BUMP="$cache_bump" \
  REQUEST_METHOD=GET \
  QUERY_STRING='recipe=pkgr&version=deadbeef&target=sles%3A16' \
  HTTP_ACCEPT='text/plain' \
  ruby "$repo_root/app/cgi-bin/build.cgi" > "$response"

grep -q '^Status: 302' "$response"
grep -q "^Location: /cache/$fingerprint.tgz" "$response"
grep -q 'compile succeeded' "$response"
tar -tzf "$cache_file" >/dev/null

echo "build success test passed"
