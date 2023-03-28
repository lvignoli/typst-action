#!/bin/bash

version=$(typst --version)
echo "Using version $version"

echo "Building $1"
typst $1 main.pdf
