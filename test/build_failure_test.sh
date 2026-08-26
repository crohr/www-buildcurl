#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
test_root="$(mktemp -d)"
cache_bump="build-failure-test-$$"
fingerprint="$(printf '%s' "$cache_bump|pkgr|sles:16|/usr/local|deadbeef" | sha1sum | cut -d ' ' -f 1)"
cache_file="/tmp/$fingerprint.tgz"
trap 'rm -rf "$test_root"; rm -f "$cache_file"' EXIT

mkdir -p "$test_root/bin" "$test_root/ruby"
cat > "$test_root/bin/ssh" <<'EOF'
#!/usr/bin/env bash
echo "compile failed" >&2
exit 23
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
  RUBYOPT=-rdigest/sha1 \
  SOURCE="$repo_root/app" \
  CACHE_BUMP="$cache_bump" \
  REQUEST_METHOD=GET \
  QUERY_STRING='recipe=pkgr&version=deadbeef&target=sles%3A16' \
  HTTP_ACCEPT='text/plain' \
  ruby "$repo_root/app/cgi-bin/build.cgi" > "$response"

grep -q '^Status: 502' "$response"
grep -q 'compile failed' "$response"

if grep -qi '^Location:' "$response"; then
  echo "failed build returned a cache redirect" >&2
  exit 1
fi

if [[ -e "$cache_file" ]]; then
  echo "failed build published a cache artifact" >&2
  exit 1
fi

echo "build failure test passed"
