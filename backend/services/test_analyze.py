from analysis import analyze_legal_document

sample_text = """
The employee shall pay a penalty of $5000
if the agreement is terminated before 12 months.
"""

result = analyze_legal_document(sample_text)

print(result)