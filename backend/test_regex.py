import re

patterns = {
    "add_task": [
        r"(?:add|create|remember|make|put in|add in)\s+(?:a\s+|an\s+|the\s+)?(.+?)(?:\s+to\s+my\s+tasks?|\s+please|\s+now|[\.!\?]|$)",
        r"(?:i\s+need\s+to|let's|can\s+i|please)\s+(?:add|create|remember|make)\s+(.+?)(?:\s+please|\s+now|[\.!\?]|$)",
        r"^add\s+(.+)$"
    ],
    "list_tasks": [
        r"(?:show|list|display|get|tell me|what are|what's|give me)\s+(?:me\s+)?(?:all\s+|my\s+)?(?:pending\s+|completed\s+|done\s+)?(?:tasks?|to-dos?|todos?|things\s+to\s+do)(?:\s+please|\s+now|[\.!\?]|$)",
        r"(?:what\s+(?:have\s+i\s+|do\s+i\s+)?)?(?:pending|left|remaining|unfinished|incomplete)\s+(?:tasks?|to-dos?|todos?)(?:\s+please|\s+now|[\.!\?]|$)",
        r"(?:what\s+(?:have\s+i\s+|do\s+i\s+)?)?(?:completed|done|finished)\s+(?:tasks?|to-dos?|todos?)(?:\s+please|\s+now|[\.!\?]|$)",
        r"^(?:list|tasks|todos|show tasks|my tasks|give me my tasks|i want to see my tasks)(?:[\.!\?]|$)"
    ],
    "update_task": [
         r"(?:change|update|modify|rename|edit)\s+(?:the\s+)?(.+?)\s+(?:to|as|into)\s+(.+?)(?:[\.!\?]|$)",
         r"^edit\s+(.+?)\s+to\s+(.+)$"
    ]
}

test_cases = [
    ("list", "list_tasks"),
    ("give me my tasks", "list_tasks"),
    ("list my tasks!", "list_tasks"),
    ("add buy milk", "add_task"),
    ("add buy milk!", "add_task"),
    ("edit buy milk to buy eggs", "update_task"),
    ("edit task 1 to task 2", "update_task")
]

print("Testing updated human-like regex patterns...")
for text, expected in test_cases:
    text_lower = text.lower().strip()
    matched = False
    
    # Check specific expected intent first
    for p in patterns[expected]:
        if re.search(p, text_lower):
            print(f"[PASS] '{text}' -> {expected}")
            matched = True
            break
            
    if not matched:
        print(f"[FAIL] '{text}' expected {expected}")
