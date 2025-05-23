class SubprocessWorker(GObject.GObject):
    __gsignals__ = {
        "output_line": (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        "error_line":  (GObject.SignalFlags.RUN_FIRST, None, (str,)),
        "finished":    (GObject.SignalFlags.RUN_FIRST, None, (int,))
    }

    def __init__(self, command):
        super().__init__()
        self.command = command

    def start(self):
        thread = threading.Thread(target=self._run_process, daemon=True)
        thread.start()

    def _run_process(self):
        process = subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        def read_stream(stream, signal_name):
            for line in stream:
                GLib.idle_add(self.emit, signal_name, line)
            stream.close()

        stdout_thread = threading.Thread(target=read_stream, args=(process.stdout, "output_line"))
        stderr_thread = threading.Thread(target=read_stream, args=(process.stderr, "error_line"))

        stdout_thread.start()
        stderr_thread.start()

        stdout_thread.join()
        stderr_thread.join()

        exit_code = process.wait()
        GLib.idle_add(self.emit, "finished", exit_code)
