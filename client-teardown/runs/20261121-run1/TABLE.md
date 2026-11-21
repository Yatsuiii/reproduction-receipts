Reference clients (arming gate: every cell must match its expected value in every trial)

| reference | clean | eof-ignore | term-ignore | wrapped |
|---|---|---|---|---|
| `ref-none` | clean 10/10 (expected clean) | **residue 10/10** (expected residue) | **residue 10/10** (expected residue) | **residue 10/10** (expected residue) |
| `ref-spec-group` | clean 10/10 (expected clean) | clean 10/10 (expected clean) | clean 10/10 (expected clean) | clean 10/10 (expected clean) |
| `ref-spec-pid` | clean 10/10 (expected clean) | clean 10/10 (expected clean) | clean 10/10 (expected clean) | **residue 10/10** (expected residue) |

Targets

| target | clean | eof-ignore | term-ignore | wrapped |
|---|---|---|---|---|
| `cli-gemini` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `cli-kilo` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `cli-opencode` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `cli-qwen` | clean 10/10 | clean 10/10 | clean 10/10 | dead 10 of 10 |
| `go-go-sdk` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `go-mcp-go` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `js-ai-sdk` | clean 10/10 | clean 10/10 | **residue 10/10** | **residue 10/10** |
| `js-ai-sdk@patched` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `js-langchain` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `js-mastra` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `js-mcp-use` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `js-openai-agents` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `js-ts-client-v2` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `py-adk` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-agno` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-autogen` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-camel` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-crewai-adapter` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-crewai-native` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-fastmcp` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-langchain-session` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-langchain` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-llamaindex` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-mcp-sdk` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-mcp-use` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-openai-agents` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-pydantic-ai-agent` | **residue 10/10** | **residue 10/10** | **residue 10/10** | **residue 10/10** |
| `py-pydantic-ai-agent@patched` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-pydantic-ai-config` | **residue 10/10** | **residue 10/10** | **residue 10/10** | **residue 10/10** |
| `py-pydantic-ai-config@patched` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-pydantic-ai-nokeepalive` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-pydantic-ai` | **residue 10/10** | **residue 10/10** | **residue 10/10** | **residue 10/10** |
| `py-pydantic-ai@patched` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-semantic-kernel` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `py-smolagents` | clean 10/10 | clean 10/10 | clean 10/10 | clean 10/10 |
| `rs-goose-spawn` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `rs-rmcp` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `ts-sdk-1.12.0` | clean 10/10 | clean 10/10 | **residue 10/10** | **residue 10/10** |
| `ts-sdk-1.25.2` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `ts-sdk-1.29.0` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `ts-sdk-1.32.1` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
| `ts-sdk-1.32.2` | clean 10/10 | clean 10/10 | clean 10/10 | **residue 10/10** |
