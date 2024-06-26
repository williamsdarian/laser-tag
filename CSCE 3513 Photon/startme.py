import os

from dotenv import load_dotenv

load_dotenv()

from supabase import create_client

import webbrowser



url = "https://xxsgrickhdpcxubeurjk.supabase.co"



key ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inh4c2dyaWNraGRwY3h1YmV1cmprIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDcyNDQ1NDUsImV4cCI6MjAyMjgyMDU0NX0.6RdisJLfJNX6FkK3dx3hR-Ust6A9EdaxCw851uphE7U"



supabase = create_client(url, key)





def insert_player(playerName, playerID):

    if playerName != None:

        supabase.table("CurrentGameTable").insert({"name": playerName, "equipment_id": int(playerID)}).execute()





def clear_table():

    supabase.table("CurrentGameTable").delete().neq('name', '0').execute()

    #supabase.table("playerNameTable").delete().neq("name", "hey").execute()









from flask import Flask, render_template, request, json, jsonify, send_file

import udp_client as uc







app = Flask(__name__)









@app.route('/')

def display_image():

    return render_template('index.html')



@app.route('/play_photon')

def play_photon():

    return render_template('play_photon.html')



@app.route('/game')

def game():

    return render_template('game.html')



@app.route('/load_screen')

def load_screen():

    return render_template('load_screen.html')



@app.route('/get_image')

def get_image():

    return send_file('static/logo.jpg', mimetype='image/jpg')



@app.route('/get_code_name', methods=['POST'])

def getCodeName():

        data = request.get_json()

        playerID = data.get('Player_ID', '')

        data = supabase.table("playerNameTable").select('*').eq('playerID', playerID).execute()

        if len(data.data) != 0:

            playerName = data.data[0]['name']

            return playerName

        else:

            return "missing"

        

           

@app.route('/insertPlayerToDataBase', methods=['POST'])

def insertPlayerToDataBase():

    data = request.get_json()

    playerID = data.get('Player_ID', '')

    codeName=data.get('Code_Name', '')

    supabase.table("playerNameTable").insert({"playerID": playerID, "name": codeName}).execute()

    return '204'





@app.route('/play_photon/start_game', methods=['POST'])

def save_players():

    try:

        clear_table()

        # Get the player names and equipment IDs from the request data

        data = request.get_json()

        player_names = data.get('Player_Names', [])

        equipment_ids = data.get('Equipment_Ids', [])



        for i, id in enumerate(player_names):

            insert_player(id, equipment_ids[i])



        return '204'

 



    except Exception as e:

        print("Error:", e)

        return jsonify({'error': 'An error occurred'}), 500

    





    







@app.route('/get_data')

def get_red_data():

    # Execute a select query on the Supabase table corresponding to the 'team'

    response = supabase.table("CurrentGameTable").select('*').execute()



    players = response.data

    # Return the players data as JSON





    return json.dumps(players)





from flask import Response



@app.route('/send_udp_message', methods=['POST'])

def send_udp_message_route():

    print(request.json.get('message'))

    message = request.json.get('message')  # Get the parameter value from the request

    response_generator = uc.send_udp_message(message) 

     # Get the generator object
    if(response_generator != "Response not Important"):
        print(response_generator)
        print("RESPONSE    " + str(response_generator))
        return Response(response_generator, mimetype='text/event-stream')
    else:
        print("Not Important")
        return ""

    


import threading

from werkzeug.serving import make_server

def run_flask_app():

    # Create a development server with the Flask app

    server = make_server('127.0.0.1', 5000, app)

    server.serve_forever()



def open_browser():

    url = 'http://127.0.0.1:5000'

    try:

        webbrowser.open(url)

        print("Browser opened successfully!")

    except Exception as e:

        print(f"Failed to open browser: {e}")



if __name__ == '__main__':

    # Start Flask app in a separate thread

    flask_thread = threading.Thread(target=run_flask_app)

    flask_thread.start()



    # Wait for Flask app to fully load

    # Since make_server doesn't block, we can skip joining the thread



    # Open the browser after Flask app is fully loaded

    open_browser()

    










    



