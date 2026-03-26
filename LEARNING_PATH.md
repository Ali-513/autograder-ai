# 📚 Learning Path: Understanding autograder-ai Codebase

This guide will help you understand the codebase in the **correct order**, building from simple foundations to complex orchestration.

---

## 🎯 **Phase 1: Foundation - Data Structures & Utilities** 
*Start here! These are the building blocks everything else uses.*

### 1.1 **States** (Data Structures)
**Location:** `workflows/states/`

**Files to read:**
1. `workflows/states/test_generation.py` ⭐ **START HERE**
   - Defines `TestCase` and `TestGenerationState` 
   - These are the data structures used throughout
   - Simple TypedDict definitions - easy to understand

2. `workflows/states/evaluation.py`
   - Defines `TestResult`, `TestExecutionState`, `EvaluationStatus`
   - More data structures for test execution

**Why first?** These define WHAT data flows through the system. Understanding the shape of data helps you understand everything else.

---

### 1.2 **Utilities** (Helper Functions)
**Location:** `utils/`

**Files to read:**
1. `utils/json_helpers.py`
   - `extract_json()` - extracts JSON from LLM responses
   - `sanitize_json()` - fixes common JSON issues
   - Simple string manipulation functions

2. `utils/code_execution.py`
   - `format_input_for_stdin()` - formats test inputs
   - `parse_agent_response()` - parses LLM agent responses
   - `sanitize_file_path()` - cleans file paths

**Why second?** These are simple helper functions used everywhere. No dependencies on other parts of the codebase.

---

## 🎯 **Phase 2: File I/O - Reading Files**
*How the system reads different file types*

### 2.1 **File Handlers** (Low-level file reading)
**Location:** `core/file_hanlders/`

**Files to read:**
1. `core/file_hanlders/base.py`
   - Abstract base class `BaseFileHandler`
   - Defines the interface all file handlers follow
   - Handles file validation

2. `core/file_hanlders/pdf.py`
   - `PDFFileHandler` - reads PDF files
   - Uses PyPDF2 library
   - Returns raw text

3. `core/file_hanlders/code.py`
   - `CodeFileHandler` - reads code files
   - Supports multiple languages (.py, .cpp, .c, .java, .js, .ts)
   - Returns raw code text

**Why third?** These are simple I/O operations. They're used by pre-processors but don't depend on anything complex.

---

## 🎯 **Phase 3: Data Processing - Extracting Meaning**
*How raw files become structured data*

### 3.1 **Pre-processors** (High-level data extraction)
**Location:** `core/pre_processors/`

**Files to read:**
1. `core/pre_processors/base.py`
   - Abstract base class `BasePreProcessor`
   - Very simple - just defines the interface

2. `core/pre_processors/assignment.py`
   - `AssignmentPreProcessor` - extracts questions from PDF
   - Uses `PDFFileHandler` to read PDF
   - Uses regex to find questions (Q1, Q2, etc.)
   - Returns dictionary: `{"q_1": "question text", ...}`

3. `core/pre_processors/submission.py`
   - `SubmissionPreProcessor` - processes student code
   - Uses `CodeFileHandler` to read files
   - Validates filenames match pattern `q_*`
   - Returns dictionary: `{"q_1.py": "code text", ...}`

**Why fourth?** These use file handlers but add business logic. They transform raw text into structured data.

---

## 🎯 **Phase 4: LLM Integration - Talking to AI**
*How the system communicates with language models*

### 4.1 **Clients** (LLM API wrappers)
**Location:** `clients/`

**Files to read:**
1. `clients/openai_client.py`
   - `OpenaiClient` - wrapper for OpenAI API
   - Gets API key from environment
   - Creates ChatOpenAI instance
   - Simple configuration class

2. `clients/ollama_client.py` (if exists)
   - Similar to OpenAI client but for local Ollama models

**Why fifth?** These are simple wrappers around LLM libraries. They're used by workflows but are straightforward.

---

## 🎯 **Phase 5: Workflow Components - The Brain**
*How the system orchestrates complex multi-step processes*

### 5.1 **Prompts** (What we tell the LLM)
**Location:** `workflows/prompts/`

**Files to read:**
1. `workflows/prompts/test_generation.py`
   - `TEST_GENERATION_PROMPT` - template for generating test cases
   - Just a string template with placeholders
   - Shows what instructions are given to LLM

2. `workflows/prompts/test_execution.py`
   - `TEST_EXECUTION_PROMPT` - template for executing tests
   - Instructions for LLM agent to run code

**Why sixth?** These are just text templates. Easy to understand, and you'll see them used in nodes.

