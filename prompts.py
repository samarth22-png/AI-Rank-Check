def get_prompt(query):
    return f"""
You are an expert product recommendation engine.

Query: "{query}"

List the TOP 5 products a customer should choose.

Rules:
- Be specific (brand names)
- Rank from best to worst
- Give 1-line reason

Output:
1. Product - Reason
2. Product - Reason
"""