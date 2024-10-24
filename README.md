# Zeotap Assignment

This repository contains two distinct applications developed using Python and Streamlit for real-time data processing and dynamic rule evaluation.
---

## 1. Rule Engine with AST

### Overview

The Rule Engine with AST is a simple rule engine that determines user eligibility based on various attributes (such as age, department, income, spend, etc.). The engine dynamically creates, modifies, and evaluates rules using an Abstract Syntax Tree (AST), enabling easy manipulation and combination of rules.

### Key Features

- **Create Rules**: Define rules using a custom syntax and convert them into an AST.
- **Combine Rules**: Efficiently merge multiple rules into a single AST representation.
- **Modify Rules**: Update existing rules by altering operators, operands, or expressions.
- **Evaluate Rules**: Check if user data satisfies predefined rules.
- **Error Handling & Attribute Validation**: Includes robust handling of invalid inputs and ensures only predefined attributes (e.g., age, department, salary, experience) are used.

### Example Rule

```plaintext
(age > 25 AND department == 'Engineering') OR (experience >= 5 AND salary > 70000)
```

### Technology Stack

- **SQLite Database** for storing rules and ASTs.
- **SQLAlchemy ORM** for database interactions.
- **Streamlit** for the front-end interface.

### API Functions

- `create_rule(rule_string)`: Parses the rule string into an AST.
- `combine_rules(rules)`: Combines multiple rules into one.
- `evaluate_rule(ast, data)`: Evaluates the given AST against the provided user data.

### Usage

1. **Create a Rule**: Input a custom rule string and convert it into an AST.
2. **Combine Rules**: Select multiple rules to merge into one.
3. **Evaluate a Rule**: Test if a set of user data satisfies a given rule.
4. **Modify a Rule**: Update an existing rule with new logic.

---

## 2. Real-Time Weather Monitoring and Alerts System

### Overview

This system allows users to monitor real-time weather data for multiple cities, set temperature thresholds, and receive alerts via email if specific conditions are met. The system integrates with the OpenWeatherMap API and uses LLMs to generate concise weather summaries.

### Key Features

- **Real-Time Weather Monitoring**: Track temperature, humidity, wind speed, and more.
- **Temperature Alerts**: Set thresholds and receive email notifications when conditions are met.
- **LLM-Generated Summaries**: Get concise two-line weather summaries for each city.
- **Interactive Visualizations**: Visualize temperature changes over time.
- **Automatic Data Fetching**: Fetches weather data every 5 minutes.

### Example Weather Summary

```plaintext
Current temperature in [City] is 30°C, with clear skies. Humidity levels are moderate.
```

### Technology Stack

- **OpenWeatherMap API** for real-time weather data.
- **Firebase** for storing and retrieving weather data.
- **Streamlit** for the front-end dashboard.
- **Mailgun** for sending email alerts.

### Main Components

- **Data Fetcher**: Pulls weather data from the API and stores it in Firebase.
- **Alert System**: Monitors temperature thresholds and triggers email notifications.
- **LLM Summary Generator**: Uses an LLM to produce short weather summaries.
- **UI**: Provides a user-friendly interface for monitoring weather conditions and setting alert preferences.

### Usage

1. **Set Preferences**: Select a city, set temperature thresholds, and choose email alerts.
2. **Monitor Weather**: View real-time weather data and summaries for the selected city.
3. **Receive Alerts**: Get email notifications if the temperature exceeds your specified thresholds.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- API keys for OpenWeatherMap and Gemini

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AnKiTu03/Zeotap-assignment.git
   cd Zeotap-assignment
   ```

2. **Create a Virtual Environment (Optional)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file with API keys for OpenWeatherMap, Gemini, and other services as needed.

5. **Run the Application**:
   - For Rule Engine:
     ```bash
     streamlit run app.py
     ```
   - For Weather Monitoring:
     ```bash
     streamlit run frontend/app.py
     ```

---

**Live Demos**:

- [Weather Monitoring System](https://weather-zeotap.streamlit.app/)
- [Rule Engine with AST](https://ast-zeotap.streamlit.app/)

--- 
