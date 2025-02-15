ARG VERSION=latest
FROM ghcr.io/typst/typst:${VERSION}

LABEL \
	org.opencontainers.image.title="Typst GitHub action based on ghcr.io/typst/typst image" \
	org.opencontainers.image.authors="Louis Vignoli <louis.vignoli@gmail.com>" \
	org.opencontainers.image.source="https://github.com/lvignoli/typst-action"

RUN apk add python3

COPY \
	LICENSE \
	README.md \
	entrypoint.py \
	/root/

ENTRYPOINT ["python3", "/root/entrypoint.py"]
