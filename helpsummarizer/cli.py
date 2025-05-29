import argparse
import subprocess
import sys
import os
import contextlib
from llama_cpp import Llama
from helpsummarizer.spinner import Spinner
from helpsummarizer.ascii_art import display_helper_ascii


HOME = os.environ["HOME"]
DEFAULT_MODEL_PATH = os.path.join(HOME, ".helpsummarizer/models/llama-3.2-3b-instruct-q4_k_m.gguf")


def parse_args():
    # 簡易パーサで --help を検出（先に help チェック用）
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--help", action="store_true")
    pre_args, _ = pre_parser.parse_known_args()

    if pre_args.help:
        display_helper_ascii()

    # 本番パーサ
    full_parser = argparse.ArgumentParser(
        description="Summarize the --help output of a given command using a local LLM."
    )
    full_parser.add_argument("--command", type=str, required=True, help="The command you want help with (e.g., ls)")
    full_parser.add_argument("--model", type=str, default=None, help="Specify the path to the GGUF model file (e.g., /path/to/model.gguf).")
    full_parser.add_argument("--filename", type=str, default=None, help="Specify the filename or size variant of the GGUF model (e.g., gemma-2b, gemma-7b).")
    full_parser.add_argument("--n_ctx", type=int, default=512, help="The maximum number of context tokens the language model can handle in a single prompt.")
    full_parser.add_argument("--help_command_length_limit", type=int, default=400, help="The maximum number of characters to capture from the output of the '--help' command.")

    # --help のときだけ ASCIIアートを先に表示
    if pre_args.help:
        full_parser.print_help()
        sys.exit()
    return full_parser.parse_args()


def get_help_output(args):
    """ execute in background """
    try:
        result = subprocess.run([args.command, '--help'], capture_output=True, text=True, check=True)
        output = result.stdout
        return output[:args.help_command_length_limit]
    except subprocess.CalledProcessError:
        return -1
    except FileNotFoundError:
        return -1


@contextlib.contextmanager
def suppress_output():
    with open(os.devnull, 'w') as fnull:
        with contextlib.redirect_stdout(fnull), contextlib.redirect_stderr(fnull):
            yield


def load_model(args):
    with suppress_output():
        if args.model is None:
            return Llama(model_path=DEFAULT_MODEL_PATH, verbose=False, n_ctx=args.n_ctx, chat_format="llama-3")
        elif os.path.exists(args.model):
            try:
                return Llama(model_path=args.model, verbose=False, n_ctx=args.n_ctx)
            except Exception:
                return -1
        else:
            try:
                target_model_path = os.path.join(HOME, ".helpsummarizer/models/", args.filename)
                return Llama(model_path=target_model_path, verbose=False, n_ctx=args.n_ctx)

            except Exception:
                print("Model not found in cache. Trying to download via download.sh...")
                # download.shの実行（失敗したら戻り値コードで検知）
                try:
                    subprocess.run(["bash", "download.sh", args.model, args.filename], check=True)
                except subprocess.CalledProcessError as e:
                    print("Download failed:", e)
                    return -2

                # ダウンロード成功後、ローカルモデルとして再読み込みを試みる
                try:
                    model_path_after_dl = os.path.join(HOME, ".helpsummarizer/models/", args.filename)  # ダウンロード先が "models/<model>" だと仮定
                    return Llama(model_path=model_path_after_dl, verbose=False, n_ctx=args.n_ctx)
                except Exception as e:
                    print("Failed to load model after download:", e)
                    return -2
        

def get_llm_response(help_output, llm):
    spinner_stopped = False
    spinner = Spinner("thinking ")
    spinner.start()

    content = (
        "The following text is the output of a command's --help option."
        "Please summarize it and explain only the important parts concisely."
        "Do not include asterisks (*) in the output, and remove unnecessary details such as overly specific option descriptions or repetitive explanations."
        "Make sure to convey the purpose of the command, its main usage, and representative options."
    )
    messages = [
        {"role": "system", "content": content},
        {"role": "user", "content": help_output},
    ]

    try:
        for chunk in llm.create_chat_completion(
            messages=messages, 
            max_tokens=300, 
            stream=True,
            ):
            delta = chunk["choices"][0]["delta"]
            if "content" in delta:
                print(delta["content"], end="", flush=True)

            if not spinner_stopped:
                if "content" in delta:
                    spinner.stop()
                    spinner_stopped = True
    finally:
        if not spinner_stopped:
            spinner.stop()

def main():
    args = parse_args()
    try:
        llm = load_model(args)
        if llm == -1:
            print("Error: Please specify a valid path.")
            sys.exit()
        elif llm == -2:
            print(f"Error: loading model from repo")
            sys.exit()

        help_output = get_help_output(args)
        if llm == -1:
            print(f"Error: The specified UNIX command was not found. Please enter a valid command.")
            sys.exit()

        get_llm_response(help_output, llm)
        print()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()