---

### 5.2 **Nodes** (Individual workflow steps)
**Location:** `workflows/nodes/`

**Files to read:**
1. `workflows/nodes/test_generation.py`
   - `analyze_question_node()` - placeholder node
   - `analyze_code_node()` - placeholder node  
   - `generate_test_cases_node()` - **IMPORTANT** - calls LLM to generate tests
   - `validate_tests_node()` - validates test case structure
   - These are the actual steps in the test generation workflow

2. `workflows/nodes/test_execution.py`
   - `setup_code_file_node()` - creates temp file with code
   - `initialize_execution_node()` - sets up test execution
   - `execute_single_test_node()` - **IMPORTANT** - runs one test using LLM agent
   - `should_continue_testing()` - decides if more tests to run
   - `finalize_execution_node()` - cleans up and finalizes

**Why seventh?** These implement the actual logic. They use prompts, states, utilities, and clients. This is where the real work happens.

---

### 5.3 **Builders** (Workflow assembly)
**Location:** `workflows/builders/`

**Files to read:**
1. `workflows/builders/test_generation.py`
   - `TestGenerationBuilder` - builds the test generation workflow graph
   - Uses LangGraph to create a state machine
   - Connects nodes together: analyze → generate → validate
   - Shows the flow of the workflow

2. `workflows/builders/test_execution.py`
   - `TestExecutionBuilder` - builds the test execution workflow graph
   - More complex - has conditional logic (loops)
   - Shows how tests are executed one by one

**Why eighth?** These assemble nodes into complete workflows. You need to understand nodes first.

---

## 🎯 **Phase 6: Orchestration - The Big Picture**
*How everything comes together*

### 6.1 **Engine** (Main orchestrator)
**Location:** `engine.py` (root level)

**Files to read:**
1. `engine.py` ⭐ **READ LAST**
   - `EvaluationEngine` - the main class that orchestrates everything
   - Uses pre-processors to extract data
   - Uses workflow builders to create workflows
   - Runs workflows and collects results
   - Generates final report

**Why last?** This is the top-level orchestrator. It uses everything else. Once you understand all the pieces, this will make perfect sense.

---

## 🎯 **Phase 7: Entry Point - How It Starts**
**Location:** `main.py` (project root)

**Files to read:**
1. `main.py`
   - Command-line interface
   - Parses arguments
   - Creates `EvaluationEngine`
   - Runs evaluation
   - Prints report

**Why very last?** This is just the entry point. It's simple but uses the engine.

---

## 📋 **Quick Reference: Reading Order Summary**

```
1. workflows/states/test_generation.py          (Data structures)
2. workflows/states/evaluation.py               (More data structures)
3. utils/json_helpers.py                        (Helper functions)
4. utils/code_execution.py                       (More helpers)
5. core/file_hanlders/base.py                   (File handler base)
6. core/file_hanlders/pdf.py                    (PDF reading)
7. core/file_hanlders/code.py                   (Code reading)
8. core/pre_processors/base.py                  (Pre-processor base)
9. core/pre_processors/assignment.py            (Question extraction)
10. core/pre_processors/submission.py           (Code processing)
11. clients/openai_client.py                    (LLM client)
12. workflows/prompts/test_generation.py        (LLM prompts)
13. workflows/prompts/test_execution.py         (More prompts)
14. workflows/nodes/test_generation.py           (Workflow steps)
15. workflows/nodes/test_execution.py           (More steps)
16. workflows/builders/test_generation.py       (Workflow assembly)
17. workflows/builders/test_execution.py        (More assembly)
18. engine.py                                    (Main orchestrator)
19. main.py                                      (Entry point)
```

---

## 💡 **Tips for Learning**

1. **Read in order** - Each phase builds on the previous one
2. **Focus on one file at a time** - Don't rush
3. **Look at imports** - They show dependencies
4. **Run the code** - Understanding comes from seeing it work
5. **Add print statements** - See what data flows through
6. **Draw diagrams** - Visualize how components connect

---

## 🔍 **Key Concepts to Understand**

- **States**: Data structures that flow through workflows
- **File Handlers**: Low-level file reading
- **Pre-processors**: High-level data extraction
- **Nodes**: Individual steps in a workflow
- **Builders**: Assemble nodes into workflows
- **Workflows**: LangGraph state machines
- **Engine**: Orchestrates everything

---

## ❓ **Questions to Ask While Reading**

- What data does this component receive?
- What data does it produce?
- What does it depend on?
- How is it used by other components?
- What problem does it solve?

---

Happy learning! 🚀

