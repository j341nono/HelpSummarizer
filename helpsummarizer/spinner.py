import threading
import sys
import time
import itertools

class Spinner:
    def __init__(self, message="Loading...", chars="/-\\|", delay=0.1):
        self.message = message
        self.chars = chars
        self.delay = delay
        self._stop_event = threading.Event()
        self._thread = None

    def _spin(self):
        if self.message:
            sys.stdout.write(self.message + " ")
            sys.stdout.flush()
        
        for c in itertools.cycle(self.chars):
            if self._stop_event.is_set():
                break
            # カーソルを行の先頭に戻してスピナー文字を表示
            if self.message:
                sys.stdout.write(f"\r{self.message} {c}")
            else:
                sys.stdout.write(f"\r{c}")
            sys.stdout.flush()
            time.sleep(self.delay)
        
        # スピナーを消去
        clear_length = len(self.message) + 2 if self.message else 1
        sys.stdout.write("\r" + " " * clear_length + "\r")
        sys.stdout.flush()

    def start(self):
        if self._thread is not None and self._thread.is_alive():
            return  # 既に動作中の場合は何もしない
        
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def stop(self):
        if self._thread is not None:
            self._stop_event.set()
            self._thread.join(timeout=1.0)  # タイムアウトを設定
            
            