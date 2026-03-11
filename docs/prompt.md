Together we will end-to-end construct a website to provide information to Australian's regarding what can be recycled in their area. The information is hard to find and the purpose of the website is to be able to quickly surface information to users. Secondly, the purpose of constructing this website is to demonstrate AI coding ability and best practices to technical leads hiring for the role of senior engineer. The source code will be committed to a public repository and should be able to be run locally, and easily deployed to web.

- To be hosted on australiarecycling.com.au
- Should be a cost effective application, balancing cost with proper production design
- Document build process, from product management to figma to code
- Scrape web for information from each area, potentially live data wrapped in an MCP or could be scraped once and stored in a database
- Website with council/location search for info dump on what is recyclable
- Ai agent text input for query, includes langchain workflow and SOP (stored operating procedure) for common questions e.g. "Is X recyclable in A?"
- Image search on item, recycling label/icon to see if an item is recyclable in a given area
- Mobile platform support
- Llm cost tracking and management dashboard

Questions:
- What tech stack is recommended? I would like to use a Java backend if possible. Also familiar frontend technologies are React, Typescript, Vite, Helm
- How would the repository be designed? A mono-repo could be appropriate but open to other options
- How can this be deployed? Preference is using GCP but if there is a simpler and easier option this should be evaluated too.
