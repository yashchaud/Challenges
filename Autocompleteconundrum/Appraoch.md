# Approach

Our approach will be very simple:

- Maintain a **hashmap** of `country -> capital` for quick lookups.
- Use a **Trie** to handle **prefix matching** on country names.
- When a user types a query, traverse the Trie to find all matching countries.
- For each match, fetch its capital from the hashmap and return the pair as  
  `Country – Capital`.
- We push results where the **initial prefix matches first**, followed by other matches.
- we stream the data replacing the older ones which no longer matches, with caching this allows for efficient yet realtime autocomplete as we will send first 20 results and then keep streaming in and out from those 20 based on words typed
