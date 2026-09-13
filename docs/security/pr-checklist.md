# Security checklist for PRs

- [ ] No secrets, tokens, or `.env` contents in the diff
- [ ] New network binds default to loopback or require explicit allow flag
- [ ] File/path inputs resolved and constrained under an allowed root
- [ ] Plugin or subprocess changes document trust assumptions
- [ ] Logs do not print API keys or full sensitive prompts
- [ ] Dependencies added only with justification; prefer stdlib
- [ ] Tests cover failure / refuse paths for security controls
