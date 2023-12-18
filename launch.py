import platform_api_calls as platform_api
import system_calls as system
import sys

if __name__ == "__main__":
    # Check if at least one command-line argument is provided
    if len(sys.argv) < 2:
        print("Usage: python script.py <argument>")
        exit(-1)

    # Get Game Name
    # game_name = platform_api.get_app_name(sys.argv[1])
    game_name = sys.argv[1]

    # Search for App PID
    pid = None
    while not pid:
        pid = system.get_pid_by_name(game_name)

    # Stash PID
    system.save_data(pid)