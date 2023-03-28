FROM ubuntu:latest

LABEL \
	org.opencontainers.image.title="Docker Image of typst" \
	org.opencontainers.image.authors="Louis Vignoli <louis.vignoli@gmail.com>" \
	org.opencontainers.image.source="https://github.com/lvignoli/typst-action"

ENV PATH="/opt/typst/bin/:${PATH}"

COPY setup.sh .
COPY entrypoint.sh .

RUN /setup.sh
RUN rm setup.sh

ENTRYPOINT ["/entrypoint.sh"]
