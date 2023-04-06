# Typst GitHub action

Build Typst documents using GitHub workflows.

## Example

Customize the following action to your own repo to compile `main.typ` to `main.pdf`, upload it as an action artifact, and create a timestamped release on push of a tagged commit.
Put it in `.github/workflow/build.yaml`.

```yaml
name: Build Typst document
on: [push, workflow_dispatch]

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Typst
        uses: lvignoli/typst-action@v0.1.0
        with:
          source_file: main.typ
      - name: Upload PDF file
        uses: actions/upload-artifact@v3
        with:
          name: PDF
          path: main.pdf
      - name: Get current date
        id: date
        run: echo "DATE=$(date +%Y-%m-%d-%H:%M)" >> $GITHUB_ENV
      - name: Release
        uses: softprops/action-gh-release@v1
        if: github.ref_type == 'tag'
        with:
          name: "${{ github.ref_name }} — ${{ env.DATE }}"
          files: main.pdf

```

It is also possible to build multiple files with a newline-separated list:

```yaml
      - name: Typst
        uses: lvignoli/typst-action@v0.1.0
        with:
          source_file: |
            foo.typ
            bar.typ
            baz.typ
```

Repository [lvignoli/typst-action-example](https://github.com/lvignoli/typst-action-example) provides an example setup.
