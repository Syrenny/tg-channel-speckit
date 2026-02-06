<!--
Sync Impact Report
==================
Version change: 0.0.0 → 1.0.0
Bump rationale: Initial constitution creation (MAJOR - new governance document)

Modified principles: N/A (initial creation)
Added sections:
  - Core Principles (3 principles: TDD, CLI-First, Simplicity)
  - Technology Constraints
  - Development Workflow
  - Governance

Removed sections: N/A (initial creation)

Templates requiring updates:
  ✅ plan-template.md - Constitution Check section is generic, compatible
  ✅ spec-template.md - No constitution-specific references, compatible
  ✅ tasks-template.md - Test-first guidance aligns with TDD principle
  ✅ checklist-template.md - Generic template, compatible

Follow-up TODOs: None
-->

# Telegram Channel Analyser Constitution

## Core Principles

### I. Test-Driven Development (NON-NEGOTIABLE)

All feature implementation MUST follow the TDD cycle:

1. **Write tests first** - Tests define the expected behavior before any implementation
2. **Verify tests fail** - Confirm the test correctly identifies missing functionality
3. **Implement minimally** - Write only enough code to make the test pass
4. **Refactor** - Clean up while keeping tests green

**Rationale**: TDD ensures code correctness, prevents regressions, and produces
well-designed, testable modules. Skipping TDD leads to untested edge cases and
brittle implementations.

**Enforcement**: PRs without corresponding tests for new functionality MUST be
rejected. Test coverage MUST be reviewed before merge.

### II. CLI-First Interface

All functionality MUST be accessible via command-line interface:

- **Text protocol**: stdin/arguments as input, stdout for results, stderr for errors
- **Composability**: Tools MUST support piping and standard Unix conventions
- **Formats**: Support both human-readable and machine-parseable (JSON) output
- **No hidden state**: Operations MUST be reproducible from command-line invocation

**Rationale**: CLI interfaces enable automation, scripting, and integration with
other tools. They ensure functionality is testable and debuggable without
requiring complex UI setup.

### III. Simplicity (YAGNI)

Every addition MUST justify its complexity:

- **Start minimal**: Implement the simplest solution that works
- **No speculative features**: Build only what is needed NOW
- **Reject premature abstraction**: Three similar lines are better than one
  abstraction used once
- **Delete freely**: Remove unused code, comments, and features

**Rationale**: Complexity compounds. Each unnecessary abstraction adds cognitive
load, maintenance burden, and potential bugs. Simple code is easier to
understand, test, and modify.

**Enforcement**: Code reviews MUST challenge complexity. Additions MUST
demonstrate clear, immediate value.

## Technology Constraints

**Shell**: Bash scripts for orchestration and CLI tools
**Prompts**: Markdown files (.md) for LLM prompts and documentation
**Dependencies**: Minimize external dependencies; prefer standard Unix tools
**Compatibility**: Scripts MUST work on Linux; macOS compatibility is optional

**Version Control**: Git with conventional commits
**CI/CD**: Scripts MUST be executable in CI environments without interactive input

## Development Workflow

1. **Specification**: Define requirements in spec.md before implementation
2. **Planning**: Create plan.md with technical approach and structure
3. **Task Breakdown**: Generate tasks.md with ordered, testable tasks
4. **Implementation**: Follow TDD cycle for each task
5. **Review**: Verify constitution compliance before merge

**Branching**: Feature branches from main; squash merge after review
**Commits**: Atomic commits with clear messages describing the "why"

## Governance

This constitution supersedes all other development practices in this project.

**Amendments** require:
1. Written proposal documenting the change and rationale
2. Review of impact on existing code and workflows
3. Update to this document with version increment
4. Migration plan if breaking existing patterns

**Versioning**: MAJOR.MINOR.PATCH
- MAJOR: Principle removal or incompatible redefinition
- MINOR: New principle or section added
- PATCH: Clarifications and non-semantic refinements

**Compliance**: All PRs and code reviews MUST verify adherence to these
principles. Violations MUST be addressed before merge.

**Version**: 1.0.0 | **Ratified**: 2026-02-06 | **Last Amended**: 2026-02-06
