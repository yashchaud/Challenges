# RAG Calculator - Natural Language Math Operations

## Why RAG Works Here (Without Smart LLM)

This calculator uses RAG (Retrieval-Augmented Generation) for semantic understanding and transaction history without relying on expensive LLMs for calculations. RAG enables natural language processing through embeddings and vector similarity, allowing the system to understand phrases like "ram takes 5kg from sita" or "reduce from last number" while keeping all mathematical operations deterministic and precise. The embeddings help with typo tolerance, synonym detection, and contextual references, making it far superior to rigid command-based calculators that only accept "add 2" or "subtract 5".

The system maintains user-specific calculation histories, supports time-travel operations ("go back 3 transactions"), and enables complex multi-user scenarios with natural language. Users can say "sita multiply by last result" or "ram reduce 10 from previous number" and the system intelligently maps these to precise mathematical operations while maintaining separate contexts for each user. This approach combines the reliability of traditional calculators with the intuitive interface of natural language processing.

## Setup Instructions

```bash
python -m venv calc_env

# Activate virtual environment
# Windows:
calc_env\Scripts\activate
# Mac/Linux:
source calc_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure MySQL credentials in config.py
# Run the calculator
python main.py
```

## Supported Users

- ram, sita, john, mary, alice, bob, system

## Supported Commands

### Basic Operations

- `ram adds 15kg`, `sita has 20`
- `john multiply 5`, `mary divide by 2`
- `alice reduce 10`, `bob increase 7`

### Transfer Operations

- `ram gives 5kg to sita`
- `sita takes 10kg from ram`
- `john transfers 15 to mary`

### Context References

- `ram adds last number`, `sita multiply by previous result`
- `john reduce from last`, `mary divide by last result`
- `alice add 5 to previous number`

### Time Travel & History

- `ram go back 3 transactions`
- `sita go back to negative balance`
- `clear last 5 transactions for john`
- `sum all previous answers`

### Information & Management

- `ram total`, `sita balance`, `current result`
- `search ram transactions`, `did sita multiply?`
- `clear memory`, `delete all transactions`
- `undo ram last`

## Why This Beats Simple Commands

Instead of rigid `add(2, 3)` syntax, users can naturally say `"ram adds 2kg to previous result"` or `"sita takes half from john's balance"` - the system understands context, handles typos, supports multiple users, and maintains complete transaction history with semantic search capabilities.
