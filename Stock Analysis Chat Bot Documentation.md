**Project Overview: Stock Analysis Chat Bot**

### **1\. Code Logic Explanation**

The bot is built using **Python**, **Streamlit**, and the **Google Gemini API**. It acts as a bridge between your raw CSV data and AI-driven insights.

#### **A. File Management & Upload**

* **The Problem:** On Windows, CSV files are often misidentified as Excel files, which the Gemini API rejects.  
* **The Fix:** In the upload\_data\_files function, we manually set the mime\_type to text/csv. This ensures the API accepts the files for its **Code Execution** engine.  
* **Caching:** We use @st.cache\_resource so the files are uploaded only once per session, saving you API quota and time.

  #### **B. The Brain: chat\_with\_data Function**

This is where the magic happens. We use **Gemini 2.0 Flash** with a specific configuration:

* **System Instructions:** We give the AI a clear personality and strict rules. We tell it exactly which file to use for which question and forbid it from using outside knowledge.  
* **Code Execution Tool:** Instead of the AI "guessing" the numbers, it generates and runs a Python script (using libraries like pandas) to calculate the exact values from your CSVs.  
* **Zero Temperature:** We set temperature=0.0 to ensure the bot is strictly factual and doesn't get creative with your financial data.

  #### **C. Streamlit User Interface**

* **API Security:** The API key is entered via a masked sidebar input, ensuring it's never hardcoded in the script.  
* **Session State:** We use st.session\_state to keep a history of your chat, allowing for a continuous, conversational experience.

**2\. Output Analysis** 

| Question Type | Example from Video | Bot Response Logic |
| :---- | :---- | :---- |
| **Data Extraction** | "What is the total quantity traded for FB in Northpoint 401K?" | The bot wrote Python code to filter the trades.csv for "Northpoint 401K" and "FB," then summed the quantity column to return **35,000.0**. |
| **Complex Calculation** | "What is the total Quantity for Garfield for security EJ0445951?" | The bot located the "Garfield" portfolio in holdings.csv, found the specific security, and performed a precise sum to get **2,784,588.0**. |
| **Irrelevant Question** | "In which year did India win the World Cup?" | **This is the most important part of the demo.** Because of our strict system prompt ("Do not use outside knowledge"), the bot followed instructions and replied: **"Sorry can not find the answer."** |

