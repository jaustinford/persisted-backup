# syntax=docker/dockerfile:1

FROM python:3.9.19-bookworm

RUN \
    apt update -y && \
    apt install -y \
        cifs-utils

RUN \
    pip3 install \
        pyyaml \
        hvac

WORKDIR /persisted-backup

COPY src/ ./src/
COPY conf/ ./conf/
