import sqlite3
from pprint import pprint

HTML = """
<!doctype html>
<html>
<head>
    <title>Our Funky HTML Page</title>
    <meta name="description" content="Our first page">
    <meta name="keywords" content="html tutorial template">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
{nav}
{body}
</body>
</html>
""".strip()

NAV = """
<nav aria-labelledby=table-of-contents">
  <h2 id="table-of-contents">
    Table of contents
  </h2>
{content}
</nav>
""".strip()

NAV_LIST = """
<ul>
{content}
</ul>
"""

BOOK_NAV_ENTRY = """
<li>
    <a id="toc-{book}" href="#{book}">
        {book}
    </a>
    {content}
</li>
"""

CHAPTER_NAV_ENTRY = """
<li>
    <a id="toc-{book}-{chapter}" href="#{book}-{chapter}">
        {chapter}
    </a>
</li>
"""

H2 = """
<h2 id="{id}">
    <a href="#toc-{id}">{content}</a>
    <a class="hdr" href="#{id}">§</a>
</h2>
""".strip()

H3 = """
<h3 id="{book}-{chapter}">
    <a href="#toc-{book}-{chapter}">{content}</a>
    <a class="hdr" href="#{book}-{chapter}">§</a>
</h3>
""".strip()

P = """
<p id="#toc-{book}-{chapter}-{verse}">
{content}
</p>
""".strip()

SPAN = """
<span>{content}</span>
""".strip()


def main():
    body = ""
    con = sqlite3.connect("bible.db")
    cur = con.cursor()
    books = cur.execute("SELECT * FROM book").fetchall()
    # pprint(book_ids)
    genesis = books[0]
    genesis_title = genesis[1].capitalize()
    body += f"{H2.format(id=genesis_title, content=genesis_title)}\n"
    genesis_chapters = cur.execute(f"SELECT * FROM book_chapter AS bc WHERE bc.book_id={genesis[0]}").fetchall()
    # pprint(genesis_chapters)
    chapter_entries = ""
    for gc in genesis_chapters[:3]:
        gc_id = gc[0]
        gc_number = gc[1]
        chapter_entries += f"{CHAPTER_NAV_ENTRY.format(book=genesis_title, chapter=gc_number)}\n"
        gen_ch = f"{genesis_title} {gc_number}"
        print(f"Creating: {gen_ch}")
        # print(H3.format(id=gen_ch, content=gen_ch))
        body += f"{H3.format(book=genesis_title, chapter=gc_number, content=gen_ch)}\n"
        verses = cur.execute(f"SELECT * FROM verse AS v WHERE v.book_chapter_id={gc_id}").fetchall()
        for v in verses:
            v_id = v[0]
            v_number = v[1]
            heading_id = v[3]
            words = cur.execute(f"SELECT * FROM bible_word as bw WHERE bw.verse_id={v_id} ORDER BY bw.bsb_location").fetchall()
            # pprint(words)
            p_content = ""
            w_len = len(words) - 1
            for i, ww in enumerate(words):
                w = ww[3]
                # print(w, end=" ")
                span = SPAN.format(content=w)
                if i != w_len:
                    p_content += f"  {span}\n"
                else:
                    p_content += f"  {span}"
            p = P.format(book=genesis_title, chapter=gc_number, verse=v_number, content=p_content)
            body += f"{p}\n"
            # print(p)
        # pprint(verses)
    chapters = NAV_LIST.format(content=chapter_entries) + "\n"
    book_entry = BOOK_NAV_ENTRY.format(book=genesis_title, content=chapters) + "\n"
    nav_list = NAV_LIST.format(content=book_entry) + "\n"
    nav = NAV.format(content=nav_list) + "\n"
    html = HTML.format(nav=nav, body=body)
    with open("site.html", "w") as f:
        f.write(html)


if __name__ == "__main__":
    main()
