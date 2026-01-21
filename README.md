🤖 Stock Assitant Chat Bot
An AI-powered financial assistant that analyzes personal investment data using Gemini 2.0 Flash and Streamlit. Unlike standard chatbots, this bot uses automated code execution to perform 100% accurate mathematical calculations on your CSV data.

🌟 Key Features
Deterministic Accuracy: Uses Python code execution (Pandas) to calculate totals rather than relying on LLM "math guesses."

Dual-File Context: Cross-references data between holdings.csv (current assets) and trades.csv (transaction history).

MIME-Type Correction: Features a custom handler for Windows-based CSV misidentification issues.

Strict Guardrails: Grounded system instructions prevent the bot from answering non-financial or out-of-scope questions.

🛠️ Tech Stack
Frontend: Streamlit

LLM: Google Gemini 2.0 Flash

Analysis: Google GenAI Code Execution Tool

Language: Python 3.13
