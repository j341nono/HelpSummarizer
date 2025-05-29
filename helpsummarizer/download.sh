#!/bin/bash
MODEL_NAME=$1
FILENAME=$2

LOCAL_DIR=${HOME}/.helpsummarizer/models/

echo "Downloading model: $LOCAL_DIR/$FILENAME"

huggingface-cli download ${MODEL_NAME} ${FILENAME} --local-dir ${LOCAL_DIR}
