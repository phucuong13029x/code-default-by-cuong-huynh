import time
import sys


sys_call_stack   = {}
sys_folder_trace = os.path.join(pathlib.Path.cwd(), 'app')

def trace_events(frame, event, arg):
    func_n = frame.f_code.co_name
    func_f = frame.f_code.co_filename
    func_l = frame.f_code.co_firstlineno
    if sys_folder_trace not in func_f: return trace_events
    if event == "call":
        unique_id = f"{time.time():.6f}"
        sys_call_stack[frame] = (unique_id, time.time())
        debuglogs.debug(f"[ID: {unique_id}] Call: {func_n}() in {func_f}:{func_l}")
    elif event == "return":
        if frame in sys_call_stack:
            unique_id, start_time = sys_call_stack.pop(frame)
            duration = time.time() - start_time
            debuglogs.debug(f"[ID: {unique_id}] Return: {func_n}() executed in {duration:.6f} sec")
    elif event == "exception":
        exc_type, exc_value, _ = arg
        debuglogs.debug(f"[EXCEPTION] {func_n}() in {func_f}:{func_l} -> {exc_type.__name__}: {exc_value}")
    return trace_events

sys.setprofile(trace_events.trace_events)
