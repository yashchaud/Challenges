# Solution Approach

I"d build a simple page with a search box at the top. As the user starts typing, I won"t hit the API immediately — instead, I"ll wait until at least 4 characters are typed. At that point, I"ll call TheDogAPI and fetch up to 6 matching dog images. These images will show up right below the search bar in real time, without needing the user to press enter.

Every time the user adds another character, I"ll filter the already-shown results and only keep those that still match. If new results are needed, I"ll fetch again but still cap it to 6 photos to avoid rate limiting. If images take time to load, I can first display breed names as placeholders and replace them with images once they arrive. This keeps the UI responsive and aligned with the requirements, And Lazy Loading ofc.
