# Quiz-Based Zone Unlock Demo

## 1. Start the MCP server (stdio - used by Cursor)

The MCP server runs automatically when Cursor loads. To run standalone:

```bash
python mcp_server.py
```

Expected output:
```
[INFO] AI Governance MCP Server starting... Loaded 3 zones, 21 patterns, 4 competency levels
[INFO] AI Governance MCP server ready (stdio)
```

## 2. Start the Quiz server (separate process)

```bash
python quiz_server.py
```

Expected output:
```
Quiz Server starting on http://localhost:3001
POST /quiz/submit with {"quiz_id":"v1","answers":["b","c","a","d","b"]}
```

## 3. Novice tries to access RED zone

In Cursor, run:
```
@mcp check_zoning_permission for file "src/core/payment.ts" with role "novice"
```

**Result:** `Access Denied - GREEN zone only. Red zone requires Champion.`

## 4. Submit quiz to unlock YELLOW zone

```bash
curl -X POST http://localhost:3001/quiz/submit \
  -H "Content-Type: application/json" \
  -d '{"quiz_id":"v1","answers":["b","c","a","d","b"]}'
```

**Result:** `{"passed": true, "message": "Passed! Unlocked YELLOW zone access", "unlocked_zone": "yellow"}`

## 5. Novice can now access YELLOW zone

Restart Cursor (or reload window) so the MCP server re-reads quiz_results.json. Then:

```
@mcp check_zoning_permission for file "src/api/users/controller.ts" with role "novice"
```

**Result:** `Allowed: true` (Yellow zone unlocked via quiz)

## Quiz answers (v1)

| Q | Question | Answer |
|---|----------|--------|
| 1 | What zone requires Champion approval? | b (Red) |
| 2 | Where should tribal knowledge live? | c (In the repo) |
| 3 | What does VTCO stand for? | a (Verb-Task-Constant-Outcome) |
| 4 | Novice in Yellow zone needs: | d (Quiz pass or mentor) |
| 5 | Entropy formula includes: | b (Bloat, rework, reverts, premature) |

Correct: `["b","c","a","d","b"]`
