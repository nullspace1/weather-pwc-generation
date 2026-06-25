# Initial Page Construction

Delegate both tasks to one agent each.

## Backend

Create a test suite to verify that each service class does as expected. Use pytest and mock to mock dependencies.

## Frontend

Create an initial page structure, as follows:

```
< header area - contains a logo and all the tabs. for now, just a 'weather' tab >
< main area - contains the main content >
    < inside the main area, for the weather tab >
        <card for searching and selecting a location>
        <card for selecting units>
        <card for generating weather data, with path to where the file will be saved>
    </inside the main area>
< footer area - contains a footer >
```

Maintain the structure of the project. Use:

```
components - reusable react components
assets - static assets
lib - 
    api - api methods
    dto - data transfer objects interfaces
pages - pages
states - reactive state objects
```

Preferably, keep app logic in small state objects with a single responsibility.

Do not test the UI for now.

Set up typescript and linting. Ensure the application looks visually correct

