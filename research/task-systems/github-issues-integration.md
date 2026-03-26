# GitHub Issues Integration — Draft Research

**Status:** Draft  
**Date:** 2026-03-26  
**Author:** CTO

## Overview

Replace custom context‑discipline task system with GitHub Issues for visible, trackable task management. Issues become the single source of truth for work items, with OpenClaw agents reading, updating, and closing them via GitHub API.

## Why GitHub Issues

1. **Visibility:** Board members can see all tasks in one place
2. **Familiarity:** Standard workflow (labels, assignees, milestones)
3. **Audit trail:** Full history in issue comments
4. **Integration:** Webhooks for real‑time updates
5. **Cost:** Free (vs building/maintaining custom system)
6. **Mobile access:** GitHub mobile app

## Proposed Workflow

```
Discord mention → Issue created → Agent assigned → Work done → Issue closed → Summary posted
```

### 1. Issue Creation
- **From Discord:** `@CTO create issue: "Research Templ.io integration"` → bot creates issue
- **Manual:** Board members create issues directly
- **Automated:** Cron jobs create recurring issues (e.g., "Morning Office Brief")

### 2. Issue Assignment
- Labels: `ceo`, `cto`, `research`, `coding`, `urgent`
- Assignees: GitHub users mapped to agents
- Milestones: `Sprint 1`, `Q2 2026`, `Backlog`

### 3. Agent Processing
- Agent polls assigned issues (or receives webhook)
- Reads issue description + comments
- Executes task (research, coding, analysis)
- Updates issue with progress/completion

### 4. Issue Closure
- Agent posts final result as comment
- Closes issue with appropriate label (`done`, `wontfix`, `duplicate`)
- Optional: cross‑post summary to Discord

## Technical Implementation

### Authentication
```bash
# Personal access token (classic)
GITHUB_TOKEN=ghp_...

# Store in OpenClaw config
openclaw config set env.GITHUB_TOKEN $GITHUB_TOKEN
```

### API Access
- **REST API:** `https://api.github.com/repos/{owner}/{repo}/issues`
- **GraphQL:** More efficient for complex queries
- **Rate limits:** 5,000 requests/hour (authenticated)

### Webhooks
- **GitHub → OpenClaw:** Issue created, assigned, commented, closed
- **OpenClaw endpoint:** `https://theoffice.tail285214.ts.net/github/webhook`
- **Payload:** JSON with issue data, action type

### Agent Integration Points

1. **Issue Reader Skill**  
   - Fetches assigned issues
   - Parses description, labels, comments
   - Converts to agent task format

2. **Issue Updater Skill**  
   - Posts progress updates as comments
   - Adds/removes labels
   - Closes issues with result summary

3. **Issue Creator Skill**  
   - Creates issues from Discord messages
   - Sets labels, assignees, milestones
   - Links to Discord message ID

## Repository Structure

**Option A: Single repo**
```
theoffice_/issues/
├── .github/workflows/
├── docs/              # Office documentation
├── scripts/           # Shared automation scripts
└── (issues track all work)
```

**Option B: Multiple repos**
- `theoffice_/tasks` — Issue tracker only
- `theoffice_/docs` — Documentation
- `theoffice_/scripts` — Automation code

**Recommendation:** Start with single repo (`theoffice_`) for simplicity.

## Sample Issue Templates

### Research Issue
```markdown
## Research Request

**Topic:** [Brief description]
**Purpose:** [Why this research matters]
**Deliverables:**
- [ ] Summary document
- [ ] Technical assessment
- [ ] Recommendations

**Time estimate:** [e.g., 2 hours]
**Priority:** High/Medium/Low
```

### Coding Issue
```markdown
## Development Task

**Feature/Bug:** [Description]
**Acceptance criteria:**
- [ ] Code written
- [ ] Tests pass
- [ ] Documentation updated

**Files affected:**
- `path/to/file.py`
- `path/to/test.py`

**Branch:** `feature/short-description`
```

### Analysis Issue
```markdown
## Data Analysis

**Dataset:** [Description/location]
**Questions:**
1. [Question 1]
2. [Question 2]

**Expected output:**
- [ ] Summary statistics
- [ ] Visualizations
- [ ] Insights report
```

## Agent Assignment Rules

| Issue Label | Default Assignee | Timeout |
|---|---|---|
| `research` | CEO | 24h |
| `coding` | CTO | 12h |
| `data` | CAO (future) | 24h |
| `urgent` | CEO (escalation) | 4h |
| `review` | CTO | 6h |

**Fallback:** Unassigned after timeout → reassign to CEO.

## Webhook Payload Example

```json
{
  "action": "assigned",
  "issue": {
    "number": 42,
    "title": "Research Templ.io integration",
    "body": "Templ is a WordPress hosting company...",
    "labels": [{"name": "research"}, {"name": "cto"}],
    "assignee": {"login": "cto-bot"}
  },
  "repository": {"full_name": "theoffice_/theoffice"},
  "sender": {"login": "bouveng"}
}
```

## OpenClaw Configuration

```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_...",
    "GITHUB_REPO": "theoffice_/theoffice"
  },
  "skills": {
    "github-issues": {
      "enabled": true,
      "pollInterval": 300,
      "webhookSecret": "..."
    }
  }
}
```

## Skills Needed

1. **`github-issues` skill** (new)
   - List, create, update, close issues
   - Handle webhooks
   - Map GitHub users ←→ OpenClaw agents

2. **`github-auth` skill** (existing?)
   - OAuth flow for Board members
   - Token management

3. **`issue-to-task` compiler**
   - Convert issue → agent task prompt
   - Include relevant context (previous comments, linked issues)

## Challenges

1. **Authentication:** Need GitHub token with repo access
2. **Agent↔GitHub user mapping:** Who "owns" each issue?
3. **Context size:** Issue history could be long → need summarization
4. **Real‑time sync:** Webhook vs polling trade‑offs
5. **Error handling:** API rate limits, network failures

## Alternatives Considered

### Linear
- Better UI, native integrations
- Cost: $10/user/month

### Jira
- Enterprise features
- Overkill for small team

### Notion
- Flexible database
- API less mature

### Custom built (abandoned)
- Full control
- High maintenance cost

## Next Steps

1. **Create test repository** (`theoffice_/tasks`)
2. **Generate GitHub token** with `repo` scope
3. **Build MVP skill:** `github-issues` (list/create issues)
4. **Test workflow:** Discord → Issue → Agent → Close
5. **Add webhooks** for real‑time updates
6. **Document workflow** for Board members

## Success Metrics

- Time from issue creation to assignment < 15min
- Issue closure rate > 80%
- Board satisfaction with visibility
- Reduced context‑rot incidents

## References

- [GitHub REST API docs](https://docs.github.com/en/rest/issues/issues)
- [GitHub Webhooks](https://docs.github.com/en/webhooks)
- [OpenClaw skills system](https://docs.openclaw.ai/skills)

---
*Draft for discussion with CEO and Board.*