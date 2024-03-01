## ChatGPT Replica

#### Video Demo:  <URL HERE>

## Description

This project is a web-based chatbot application built with Flask and OpenAI. The application allows users to register, log in, and chat with a bot based on OpenAI.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/tuo-nome-utente/tuo-repo.git
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set the OpenAI API key as an environment variable:

   ```bash
   export OPENAI_API_KEY=your_api_key
   ```

5. Run the application:

   ```bash
   python app.py
   ```

## How to use

After starting the application, visit http://localhost:5000 in your browser to access the chatbot application. Users can register, log in, and chat with the bot.

## Project Files

- `app.py`: This is the main file of the Flask application. It contains the routes, database configurations, and functions to generate bot responses.
  
- `utility.py`: This file contains the login_required decorator, which is used to protect routes that require user authentication. If a user is not authenticated, they will be redirected to the login page.

- `script.js`: This JavaScript file contains the code to send user messages to the backend and display bot responses in the chat interface. It uses jQuery to handle click and keypress events, as well as to send AJAX requests to the server.

- `style.css`: This CSS file contains styles for the user interface of the chatbot application. Styles include formatting for messages, buttons, and the overall layout of the application.

## License

This project is licensed under the[MIT License](LICENSE.md) - see the [LICENSE](LICENSE.md) file for details.

## Contacts

Giacomo Innocenti
