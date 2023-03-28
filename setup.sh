#!/bin/sh

set -e

echo "==> Install necessary utilities"

apt-get update
apt-get install -y \
	bash \
	curl \
	ripgrep \
	wget 

TARBALL_URL="https://api.github.com/repos/typst/typst/releases"

echo "==> Downloading Typst..."

curl -s $TARBALL_URL \
	| rg "browser_download_url.*typst-x86_64-unknown-linux-gnu.tar.gz" \
	| head -1 \
	| cut -d : -f 2,3 \
	| tr -d \" \
	| wget -qi - 

echo "==> Extracting Typst binary..."

tar xf typst-x86_64-unknown-linux-gnu.tar.gz

echo "==> Moving binary..."

mkdir -p /opt/typst/bin
cp typst-x86_64-unknown-linux-gnu/typst /opt/typst/bin

echo "==> Cleaning up"

rm -r typst-x86_64-unknown-linux-gnu
rm typst-x86_64-unknown-linux-gnu.tar.gz 
