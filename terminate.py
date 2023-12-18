import system_calls as system

pid = system.load_data()
print(pid)

system.terminate_process(pid)
