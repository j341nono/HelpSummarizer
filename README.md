# HelpSummarizer

**HelpSummarizer** is a command-line tool that uses AI to generate concise, readable summaries of shell command help output. Perfect for quickly understanding complex command usage without parsing lengthy documentation.

## Features

- **AI-powered summaries**: Leverages language models to create clear, concise explanations
- **Local and remote models**: Supports both local GGUF files and Hugging Face models
- **Customizable context**: Adjust token limits and input length for optimal performance
- **Simple interface**: One command to get help for any shell tool

## Quick Start

### Installation

```bash
curl -sSL https://raw.githubusercontent.com/j341nono/HelpSummarizer/main/install.sh | bash
```

### Basic Usage

- Summarize a command's help output
```bash
helpsummarizer --command cat
```

- Use a specific local model
```bash
helpsummarizer --command grep --model /path/to/model.gguf
```

- Use a Hugging Face model
```bash
helpsummarizer --command ls --model hugging-quants/Llama-3.2-3B-Instruct-Q4_K_M-GGUF --filename llama-3.2-3b-instruct-q4_k_m.gguf
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--command` | string | *required* | Shell command to summarize (e.g., `ls`, `cat`, `grep`) |
| `--model` | string | *optional* | Path to GGUF model file or Hugging Face repository name |
| `--filename` | string | *optional* | Specific model file/variant when using Hugging Face models |
| `--n_ctx` | integer | 512 | Maximum context tokens for the language model |
| `--help_command_length_limit` | integer | 400 | Maximum characters to extract from command help output |

## Examples

### Basic Command Summary
```bash
helpsummarizer --command find
```

### Advanced Configuration
```bash
helpsummarizer \
  --command grep \
  --model /models/gemma-2b.gguf \
  --n_ctx 256 \
  --help_command_length_limit 300
```

### Using Hugging Face Models
```bash
helpsummarizer \
  --command awk \
  --model huggingface/CodeBERTa-small-v1 \
  --filename model.bin
```

## How It Works

1. **Extract Help**: Runs `<command> --help` to get the raw help output
2. **Process**: Truncates output based on `--help_command_length_limit`
3. **Summarize**: Feeds the help text to the specified language model
4. **Output**: Returns a concise, human-readable summary

## Requirements

- Unix-like operating system (Linux, macOS)
- Python 3.7+ (for local models)
- Internet connection (for Hugging Face models)

## Troubleshooting

**Model not found**: Ensure the model path is correct and the file exists
**Context too small**: Increase `--n_ctx` if summaries are cut off
**Help output too long**: Reduce `--help_command_length_limit` for very verbose commands

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests on the [GitHub repository](https://github.com/j341nono/HelpSummarizer).
