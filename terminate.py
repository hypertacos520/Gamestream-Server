import system_calls as system
import sys

if __name__ == "__main__":
    # Check if at least one command-line argument is provided
    if len(sys.argv) < 2:
        print("Usage: python terminate.py <game_name>")
        exit(-1)

    # Get Game Name
    # game_name = platform_api.get_app_name(sys.argv[1])
    game_name = sys.argv[1]

    pid = system.get_pid_by_name(game_name)
    print(pid)
    if not pid == None:
        system.terminate_process(pid)
    else:
        print(f"No process found with name: '{game_name}'\nUsing fallback method")
        system.force_terminate_process()
