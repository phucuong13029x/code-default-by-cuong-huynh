import time
import sys

call_id      = 10000000
call_stack   = {}
folder_trace = '/home/cuong.huynh'

def trace_events(frame, event, arg):
    global call_id
    func_n = frame.f_code.co_name
    func_f = frame.f_code.co_filename
    func_l = frame.f_code.co_firstlineno
    if folder_trace not in func_f: return trace_events
    if event == "call":
        call_id += 1
        call_stack[frame] = (call_id, time.time())
        print(f"[ID: {call_id}] CALL: {func_n}() in {func_f}:{func_l}")
    elif event == "return":
        if frame in call_stack:
            unique_id, start_time = call_stack.pop(frame)
            duration = time.time() - start_time
            print(f"[ID: {unique_id}] RETURN: {func_n}() executed in {duration:.6f} sec")
    elif event == "exception":
        print(f"EXCEPTION in {func_n}() in {func_f}:{func_l}")
    return trace_events

sys.setprofile(trace_events)
