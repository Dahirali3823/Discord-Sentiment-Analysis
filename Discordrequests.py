import requests
import json
import time
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

def retrieve(channelid):
    # Retrieve the token from the environment variable
    token = os.getenv('DISCORD_TOKEN')
    if not token:
        print("Error: DISCORD_TOKEN not found in environment variables.")
        return

    headers = {
        'authorization': f'Bot {token}'  # Use the token securely
    }
    
    # Base URL for the API endpoint
    base_url = f'https://discord.com/api/v9/channels/{channelid}/messages?limit=100'
    last_message_id = 1083959512672772096  # Track the ID of the last fetched message
    
    # Clear or initialize the JSON file
    with open('/Users/dahirali/Desktop/Sentiment analysis/messages.json', 'r', encoding='utf-8') as f:
         existing_data = json.load(f)
    
    while True:
        url = base_url
        if last_message_id:
            # Add the "before" parameter to paginate
            url += f"&before={last_message_id}"
        
        # Fetch messages
        print(f"Fetching messages from URL: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        
        jsonn = response.json()
        
        # If no more messages are returned, stop the loop
        if not jsonn:
            break
        
        # Filter messages from the target user and not starting with 'http'
        userid = '680518145219625098'
        filtered_messages = [
            value['content']
            for value in jsonn
            if value['author']['id'] == userid and not value['content'].startswith('http')
        ]
        
        # Append messages incrementally to the JSON file
        with open('/Users/dahirali/Desktop/Sentiment analysis/messages.json', 'r+', encoding='utf-8') as f:
            # Load existing data
            existing_data = json.load(f)
            # Extend the list with new filtered messages
            existing_data.extend(filtered_messages)
            # Move the cursor to the beginning of the file and overwrite
            f.seek(0)
            json.dump(existing_data, f, indent=4, ensure_ascii=False)
        
        # Update last_message_id for pagination
        last_message_id = jsonn[-1]['id']
        
        # Avoid hitting Discord's rate limit
        time.sleep(1)
    print("Fetching complete!")

# Call the function with the channel ID
retrieve('851310878888558614')
