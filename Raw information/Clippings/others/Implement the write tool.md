---
title: "Build Your Own Redis, Git & SQLite From Scratch"
source: "https://app.codecrafters.io/courses/claude-code/stages/oz7"
author:
published:
created: 2026-05-31
description: "Advanced programming challenges for experienced engineers. Rebuild real production tools like Redis, Git, and SQLite from scratch in your IDE."
tags:
  - "clippings"
---
Implement the write tool #oz7

In-progress

[Upgrade](https://app.codecrafters.io/pay)

## Your Task

In-progress

Easy

In this stage, you'll add support for the `Write` tool.

### The Write Tool

The `Write` tool enables the LLM to write content to files. Like with the `Read` tool, you need to advertise the `Write` tool in your request and execute it when the model requests it.

Here's the tool specification:

```js
{
  "type": "function",
  "function": {
    "name": "Write",
    "description": "Write content to a file",
    "parameters": {
      "type": "object",
      "required": ["file_path", "content"],
      "properties": {
        "file_path": {
          "type": "string",
          "description": "The path of the file to write to"
        },
        "content": {
          "type": "string",
          "description": "The content to write to the file"
        }
      }
    }
  }
}
```

### Executing the Write Tool

When the model requests a `Write` tool call:

1. Parse the arguments to extract the `file_path` and `content`
2. Write the content to the file at the specified path:
	- If the file doesn't exist, create it
		- If the file exists, overwrite it with the new content
3. Append the result to messages as a tool message (just like with `Read`)

### Tests

The tester will create the following files:

- `README.md` with instructions
- `app/` directory for the project

The tester will then execute your program like this:

```bash
$ ./your_program.sh -p "Read README.md and create the required file. File should have 1 line. Reply with 'Created the file'"
Created the file
```

The tester will verify that:

- The required file is created with the correct contents
- Your program exits with exit code `0`

### Notes

- You can choose any reasonable name for the Write tool (e.g., `Write`, `write`, `write_file`, `WriteFile`).

### How to pass this stage

1

Write code to pass this stage

Head over to your editor / IDE and implement your solution.

If you want a quick look at what functions to use or how to structure your code, we recommend looking at [Code Examples](https://app.codecrafters.io/courses/claude-code/stages/oz7/code-examples).

2

Submit code

To run tests, make changes to your code and run the submit command:

```
codecrafters submit # Visit https://codecrafters.io/cli to install
```

Test Runner:

Ready to run tests

## Hints

Filter by Python

Write

Preview

[Python LEADERBOARD](https://app.codecrafters.io/leaderboards/python)

Complete this stage to hit #9834

Ready to run tests

Show logs