# Solution Approach

1. **Data Fetching Layer**

   - Call the NASA EONET `/events` API on app load.
   - From the JSON, extract all unique categories and cache them locally (to avoid multiple API calls).

2. **Category Selection**

   - Render categories in a dropdown or an input box with autocomplete (filtering client-side from the cached categories).
   - On selection, filter the already-fetched events by the chosen category (instead of calling the API again, unless pagination/large data requires server calls).

3. **Event Display**

   - Show the list of events for that category with their metadata (title, date, etc.).
   - Extract the geo-coordinates from each event and prepare markers for Google Maps.

4. **Map Integration**

   - Embed a Google Map (iframe or Maps JavaScript API).
   - Plot markers for all event geo-coordinates.
   - Clicking a marker highlights the event details in a popup inside the app.

5. **Optimization**
   - Use client-side caching to avoid redundant API calls.
   - Lazy-load the map only when events are selected to reduce initial load.
   - Allow real-time autocomplete for categories to improve user experience.
