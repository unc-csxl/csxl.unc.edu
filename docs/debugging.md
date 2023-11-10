# Debugging Documentation

## Frontend Debugging

Using Google Chrome, inspect the page or open developer tools.

Navigate to the `Sources` tab.

Look for `Authored`, expand it to `webpack://` and look for your `src` directory. From here you can navigate to TypeScript files powering your frontend components, widgets, and services. Navigate to the typescript file in question and you can add debug breakpoints.

For more on the Chrome debugger, see the [official documentation](https://developer.chrome.com/docs/devtools/javascript/).

## Backend Debugging

To debug running backend API code, you'll need to start the backend using a different strategy than `honcho`. Go ahead and stop honcho, if running, thus killing your frontend and backend dev servers.

In VSCode, navigate to the debugger pane (play button with a bug icon).

Click the link to "Create a launch.json" file. Select Python, then FastAPI, then accept the defaults until the `launch.json` file is opened up.

In configurations, change the `args` to include `backend.main` and add the following `"envFile"` setting so that your backend has access to the environment variables stored in your `backend/.env` file.

~~~
            "args": [
                "main:app",
                "--reload"
            ],
            "envFile": "${workspaceFolder}/backend/.env",
~~~

Try launching the debugger by pressing the play button in the sidebar. You can close the popup about creating a virtual environment. In a terminal, you should see "Application startup complete."

This will run your FastAPI backend API application on port 8000 of localhost, try navigating to <http://127.0.0.1:8000/docs> and you should see your API end-points.

Now, open the backend API or Service module in question, add a breakpoint in VSCode, and attempt to call the API endpoint via the docs API browser. Back in VSCode you should see the debugger paused.

For more on the Python debugger in VSCode, see the [official documentation](https://code.visualstudio.com/docs/editor/debugging#_breakpoints).

It is worth noting, you can debug your Pytest Unit/Integration tests from VSCode's built-in testing tool as described in the [testing documentation](./testing.md).

TODO: Add documentation for debugging in the backend while ensuring the frontend is still running! The current documentation is limited to debugging the backend via the `/docs` UI.