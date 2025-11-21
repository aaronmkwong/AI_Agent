This project builds an LLM “agent” that can take goals in natural language and accomplish them by calling safe, purpose-built functions (“tools”). Each tool is designed to return plain text, enforce strict sandbox boundaries, and handle errors gracefully. The agent plans, calls tools iteratively based on results, and uses the outputs to decide its next steps—like a mini operating system for AI actions.

Tools like file system inspection, reading/writing files, and running commands are wired into an agent loop with guardrails. Prompt design, result parsing, and failure recovery are practiced while keeping the agent constrained to a working directory and a limited capability set. The emphasis is on reliability, safety, and deterministic interfaces—so the agent remains predictable.

Real-world use cases include developer assistants that scaffold projects, refactor code, and run tests; data ops helpers that ingest files, transform them, and produce reports; and customer support workflows that triage tickets, summarize logs, and draft responses. Teams could also use these agents for documentation maintenance, CI/CD triage, and lightweight RPA—automating repetitive tasks safely within predefined boundaries.

NOTE: The program is for demonstration of a personal learning project only and should not be used by anyone other than the author specific to the learning tasks for the Boot Dev course it pertains to as it does not have all the security and safety features that a production AI agent would have. 


<img src="https://github.com/aaronmkwong/AI_Agent/blob/main/sreenshots/251121 1022AM AI Agent Project Screenshot.jpg" width="1000" height="1000">
