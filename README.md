# Typst GitHub action

Build Typst documents using GitHub workflows.

## Minimal example

The following `.github/workflows/build.yaml` action compiles `main.typ` to `main.pdf` on every push.

```yaml
name: Build Typst document
on: push

jobs:
  build_typst_documents:
    runs-on: ubuntu-latest:
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Typst
        uses: lvignoli/typst-action@v0
        with:
          source_file: main.typ
```

## Longer example

Here we compile multiple files on each push, and all the PDF them in a tagged and timestamped release when the commit is tagged.

<!-- Customize the following action to your own repo to compile `main.typ` to `main.pdf`, upload it as an action artifact, and create a timestamped release on push of a tagged commit.
Put it in `.github/workflow/build.yaml`. -->

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
        uses: lvignoli/typst-action@v0
        with:
          source_file: |
            first_file.typ
            second_file.typ
            third_and_final_file.typ

      - name: Upload PDF file
        uses: actions/upload-artifact@v3
        with:
          name: PDF
          path: *.pdf

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

Repository [lvignoli/typst-action-example](https://github.com/lvignoli/typst-action-example) provides an example setup.
