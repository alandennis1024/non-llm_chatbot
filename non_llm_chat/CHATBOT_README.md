# Non-LLM Chatbot

A Flask-based chatbot application using the ChatterBot library, designed for deployment with Databricks Asset Bundles. This chatbot provides conversational AI capabilities without relying on large language models (LLMs).

## Features

- **Basic Chatbot**: Pattern-matching chatbot using ChatterBot library
- **Flask Web Interface**: Web-based chat interface with REST API
- **Command Line Interface**: Terminal-based chat interface
- **Databricks Integration**: Ready for deployment with Databricks Asset Bundles
- **Multiple Bot Management**: Support for managing multiple chatbot instances
- **Training Capabilities**: Train bots with custom conversation data

## Project Structure

```
non_llm_chat/
├── src/
│   └── non_llm_chat/
│       ├── __init__.py          # Package initialization
│       ├── chatbot.py           # Core chatbot classes
│       ├── flask_app.py         # Flask web application
│       └── main.py              # Main entry point
├── resources/
│   └── non_llm_chat.job.yml     # Databricks job configuration
├── databricks.yml               # Databricks bundle configuration
├── pyproject.toml               # Python package configuration
├── requirements.txt             # Python dependencies
└── demo.py                      # Demo script
```

## Dependencies

- **Flask**: Web framework for the REST API and web interface
- **ChatterBot**: Core chatbot functionality
- **SQLAlchemy**: Database backend for conversation storage
- **PyYAML**: Configuration file parsing

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the Python wheel** (for Databricks deployment):
   ```bash
   uv build --wheel
   ```

## Usage

### Web Interface

Start the Flask web application:
```bash
python -m non_llm_chat.main --mode web
```

The web interface will be available at `http://localhost:5000`. You can:
- Chat with the bot through the web interface
- Use the REST API endpoints

### Command Line Interface

Run the chatbot in CLI mode:
```bash
python -m non_llm_chat.main --mode cli
```

### Training Mode

Train a bot with custom data:
```bash
python -m non_llm_chat.main --mode train --bot-name MyBot --training-data conversations.txt
```

### Demo Script

Run the demonstration script to see all features:
```bash
python demo.py
```

## REST API Endpoints

### Chat with Bot
- **POST** `/api/chat`
- **Body**: `{"message": "Hello", "bot_name": "optional"}`
- **Response**: `{"response": "Hi there!", "bot_name": "DefaultBot", "status": "success"}`

### List Bots
- **GET** `/api/bots`
- **Response**: `{"bots": ["DefaultBot"], "status": "success"}`

### Create Bot
- **POST** `/api/bots`
- **Body**: `{"name": "NewBot", "train_basic": true}`
- **Response**: `{"message": "Bot created successfully", "bot_name": "NewBot", "status": "success"}`

### Train Bot
- **POST** `/api/train`
- **Body**: `{"bot_name": "MyBot", "conversations": ["Hello", "Hi!", "Goodbye", "Bye!"]}`
- **Response**: `{"message": "Training completed successfully", "status": "success"}`

### Health Check
- **GET** `/health`
- **Response**: `{"status": "healthy", "service": "non-llm-chatbot"}`

## Databricks Deployment

### Prerequisites

1. Install Databricks CLI
2. Configure authentication with your Databricks workspace

### Deploy with Asset Bundle

1. **Deploy the bundle**:
   ```bash
   databricks bundle deploy
   ```

2. **Run the job**:
   ```bash
   databricks bundle run non_llm_chat_job
   ```

### Job Configuration

The Databricks job includes two tasks:

1. **chatbot_web_app**: Runs the Flask web application
2. **chatbot_training_task**: Trains a production bot with custom data

The job configuration is defined in `resources/non_llm_chat.job.yml`.

## Configuration Options

### Command Line Arguments

- `--mode`: Run mode (web, cli, train)
- `--host`: Host address for web mode (default: 0.0.0.0)
- `--port`: Port number for web mode (default: 5000)
- `--debug`: Enable debug mode for web mode
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--bot-name`: Bot name for train mode
- `--training-data`: Path to training data file for train mode

### Environment Variables

You can set environment variables to configure the application:
- `FLASK_HOST`: Host address for Flask app
- `FLASK_PORT`: Port number for Flask app
- `LOG_LEVEL`: Logging level

## Development

### Adding New Features

1. **Extend the BasicChatBot class** in `chatbot.py` for new chatbot functionality
2. **Add new Flask routes** in `flask_app.py` for new API endpoints
3. **Update the main entry point** in `main.py` for new command-line options

### Testing

Run the demo script to test all functionality:
```bash
python demo.py
```

### Building for Production

Build the Python wheel for deployment:
```bash
uv build --wheel
```

## Troubleshooting

### Common Issues

1. **ChatterBot Installation Issues**: 
   - Ensure you have the correct version of SQLAlchemy (<2.0.0)
   - Install chatterbot-corpus separately if needed

2. **Flask Import Errors**:
   - Make sure Flask is installed: `pip install Flask`

3. **Database Permissions**:
   - Ensure the application has write permissions for SQLite database files

4. **Databricks Deployment Issues**:
   - Check that all dependencies are listed in requirements.txt
   - Verify the wheel file is built correctly

### Logs

The application logs to standard output. Set log level with `--log-level DEBUG` for detailed logging.

## License

This project is designed for educational and development purposes. Please check the licenses of individual dependencies (ChatterBot, Flask, etc.) for production use.

## Support

For issues related to:
- **Databricks Asset Bundles**: Check the [official documentation](https://docs.databricks.com/dev-tools/bundles/)
- **ChatterBot**: See the [ChatterBot documentation](https://chatterbot.readthedocs.io/)
- **Flask**: Refer to the [Flask documentation](https://flask.palletsprojects.com/)