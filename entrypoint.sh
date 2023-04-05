#!/bin/bash

version=$(typst --version)
echo "Using version $version"

echo "Building $1"
typst compile $1 main.pdf
