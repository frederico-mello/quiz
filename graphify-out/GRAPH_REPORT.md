# Graph Report - .  (2026-07-14)

## Corpus Check
- 43 files · ~131,485 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 101 nodes · 154 edges · 17 communities (13 shown, 4 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 13 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Quiz App Core|Quiz App Core]]
- [[_COMMUNITY_Avatar GIF Generation|Avatar GIF Generation]]
- [[_COMMUNITY_OpenSpec Commands & Skills|OpenSpec Commands & Skills]]
- [[_COMMUNITY_OpenSpec Prompts & Skills|OpenSpec Prompts & Skills]]
- [[_COMMUNITY_CLI Bootstrap Script|CLI Bootstrap Script]]
- [[_COMMUNITY_Python Dependencies|Python Dependencies]]
- [[_COMMUNITY_Content Filter|Content Filter]]
- [[_COMMUNITY_LLM Service|LLM Service]]
- [[_COMMUNITY_Codacy Code Quality Tools|Codacy Code Quality Tools]]
- [[_COMMUNITY_Codacy CLI Configuration|Codacy CLI Configuration]]
- [[_COMMUNITY_OpenCode Plugin Package|OpenCode Plugin Package]]
- [[_COMMUNITY_Dart Analysis Config|Dart Analysis Config]]
- [[_COMMUNITY_Trivy Security Scanner|Trivy Security Scanner]]
- [[_COMMUNITY_Graphify Agent Config|Graphify Agent Config]]

## God Nodes (most connected - your core abstractions)
1. `openspec CLI` - 11 edges
2. `main()` - 9 edges
3. `_frames_to_gif_bytes()` - 7 edges
4. `requirements.txt (Python deps)` - 7 edges
5. `check_text()` - 6 edges
6. `evaluate_answer()` - 6 edges
7. `_draw_scientist_frame()` - 5 edges
8. `generate_talking_gif_bytes()` - 5 edges
9. `generate_idle_gif_bytes()` - 5 edges
10. `get_talking_gif_base64()` - 5 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `get_idle_gif_base64()`  [EXTRACTED]
  app.py → src/avatar.py
- `main()` --calls--> `check_text()`  [EXTRACTED]
  app.py → src/content_filter.py
- `main()` --calls--> `evaluate_answer()`  [EXTRACTED]
  app.py → src/llm_service.py
- `spec-driven schema` --conceptually_related_to--> `openspec CLI`  [INFERRED]
  openspec/config.yaml → .opencode/commands/opsx-apply.md
- `main()` --calls--> `get_talking_gif_base64()`  [EXTRACTED]
  app.py → src/avatar.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **OpenSpec change lifecycle (propose -> apply -> archive, explore parallel)** — _github_skills_openspec_propose_skill, _github_skills_openspec_apply_change_skill, _github_skills_openspec_archive_change_skill, _github_skills_openspec_explore_skill, concept_openspec_cli [EXTRACTED 1.00]
- **Codacy analysis configuration suite (CLI + languages + per-tool)** — _codacy_cli_config, _codacy_tools_configs_languages_config, _codacy_tools_configs_lizard, _codacy_tools_configs_semgrep, _codacy_tools_configs_trivy, _codacy_tools_configs_analysis_options, concept_codacy_cli [INFERRED 0.95]
- **OpenSpec change lifecycle (propose -> explore -> apply -> sync -> archive)** — opencode_commands_opsx_propose, opencode_commands_opsx_explore, opencode_commands_opsx_apply, opencode_commands_opsx_sync, opencode_commands_opsx_archive [INFERRED 0.95]
- **OpenSpec skills orchestrating the openspec CLI** — opencode_skills_openspec_propose_skill, opencode_skills_openspec_apply_change_skill, opencode_skills_openspec_archive_change_skill, opencode_skills_openspec_sync_specs_skill, opencode_skills_openspec_explore_skill, openspec_cli [INFERRED 0.95]

## Communities (17 total, 4 thin omitted)

### Community 0 - "Quiz App Core"
Cohesion: 0.23
Nodes (9): main(), edge-tts (Python lib), get_talking_gif_base64(), Retorna GIF falante em base64.      Se duration_seconds for fornecido, gera um G, get_warning_level(), get_question(), load_questions(), generate_speech() (+1 more)

### Community 1 - "Avatar GIF Generation"
Cohesion: 0.22
Nodes (12): Image, _draw_scientist_frame(), _frames_to_gif_bytes(), generate_idle_gif_bytes(), generate_talking_gif_bytes(), get_idle_gif_base64(), Converte uma lista de frames PIL em bytes GIF., Gera GIF animado do professor falando.      Se audio_duration_seconds > 0, o GIF (+4 more)

### Community 2 - "OpenSpec Commands & Skills"
Cohesion: 0.33
Nodes (13): /opsx-apply command, /opsx-archive command, /opsx-explore command, /opsx-propose command, /opsx-sync command, openspec-apply-change skill, openspec-archive-change skill, openspec-explore skill (+5 more)

### Community 3 - "OpenSpec Prompts & Skills"
Cohesion: 0.25
Nodes (11): opsx-apply prompt (implement tasks), opsx-archive prompt (archive a change), opsx-explore prompt (thinking/ideation mode), opsx-propose prompt (create change + artifacts), openspec-apply-change skill (implement tasks), openspec-archive-change skill (finalize & archive), openspec-explore skill (thinking partner), openspec-propose skill (create change + artifacts) (+3 more)

### Community 4 - "CLI Bootstrap Script"
Cohesion: 0.39
Nodes (6): cli.sh script, download(), download_cli(), download_file(), get_latest_version(), handle_rate_limit()

### Community 5 - "Python Dependencies"
Cohesion: 0.38
Nodes (7): langchain (Python lib), langchain-openai (Python lib), mutagen (Python lib), openai (Python lib), python-dotenv (Python lib), requirements.txt (Python deps), streamlit (Python lib)

### Community 6 - "Content Filter"
Cohesion: 0.57
Nodes (6): check_keywords(), check_patterns(), check_text(), check_text_llm(), check_text_local(), normalize_leet()

### Community 7 - "LLM Service"
Cohesion: 0.70
Nodes (4): build_prompt(), clean_text_for_tts(), evaluate_answer(), get_llm()

### Community 8 - "Codacy Code Quality Tools"
Cohesion: 0.50
Nodes (4): lizard tool (complexity analyzer), opengrep tool (semgrep fork, multi-language SAST), Codacy Lizard Config (complexity thresholds), Codacy Semgrep Config (security rule patterns)

### Community 9 - "Codacy CLI Configuration"
Cohesion: 0.67
Nodes (3): Codacy CLI Config (.codacy/cli-config.yaml), Codacy Languages Config (tool-language registry), Codacy CLI (local analysis mode)

## Knowledge Gaps
- **15 isolated node(s):** `@opencode-ai/plugin`, `Codacy CLI Config (.codacy/cli-config.yaml)`, `Codacy Analysis Options (Dart analyzer + linter rules)`, `Codacy Languages Config (tool-language registry)`, `Codacy Trivy Config (vuln + secret scanner)` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `requirements.txt (Python deps)` connect `Python Dependencies` to `Quiz App Core`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Why does `streamlit (Python lib)` connect `Python Dependencies` to `Quiz App Core`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **What connects `@opencode-ai/plugin`, `Desenha um frame do avatar professor.`, `Converte uma lista de frames PIL em bytes GIF.` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._