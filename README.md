# Legacy Safety Net
A tool that automatically writes tests for old Java code.

"The goal is not refactoring. The goal is safety."

## Why I Built This

Refactoring old code (legacy code) is dangerous because it often lacks tests. If you change one line, you might break the whole system without knowing.

I built this tool to create a "Safety Net". It records how the code behaves right now so developers can change it with confidence later.

## What It Does

This tool uses the "Golden Master" testing technique:

Watches your Java application run.

Captures the output (return values) of a specific method.

Saves that output as a JSON file (Snapshot).

Generates a standard JUnit 5 test file automatically.

If you change the code and the output changes, the test fails.

## How It Works

Python orchestrates the process.

Java Reflection runs inside the application to spy on data.

Gson saves the object state to a file.

## Usage
"python cli.py src_legacy --main LegacyApp --method getUserData" 