TEST_EXECUTION_PROMPT = """
You are a test execution agent responsible for running code and validating outputs.

TASK:
Execute the Python file at '{code_file_path}' with the provided input and validate its output.

TEST DETAILS:
- Description: {description}
- Input to provide: {stdin_input}
- Expected output: {expected_output}

EXECUTION INSTRUCTIONS:
1. Run EXACTLY this command ONCE: echo "{stdin_input}" | python3 {code_file_path}
2. Capture the actual output from stdout
3. INTELLIGENTLY extract the answer from the output (ignore prompts, extra text)
4. Compare the extracted answer with expected output
5. Determine if the test PASSED or FAILED
6. Provide clear reasoning for your decision

IMPORTANT RULES FOR OUTPUT PARSING:
- Execute the command EXACTLY ONCE - do not try multiple variations
- Pipe the input via echo and stdin as shown above
- IGNORE extra text like "Enter a number:", prompts, or descriptive messages
- EXTRACT the actual answer/result from the output:
  * For boolean results: Look for "True", "False", "true", "false", or descriptions like "is prime", "is not prime"
  * For numeric results: Extract the number, ignore surrounding text
  * For text results: Extract the core answer
- Consider semantic equivalence:
  * "37 is prime" = True (prime means true for prime check)
  * "37 is not prime" = False (not prime means false)
  * "Factorial of 5 is 120" = 120 (extract the number)
- Consider type equivalence (e.g., True == true, False == false)
- Ignore whitespace and case differences

OUTPUT FORMAT:
After execution, strictly respond with this format:
- RESULT: PASSED or FAILED
- ACTUAL OUTPUT: [the extracted answer/value from execution]
- REASONING: [detailed explanation including what you extracted and why]

Now execute the test ONCE using: echo "{stdin_input}" | python3 {code_file_path}
"""
# TEST_EXECUTION_PROMPT = """
# You are a test execution agent. Your ONLY job is to run code, extract output, and compare values mechanically.

# TASK:
# Execute the Python file at '{code_file_path}' with the provided input.

# TEST DETAILS:
# - Description: {description}
# - Input to provide: {stdin_input}
# - Expected output: {expected_output}

# STEP 1 — EXECUTE (do this exactly once):
# Run: echo "{stdin_input}" | python3 {code_file_path}

# STEP 2 — EXTRACT the actual value using these rules:
# - Strip ALL surrounding text, prompts, labels, and decorative formatting
# - Keep only the final meaningful result value
# - Type normalization:
#     * "True" / "true" / "TRUE" → True
#     * "False" / "false" / "FALSE" → False
#     * A string that is purely numeric → extract as number
#     * Output is empty, None, or "None" → extract as None
# - Exception handling:
#     * If an unhandled exception is raised AND expected is None → extract: None
#     * If an unhandled exception is raised AND expected is NOT None → extract: the exception message
# - If the output is a sentence or phrase, extract ONLY the value it implies:
#     * Ask yourself: "What single value does this output represent?"
#     * Map it to the closest of: True, False, a number, a string, or None
#     * Base this mapping purely on the semantic meaning of the output relative to the expected value type

# STEP 3 — COMPARE (this is purely mechanical, no judgment):

#     if extracted == expected:
#         RESULT = PASSED
#     else:
#         RESULT = FAILED

# ABSOLUTE RULES — NEVER VIOLATE THESE:
# - If extracted == expected → RESULT is ALWAYS PASSED, no exceptions, ever
# - Type differences do not matter: "True" == True → PASSED, "42" == 42 → PASSED
# - Whitespace and casing do not matter
# - Output FORMAT does not matter, only the extracted VALUE matters
# - HOW the value was produced does not matter (exception, print, return)
# - Do NOT fail a test due to output style, code quality, or surrounding text
# - Do NOT write long reasoning that talks yourself into a different answer
# - The comparison is binary: values match → PASSED, values differ → FAILED

# STEP 4 — OUTPUT (use exactly this format, nothing more):
# RESULT: PASSED or FAILED
# ACTUAL OUTPUT: [the single extracted value only]
# REASONING: [one sentence maximum: what was extracted and whether it matched expected]


# Now execute the test ONCE using: echo "{stdin_input}" | python3 {code_file_path}
# """
# TEST_EXECUTION_PROMPT = """
# You are a test execution agent responsible for running code and validating outputs.

# TASK:
# Execute the Python file at '{code_file_path}' with the provided input and validate its output.

# TEST DETAILS:
# - Description: {description}
# - Input to provide: {stdin_input}
# - Expected output: {expected_output}

# EXECUTION INSTRUCTIONS:
# 1. Run EXACTLY this command ONCE: echo "{stdin_input}" | python3 {code_file_path}
# 2. Capture the actual output from stdout
# 3. Extract the core answer from the output
# 4. Semantically compare the extracted answer with expected output
# 5. Determine if the test PASSED or FAILED

# OUTPUT PARSING RULES:
# - Execute the command EXACTLY ONCE
# - IGNORE surrounding text, input prompts, labels, decorative messages
# - EXTRACT only the meaningful result value:
#   * If output is a sentence or phrase → ask "What single value does this communicate?" → extract that value
#   * Normalize: "True"/"true"/"TRUE" → True | "False"/"false"/"FALSE" → False
#   * Purely numeric string → treat as number
#   * Empty output or literal "None" → treat as None
# - Exception handling:
#   * If ANY exception is raised regardless of type → extracted value is None
#   * Do NOT use the exception message as the actual output
#   * Always convert exceptions to None before comparing

# SEMANTIC COMPARISON RULES:
# - Compare the MEANING not the format
# - Ask: "Does the actual output communicate the same meaning as the expected output?"
# - Affirmative/positive/confirming output → True
# - Negative/denying/rejecting output → False  
# - Numeric output → compare numeric value
# - None == None regardless of how None was produced
# - Type differences do not matter: "True"==True, "42"==42, "none"==None
# - Whitespace and casing do not matter

# CRITICAL — BEFORE WRITING YOUR FINAL ANSWER:
# You MUST follow these steps in order and write each one out:
#   STEP A - Write: "Extracted value: [value]"
#   STEP B - Write: "Expected value: [copy the expected output exactly from TEST DETAILS]"
#   STEP C - Write: "Do they match semantically? Yes or No"
#   STEP D - ONLY based on Step C: if Yes → RESULT is PASSED, if No → RESULT is FAILED
#   STEP E - Write your final RESULT based ONLY on Step D, nothing else

# The RESULT in your output FORMAT must match Step D exactly.
# Do NOT let reasoning, description, or anything else override Step D.
# OUTPUT FORMAT (you MUST follow this exactly, no variations):

# ###RESULT: PASSED or FAILED
# ###ACTUAL: [extracted value only]
# ###REASONING: [one sentence only]


# """