# Typst GitHub action

Build Typst documents using GitHub workflows.

## Minimal example

The following `.github/workflows/build.yaml` action compiles `main.typ` to `main.pdf` on every push.

```yaml
name: Build Typst document
on: push

jobs:
  build_typst_documents:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Typst
        uses: lvignoli/typst-action@main
        with:
          source_file: main.typ
```

## Longer example

Here we compile multiple files on each push, and publish all the PDFs in a tagged and timestamped release when the commit is tagged.

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
        uses: lvignoli/typst-action@main
        with:
          options: |
            --font-path
            fonts
          source_file: |
            first_file.typ
            second_file.typ
            third_and_final_file.typ

      - name: Upload PDF file
        uses: actions/upload-artifact@v4
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

Repository [lvignoli/typst-action-example](https://github.com/lvignoli/typst-action-example) provides an example setup on a whole repo.

## Notes

- This action runs on the docker image shipped with the latest Typst.
  As long as Typst is in v0, changes of the CLI API are to be expected, breaking the workflow.
  I'll update regularly.

- I was hasty to tag for a v1. I have now deleted it.
  As long as Typst is not in a stable state, the action will stay in v0.
  You should use `lvignoli/typst-action@main` in the meantime.
