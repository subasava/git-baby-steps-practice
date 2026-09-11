# Validate Markdown Formatting Across the Project

Use this instruction when the user wants to review and standardize formatting across all Markdown files in the project.

## Purpose

Validate all Markdown files in the repository for consistent formatting and structure, with a focus on:
- heading hierarchy and heading spacing
- consistent list formatting
- code fence usage and spacing
- link formatting and relative path consistency
- table alignment and readability
- section ordering and document consistency
- removal of obvious formatting drift or duplicate whitespace issues

## Recommended approach

This task should be handled using Approach 2: iterative validation across multiple files.

## Scope

- Review all Markdown files in the project, including top-level docs and nested documentation under folders such as `work/`, `reports/`, `instructions/`, and `hello-genai/`.
- Skip generated or vendor content when appropriate, such as files under hidden folders, dependency folders, or build artifacts.
- Focus on formatting consistency rather than changing technical meaning.

## Instructions for the agent

1. Discover all Markdown files in the repository.
   - Gather the list of `.md` files to review.
   - Exclude irrelevant generated or third-party content when necessary.

2. Validate each file iteratively.
   - For each Markdown file, inspect the content for formatting consistency.
   - Check headings, bullet indentation, spacing, tables, code fences, links, and any repeated structure patterns.
   - Make only formatting-focused edits that do not alter the document’s meaning.

3. Apply fixes consistently.
   - Normalize heading levels where needed.
   - Standardize spacing around headings, lists, and code fences.
   - Fix malformed Markdown that would cause rendering issues.
   - Clean up obvious whitespace and line-break inconsistencies.

4. Re-check after edits.
   - Re-scan the file after making updates.
   - Confirm the formatting is now consistent and no new problems were introduced.

5. Summarize results.
   - Report which files were checked.
   - Report which files were updated.
   - Highlight any files that need manual review because the formatting issue is ambiguous or semantic in nature.

## Validation checklist

Check each Markdown file for the following:

- Heading structure is logical and consistent.
- No heading skips levels unexpectedly.
- Lists use consistent indentation and spacing.
- Bullet and numbered lists are formatted consistently.
- Code fences are properly opened and closed.
- Code blocks have surrounding blank lines where appropriate.
- Links use the correct relative format and are not broken by typos.
- Tables are aligned and readable.
- There is no trailing whitespace or inconsistent blank-line spacing.
- The file reads cleanly when rendered in Markdown viewers.

## Output requirements

Return a concise summary that includes:
- total number of Markdown files reviewed
- number of files updated
- list of files that required formatting fixes
- any remaining issues that may need a human decision

## Example iterative prompt

Use the following prompt when invoking the agent:

"Review all Markdown files in this project for consistent formatting. Use an iterative Approach 2 workflow: first enumerate the Markdown files, then review each file for heading structure, list formatting, code fence spacing, link consistency, and general Markdown readability. Apply only formatting fixes that preserve meaning, then re-check each updated file and provide a final summary of files reviewed, files changed, and any remaining manual review items."

## Notes

- Prefer small, predictable formatting adjustments over large rewrites.
- Do not change content meaning, technical examples, or task instructions unless the formatting issue is clearly incorrect.
- If a Markdown file is highly inconsistent or the intended formatting is unclear, flag it for manual review instead of guessing.
