# Insecure Images: Following 5 images should be marked

FROM 666686886514.dkr.ecr.us-esast-1.amazon.com/cobis/cts-cis-serverless:cobis-cloud-cis-microservice-3
RUN apk add --no-cache python g++ make

FROM node
RUN apk add --no-cache python g++ make

FROM node AS node_image
RUN apk add --no-cache python g++ make

FROM node:12.2
RUN apk add --no-cache python g++ make

FROM node:12.2 AS node_image
RUN apk add --no-cache python g++ make

# Secure: Following 5 images should not be marked

FROM ubuntu@sha256:3235326357dfb65f1781dbc4df3b834546d8bf914e82cce58e6e6b676e23
RUN apt update

FROM ubuntu@sha256:3235326357dfb65f1781dbc4df3b834546d8bf914e82cce58e6e6b676e23 AS ubuntu
RUN apt update

FROM ubuntu:21.01-lts@sha256:3235326357dfb65f1781dbc4df3b834546d8bf914e82cce58e6e6b676e23 AS ubuntu
RUN apt update

FROM alpine:3.14@sha256:8d52b2c215a2a0a2c4132d8288e0e01a90fca5c5f5d364f5ed7b45b7ee1bdf67
RUN apt update

FROM --platform=$BUILDPLATFORM nginx@sha256:3fdd0a9532d0522bfa71b8aae903f7d15d39af0b0c74f84a2b13e107d0a45c4a
RUN apt update

FROM #{variable-image}#
RUN apt update

FROM ${variable-image}
RUN apt update

FROM $variable_image
RUN apt update