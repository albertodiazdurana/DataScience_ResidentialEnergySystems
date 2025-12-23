# Project Memory

@../project-knowledge/energy-engineering-data-science/08_Project_Handoff.md

# Quick Reference Data Science Methodology (DSM)

## Key Paths
- Methodology: DSM_1.0_Data_Science_Collaboration_Methodology_v1.1.md
- Appendices: DSM_1.0_Methodology_Appendices.md
- PM Guidelines: DSM_2.0_ProjectManagement_Guidelines_v2_v1.1.md

## Document References
- Environment Setup: Section 2.1
- Exploration: Section 2.2
- Feature Engineering: Section 2.3
- Analysis: Section 2.4
- Communication: Section 2.5
- Session Management: Section 6.1

## Author
**Alberto Diaz Durana**
[GitHub](https://github.com/albertodiazdurana) | [LinkedIn](https://www.linkedin.com/in/albertodiazdurana/)

## Working Style
- Confirm understanding before proceeding
- Be concise in answers
- Do not generate files before providing description and receiving approval

## Command Execution
- Execute read-only commands (git status, ls, cat, grep, find, python -c for reading) without asking
- Show write commands (git commit, git push, rm, mv, pip install, file edits) for my approval first

## Code Output Standards
- Print statements show actual values (shapes, metrics, counts)
- Avoid generic confirmations: "Complete!", "Done!", "Success!"
- Let results speak: Show df.shape, not "Data loaded successfully!"

## Notebook Development Protocol

When generating notebook cells:
1. Generate ONE cell at a time; unless the first cell contains markdown only, then generate up to TWO cells
2. Wait for user approval OR execution output before generating next cell
3. Never generate multiple cells without explicit request
4. Adapt each cell based on actual output from previous cells
5. Number each cell with a comment (e.g., `# Cell 1`, `# Cell 2`) for easy reference in discussions

**Interaction pattern:**
- User describes goal → Claude proposes cell → User approves/runs → Claude sees output → Claude generates next cell
- "Continue" or "yes" = generate next cell
- "Generate all cells" = explicit batch override