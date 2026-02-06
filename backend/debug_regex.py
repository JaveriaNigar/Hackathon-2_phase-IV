import re

# Test the regex patterns
message = "I've finished task Test Task 1769363712"
message_lower = message.lower()

print(f"Testing message: '{message}'")
print(f"Lowercase: '{message_lower}'")

# Test the first pattern
match1 = re.search(r'(?:complete|finish|done).*?(?:task|:|called|named)\s+(.+)', message_lower, re.IGNORECASE)
print(f"Pattern 1 (complete|finish|done .* task): {match1.group(1) if match1 else 'No match'}")

# Test the second pattern
match2 = re.search(r'(?:complete|finish|done)\s+(.+?)\s*(?:task)', message_lower, re.IGNORECASE)
print(f"Pattern 2 (complete|finish|done X task): {match2.group(1) if match2 else 'No match'}")

# Test the third pattern
match3 = re.search(r"(?:i've|i have|have)\s+(?:finished|completed|done)\s+(?:task\s+)?(.+)", message_lower, re.IGNORECASE)
print(f"Pattern 3 (i've|have finished [task] X): {match3.group(1) if match3 else 'No match'}")

# Test the delete patterns
delete_message = "Delete task Test Task 1769363712"
delete_message_lower = delete_message.lower()

print(f"\nTesting delete message: '{delete_message}'")
print(f"Lowercase: '{delete_message_lower}'")

# Test the first delete pattern
del_match1 = re.search(r'(?:delete|remove).*?(?:task|:|called|named)\s+(.+)', delete_message_lower, re.IGNORECASE)
print(f"Delete Pattern 1 (delete|remove .* task): {del_match1.group(1) if del_match1 else 'No match'}")

# Test the second delete pattern
del_match2 = re.search(r'(?:delete|remove)\s+(?:task\s+)?(.+)', delete_message_lower, re.IGNORECASE)
print(f"Delete Pattern 2 (delete|remove [task] X): {del_match2.group(1) if del_match2 else 'No match'}")