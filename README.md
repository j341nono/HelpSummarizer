# HelpSummarizer

**HelpSummarizer** is a command-line tool that summarizes the --help output of shell commands using a language model. 

It is designed to provide concise, readable summaries to help users quickly understand the usage of various shell commands.

## Installation

```bash
curl -sSL https://raw.githubusercontent.com/j341nono/HelpSummarizer/main/install.sh | bash
```

## Usage

- Basic usage
    ```bash
    helpsummarizer --command cat
    ```

- Specify a local model file
    ```bash
    helpsummarizer --command cat --model path.to.model
    ```

- Use a model hosted on Hugging Face
    ```bash
    helpsummarizer --command cat --model repository --filename filename
    ```

- Set the maximum number of tokens the model can process
    ```bash
    helpsummarizer --command cat --n_ctx 256
    ```

- Limit the number of characters extracted from the --help output
    ```bash
    helpsummarizer --command cat --n_ctx 256 --help_command_length_limit 300
    ```

## Command Line Arguments

- `--command` (str, required):

    The shell command to summarize (e.g., ls, cat, grep).

- `--model` (str, optional):

    Path to a GGUF model file or a Hugging Face repository (e.g., /path/to/model.gguf, repository_name).

- `--filename` (str, optional):

    Used with Hugging Face models to specify the exact file or variant to load (e.g., gemma-2b, gemma-7b).

- `--n_ctx` (int, optional, default=512):

    Maximum number of context tokens the model can handle in a single prompt.

- `--help_command_length_limit` (int, optional, default=400):

    Maximum number of characters to extract from the output of the --help command.


## Example
```bash
helpsummarizer --command grep --model /models/gemma-2b.gguf --n_ctx 256 --help_command_length_limit 300
```

This command will summarize the grep --help output using a local Gemma model with a context size of 256 tokens, and limit the help text input to 300 characters.
