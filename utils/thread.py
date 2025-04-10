import threading

active_threads_names = {}

def StarterThread(name, target):
    if name in active_threads_names:
        return
    
    def thread_function():
        target()
        active_threads_names.pop(name, None)
    
    thread = threading.Thread(target=thread_function, daemon=True)
    thread.start()
    active_threads_names[name] = thread
    
def RemoveThread(name):
    print(f"Removing thread {name}")
    if name in active_threads_names:
        # active_threads_names[name].join()
        active_threads_names.pop(name, None)
        return True
    return False