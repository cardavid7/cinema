# Cinema Frontend

Angular SPA for the [Cinema Reservation API](../README.md): movie catalog, seat selection, reservations, and an admin panel for managing rooms, movies, functions, and seats. Generated with [Angular CLI](https://github.com/angular/angular-cli) `19.2.27`.

## Table of Contents

- [Development server](#development-server)
- [API configuration](#api-configuration)
- [Building](#building)
- [Running unit tests](#running-unit-tests)
- [Deployment](#deployment)

## Development server

By default the app talks to the backend through `/api/v1/...` relative paths, which the Angular dev server proxies to `http://localhost:8000` via [`proxy.conf.json`](proxy.conf.json). Make sure the [backend](../README.md#running-the-application) is running locally first, then:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## API configuration

The backend base URL is controlled by `environment.apiUrl` (see [`src/environments/`](src/environments/)):

| File | Used by | `apiUrl` |
|---|---|---|
| `environment.ts` | `ng serve` / default `ng build` | `''` (empty — relies on the dev proxy or same-origin deployment) |
| `environment.prod.ts` | `ng build --configuration production` (via `fileReplacements` in `angular.json`) | Generated at build time by [`scripts/set-env.js`](scripts/set-env.js) from the `API_URL` environment variable |

To point a production build at a specific backend without touching code, set `API_URL` before building:

```bash
API_URL=https://cinema-backend.onrender.com npm run build:render
```

`npm run build:render` runs `set-env.js` (writing `environment.prod.ts`) and then `ng build --configuration production`. If `API_URL` is left unset, `apiUrl` stays empty, which only works when the frontend is served from the same origin as the API.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Karma](https://karma-runner.github.io) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Deployment

This app is meant to be deployed as a **Static Site**, separate from the [backend](../README.md#deployment). On Render:

- Root directory: `frontend`
- Build command: `npm install && npm run build:render`
- Publish directory: `dist/frontend/browser`
- Environment variable: `API_URL` → the backend's public URL (no trailing slash)
- Add a rewrite rule `/*` → `/index.html` so Angular's client-side routing handles deep links (e.g. `/movies/5`) correctly on refresh.

After the backend is deployed, make sure its `CORS_ORIGINS` environment variable includes this site's URL — otherwise requests from the browser will be blocked. See the root [README's Deployment section](../README.md#deployment) for the full multi-service walkthrough, including the one-step [`render.yaml`](../render.yaml) Blueprint.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
