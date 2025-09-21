# Calculator Chatbot with Memory

## What we're building

A smart calculator that remembers your previous calculations. You can say things like "add 12 and 14", then "multiply by 5", then "subtract the first result".

```
User: Add 12 and 14
Bot: 26

User: Multiply by 5
Bot: 130

User: Subtract the first result
Bot: 104
```

## Enhanced approach with RAG

We're using **RAG (Retrieval-Augmented Generation)** to make it truly smart without giving it a "brain". Think of it as a super-smart filing system that understands meaning.

The system has:

- Calculator engine (does the actual math - no AI here)
- Vector store (remembers calculations with embeddings)
- Semantic search (finds similar past calculations)

### How it works

Instead of just storing numbers, we store the **meaning** of each calculation:

- "split rent among 3 people" gets stored with its embedding
- When you say "do the rent thing again but for 4 people", it finds that calculation
- Then it just changes the number and does normal math

### What it can do

1. **Track everything**: "Show me the final total after all those additions"
2. **Remember context**: "Did we add 2 somewhere?" or "When did Ram add rice to the calculation?"
3. **Jump around**: "Go back to the 3rd calculation" or "start from the rent calculation"
4. **Smart clearing**: "Clear everything after I added 50" or "clear my last 3 commands"
