# Memory Bot – AI Chatbot with Conversation Memory

## Project Overview

Memory Bot is a locally running AI-powered chatbot application developed using Python, Streamlit, LangChain, and Ollama.

The main purpose of this project is to provide an interactive chatbot that can communicate with users, understand their questions, and generate meaningful responses using a locally running Large Language Model (LLM).

Unlike a basic chatbot, Memory Bot maintains conversation history for each chat. It allows users to create multiple conversations, switch between previous chats, and continue their discussions without losing saved messages.

The application stores chat conversations in a JSON file, making it possible to access previous conversations even after restarting the application.

This project demonstrates how Large Language Models can be integrated into a user-friendly web application with local storage and conversation memory.

## Objectives

- To develop an AI-powered chatbot using a locally running language model.
- To maintain conversation history for better interaction.
- To provide multiple chat sessions.
- To store and retrieve conversations using JSON.
- To create a simple and attractive user interface using Streamlit.
- To understand the integration of LangChain with Ollama.
- To run an AI chatbot locally without depending on cloud-based AI APIs.

## Features

### 1. AI-Powered Conversations

- Generates intelligent responses using the Llama 3.2 language model.
- Answers user questions in a conversational format.
- Provides real-time streaming responses.

### 2. Conversation Memory

- Maintains previous messages within each chat.
- Uses conversation history to generate context-aware responses.
- Keeps the latest 12 messages as the conversation memory window.

### 3. Multiple Chat Sessions

- Create new conversations whenever required.
- Switch between previously created chats.
- Automatically generates unique chat IDs.
- Maintains separate conversation histories.

### 4. Chat History Storage

- Stores conversations in a `chats.json` file.
- Saves user messages and AI responses.
- Loads previously saved conversations when the application starts.
- Allows users to delete unwanted conversations.

### 5. Model Selection

- Supports selecting locally available Ollama models.
- Uses Llama 3.2 as the default model.
- Allows users to change the AI model based on availability.

### 6. Creativity Control

- Includes a temperature slider.
- Allows users to control the creativity of AI responses.
- Lower values produce more focused responses.
- Higher values allow more creative responses.

### 7. Interactive User Interface

- Developed using Streamlit.
- Includes a sidebar for chat management.
- Provides separate chat bubbles for user and assistant messages.
- Includes suggested prompts for starting conversations.
- Uses custom CSS styling for an attractive interface.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application development |
| Ollama | Running AI models locally |
| Llama 3.2 | Large Language Model |
| LangChain | Managing AI conversations |
| LangChain Core | Handling chat messages |
| LangChain Ollama | Connecting LangChain with Ollama |
| JSON | Storing conversation history |
| UUID | Generating unique chat IDs |
| Pathlib | Managing file paths |
| CSS | Custom user interface styling |

## Project Structure

```text
Memory-Bot/
│
├── app.py
├── chats.json
├── requirements.txt
└── README.md
```

### File Description

- **app.py:** Main Python application containing chatbot logic, Streamlit interface, Ollama integration, and conversation management.
- **chats.json:** Stores chat history, user messages, and AI-generated responses.
- **requirements.txt:** Contains the Python packages required to run the application.
- **README.md:** Provides project information, installation steps, and usage instructions.

## Installation and Setup

### Step 1: Install Python

Download and install Python from:

https://www.python.org/downloads/

Check the Python installation:

```bash
python --version
```

### Step 2: Install Ollama

Download Ollama from:

https://ollama.com/download

Install Ollama on your system.

### Step 3: Download the Llama 3.2 Model

Open Command Prompt or VS Code Terminal and execute:

```bash
ollama pull llama3.2
```

This downloads the Llama 3.2 model to your local system.

### Step 4: Create a Project Folder

Create a folder named:

```text
Memory-Bot
```

Open this folder using Visual Studio Code (VS Code).

### Step 5: Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

### Step 6: Install Required Libraries

Create a `requirements.txt` file and add:

```text
streamlit
langchain-core
langchain-ollama
ollama
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### Step 7: Run the Application

Make sure Ollama is running and execute:

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

Default local URL:

```text
http://localhost:8501
```

## How to Use the Application

1. Open the Memory Bot application in your browser.
2. The welcome screen displays the chatbot introduction.
3. Select one of the suggested prompts or enter your own question.
4. The AI chatbot generates a response using the selected Ollama model.
5. Continue the conversation with additional questions.
6. Use the New Chat button to start another conversation.
7. Select previous chats from the sidebar to continue an earlier discussion.
8. Use the delete button to remove unwanted conversations.
9. Change the AI model using the Model selection option.
10. Adjust the Creativity slider to control response generation.

## How Conversation Memory Works

Memory Bot uses conversation history to maintain context during a chat session.

Whenever a user sends a message:

1. The application receives the user's input.
2. Previous messages are retrieved from the current chat.
3. The latest conversation messages are converted into LangChain message objects.
4. A system prompt is added to define the chatbot's behaviour.
5. The conversation history and new question are sent to the Ollama language model.
6. The AI generates a response.
7. Both the user message and AI response are stored in `chats.json`.

This process helps the chatbot generate responses based on the previous conversation.

**Note:** The application maintains a limited conversation context of the latest 12 stored messages per chat. The full chat history is saved separately in the JSON file. It does not currently implement permanent semantic memory or a vector database.

## Application Screenshots

Add your project screenshots in this section after running the application.

Example:

```markdown
![Memory Bot Home Page](screenshots/home.png)

![Memory Bot Chat Interface](screenshots/chat.png)

![Memory Bot Chat History](screenshots/history.png)
```

## Advantages

- Runs locally using Ollama.
- No external AI API key is required.
- Supports multiple conversations.
- Saves chat history automatically.
- Provides context-aware AI responses.
- Simple and user-friendly interface.
- Allows flexible model selection.
- Demonstrates practical AI application development.

## Future Enhancements

The project can be improved with the following features:

- Add long-term memory using vector databases.
- Implement document-based question answering.
- Add voice input and voice responses.
- Support image understanding.
- Add user authentication.
- Export conversations as PDF or text files.
- Implement chat search functionality.
- Add dark and light themes.
- Improve memory management using embeddings and semantic search.

## Learning Outcomes

Through this project, I learned:

- How to develop interactive applications using Streamlit.
- How to integrate locally running LLMs using Ollama.
- How to use LangChain for managing conversations.
- How to maintain conversation history.
- How to store and retrieve data using JSON files.
- How to implement multiple chat sessions.
- How to customize application interfaces using CSS.
- How to connect Python applications with AI language models.

## Author

**Keerthana**

B.Sc. Computer Science with Artificial Intelligence

## License

This project is created for educational and learning purposes.

---

**Memory Bot – Your Local AI Assistant with Conversation Memory**
