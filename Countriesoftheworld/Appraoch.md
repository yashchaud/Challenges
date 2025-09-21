# Solution Approach

I"ll start with a simple input form where the user can type the country name. To make it smoother, I"d plug in the RestCountries API so that as the user types, it autocompletes valid country names. Once a country is selected, I"ll fetch its details from RestCountries — that gives me the capital, currency, and other metadata.

Next, I"ll use the capital city to hit a weather API (like OpenWeatherMap) and display current weather. On top of that, I can map keywords like “rain” or “sun” from the weather response to show a relevant image, just to make the app more lively. For exchange rates, since we need USD as the base, I"ll call the currency API with the country"s currency. But instead of hardcoding USD everywhere, I"d prefer detecting the user"s browser location and automatically converting into their local currency, which feels more natural to the user.

This way, everything ties together: country details, real-time weather, context-aware images, and currency exchange — all driven directly from the user"s input without extra manual steps.
