from pathlib import Path
import sys

sys.path.extend('/pyswim')

from pyswim import fixm_schema

xml = Path('/src/hp1.xml').read_text()
fixm_schema.CreateFromDocument(xml)
