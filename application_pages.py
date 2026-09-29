"""Fall 2027 application materials, sharing the PDF authoring text."""
import json
from pathlib import Path
from html import escape

DATA=json.loads((Path(__file__).parent/'application_content.json').read_text(encoding='utf-8'))
FILES={
 'sop':'Tong_Stone_Shi_Statement_of_Purpose_Fall_2027.pdf',
 'personal':'Tong_Stone_Shi_Personal_Statement_Fall_2027.pdf',
}

def application_page(key, base):
    doc=DATA[key]
    sections=[]
    for section in doc['sections']:
        heading=f'<h2>{escape(section["heading"])}</h2>' if section['heading'] else ''
        paragraphs=''.join(f'<p>{escape(text)}</p>' for text in section['paragraphs'])
        sections.append(f'<section>{heading}{paragraphs}</section>')
    body=f'''<article class="document-page application-page">
      <p class="eyebrow">{escape(DATA['cycle'])}</p>
      <h1>{escape(doc['title'])}</h1>
      <p class="lead">{escape(doc['subtitle'])}</p>
      <div class="button-row"><a class="button primary" href="/static/documents/{FILES[key]}" download>Download PDF</a><a class="button secondary" href="/cv">View research CV</a></div>
      <div class="application-prose">{''.join(sections)}</div>
    </article>'''
    return base(doc['title']+' | Tong (Stone) Shi',body)
