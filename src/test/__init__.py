from src.segmenter import Segmenter

html = """
<body>
    <div>Hello, world!</div>
    <div>Hello, world!</div>
</body>
"""

splitter = Segmenter()
segments = splitter.segment_html(html)
print(segments)
