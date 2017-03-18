import html

def unescape(s):
    s = html.unescape(s)

if __name__ == '__main__':
    s = unescape("Victor Hugo's &amp;lt;i&amp;gt;Les Misérables&amp;lt;/i&amp;gt;");
    print(s)
