import requests

def steam_app_name(steam_url):
    # Convert URL to AppID
    url_parts = steam_url.split('/')
    app_id = url_parts[-1]

    # Construct the Steam API URL to get app details
    api_url = f'https://store.steampowered.com/api/appdetails?appids={app_id}'
    
    # Make a request to the Steam API
    response = requests.get(api_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Check if the app details are available
        if str(app_id) in data and data[str(app_id)]['success']:
            app_data = data[str(app_id)]['data']
            
            # Retrieve the executable name
            app_name = app_data.get('name')
            
            if app_name:
                return app_name
            else:
                return "Application name not found."
        else:
            return "Failed to retrieve app details."
    else:
        return f"Failed to fetch data from Steam API. Status code: {response.status_code}"
    
def get_app_name(launch_url):
    if launch_url.startswith("steam://"):
        return steam_app_name(launch_url)
    else:
        print("Unknown Platform URL")
        exit(-1)

print(get_app_name("steam://rungameid/1118310"))