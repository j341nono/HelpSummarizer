#!/bin/bash

LOCAL_DIR=${HOME}/.helpsummarizer/models/

mkdir -p ${LOCAL_DIR}

echo "$LOCAL_DIR を作成しました．"

huggingface-cli download hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF llama-3.2-3b-instruct-q4_k_m.gguf --local-dir ${LOCAL_DIR}

uv tool install git+https://github.com/j341nono/HelpSummarizer.git

echo "完了しました．"