import re

def clean_fallback_title(title):
    if not title: return ""
    prev_title = ""
    while title != prev_title:
        prev_title = title
        title = re.sub(r'^(?:to|my|a|the|task|tasks|called|named|as|is|with|label)\s+', '', title, flags=re.IGNORECASE).strip()
    return title.strip('"').strip("'").strip().strip('"').strip("'")

def test_regex_v2(message):
    message_lower = message.lower().strip()
    print(f"Testing: '{message}'")

    # 1. Add (unchanged)
    if "add" in message_lower or "create" in message_lower:
        match = re.search(r'(?:add|create).*?(?:task|:|called|named)\s+(.+)', message_lower, re.IGNORECASE)
        # ... logic ...
        print("  Matches ADD")

    # 2. Update (MOVED UP)
    elif re.search(r'\b(?:upd|edi|cha|ren)', message_lower):
        match = re.search(r'(?:upd|edi|cha|ren).*?(?:task|:|called|named)?\s+(.+?)\s+(?:to|as)\s+(.+)', message_lower, re.IGNORECASE)
        if match:
             print(f"  Matches UPDATE. Old: {match.group(1)}, New: {match.group(2)}")
        else:
             print("  Matches UPDATE (Parse failed)")

    # 3. Delete
    elif re.search(r'\b(?:del|rem)', message_lower):
        print("  Matches DELETE")

    # 4. Complete
    elif re.search(r'\b(?:comp|fin|don|mark.*?c|mark.*?d|as\s+done|mark.*?done)', message_lower):
         match = re.search(r'(?:comp|fin|don|mark.*?c|mark.*?d|as\s+done|mark.*?done).*?(?:task|:|called|named)?\s+(.+?)(?:\s+as\s+done|\s+is\s+done|\s+done)?$', message_lower, re.IGNORECASE)
         print(f"  Matches COMPLETE. Title: {match.group(1) if match else 'None'}")

    else:
        print("  No match")

test_regex_v2("Edit task market to supermarket")
test_regex_v2("Change task market to supermarket")
test_regex_v2("Edit done to not done") 
