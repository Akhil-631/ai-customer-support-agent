from pathlib import Path
import webbrowser

from graph import graph


# Generate Mermaid representation from the actual LangGraph
mermaid_code = graph.get_graph().draw_mermaid()

# Remove Mermaid frontmatter so the diagram can be embedded directly in HTML
if "graph TD;" in mermaid_code:
    mermaid_code = mermaid_code[mermaid_code.index("graph TD;"):]


# Create a standalone HTML visualization
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Customer Support Agent - LangGraph</title>

    <script type="module">
        import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

        mermaid.initialize({{
            startOnLoad: true,
            theme: "default",
            flowchart: {{
                curve: "linear",
                useMaxWidth: true,
                htmlLabels: true
            }}
        }});
    </script>

    <style>
        body {{
            margin: 0;
            padding: 30px;
            background: #f7f7f8;
            font-family: Arial, sans-serif;
        }}

        h1 {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .graph-container {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            overflow: auto;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        }}
    </style>
</head>

<body>
    <h1>AI Customer Support Agent — LangGraph</h1>

    <div class="graph-container">
        <pre class="mermaid">
{mermaid_code}
        </pre>
    </div>
</body>
</html>
"""


# Save the visualization
output_file = Path("langgraph_visualization.html")
output_file.write_text(html, encoding="utf-8")


# Open it automatically in the default browser
webbrowser.open(output_file.resolve().as_uri())


print(f"LangGraph visualization created:")
print(output_file.resolve())