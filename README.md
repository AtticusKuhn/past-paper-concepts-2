# Past Paper Concept Analyzer

A system for analyzing Cambridge Computer Science Tripos past papers to extract, store, and analyze key concepts and themes.

The goal is to build a database of common concepts in the CS tripos to help students in revising.
The ideal is to build, for example, an sqlite database of concepts, as well as data about those concepts
such as in what papers/sections those concepts appear in, what course those concepts are a part of, etc.
Thus, Cambridge students can use an sql browser such as `sqlitebrowser` to query the concepts and
figure out most effectively how to study.

The way of implemeneting this is to upload the PDF of each solutions paper to an LLM that
supports vision capabilities, and asking that LLM to extract the key concepts of that solutions paper.

The solutions papers can be downloaded online, so this tool should also support mass-downloading of papers.

There are multiple subjects in the tripos, so this tool should be careful not to mix up questions from separate subjects, but to keep the subjects organised.

# Difficult Issues
These are the key challenges in implementing such a project

- How to get the LLM to use a consistent or canonical naming scheme across all papers? For example, if it extracts the concepts `Bellman-Ford` from one question and `Bellman-Ford-Moore` from a different paper, those two concepts will be treated as different concepts in the database, even though they are the same concept.
- Downloading the solutions to a given paper is only permitted to students, so the tool should have a way to allow students to set the cookie request header on the tool to permit it to download the solutions.
