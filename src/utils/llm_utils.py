import re
def extract_html(text):
  """
  Extracts HTML code from a string.

  Args:
    text: The input string containing HTML code.

  Returns:
    The extracted HTML code as a string, or None if no HTML code is found.
  """
  match = re.search(r"<!DOCTYPE html>(.*?)</html>", text, re.DOTALL)
  if match:
    return match.group(0)
  else:
    return None