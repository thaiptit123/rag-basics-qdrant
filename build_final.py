import re
import os

# 1. Run pandoc to convert the newly structured Markdown
os.system('pandoc bai_1_qdrant_tutorial.md -s -o temp_standalone.tex')

# 2. Read the pandoc output
with open('temp_standalone.tex', 'r', encoding='utf-8') as f:
    tex = f.read()

# 3. Read template
with open('../AI_Guru_Tutorial_Series_Template.tex', 'r', encoding='utf-8') as f:
    template = f.read()

match = re.search(r'\\usepackage\{fontspec\}(.*?)\\setlength\{\\parskip\}\{0\.5em\}', template, re.DOTALL)
preamble = match.group(0)
preamble = preamble.replace('fig/aiguru-logo.png', '../aiguru-logo.png')
preamble = preamble.replace(r'\newcommand{\watermarkLogo}{../aiguru-logo.png}', r'\newcommand{\watermarkLogo}{../aiguru-logo-faded.png}')
preamble = preamble.replace('[opacity=0.10]', '')
preamble = preamble.replace('fig/tinix-logo.png', '../tinix-logo.png')
# Fix TikZ $ catcode issue when shipping out during a Verbatim environment
preamble = preamble.replace('\\begin{tikzpicture}', '\\begingroup\\catcode`\\$=3\n  \\begin{tikzpicture}')
preamble = preamble.replace('\\end{tikzpicture}%', '\\end{tikzpicture}%\n  \\endgroup')
preamble += "\n\\usepackage{fvextra}\n\\usepackage{caption}\n\\captionsetup{font=large}\n\\usepackage{float}\n\\usepackage{tocloft}\n\\renewcommand{\\cftsecleader}{\\cftdotfill{\\cftdotsep}}\n"
preamble += "\\setlength{\\fboxsep}{0pt}\n\\setlength{\\fboxrule}{0.5pt}\n"

# Code block wrapping will be applied to tex directly below.

tex = tex.replace(r'\begin{figure}', r'\begin{figure}[H]')
# We also need to add a command to draw lines in tables (fixing the borders)
# The user wants prominent borders for the glossary table
tex = tex.replace(r'\begin{longtable}[]{@{}lll@{}}', r'\begin{longtable}{|p{0.2\linewidth}|p{0.25\linewidth}|p{0.45\linewidth}|}')
tex = tex.replace(r'\begin{longtable}[]{@{}lllll@{}}', r'\begin{longtable}{|p{0.12\linewidth}|p{0.17\linewidth}|p{0.17\linewidth}|p{0.22\linewidth}|p{0.17\linewidth}|}')
tex = tex.replace(r'\begin{longtable}[]{@{}lllllll@{}}', r'\begin{longtable}{|p{0.13\linewidth}|p{0.05\linewidth}|p{0.08\linewidth}|p{0.15\linewidth}|p{0.07\linewidth}|p{0.08\linewidth}|p{0.30\linewidth}|}') # For the comparison table (7 columns)

def color_header(match):
    header_content = match.group(1)
    parts = header_content.split(r'\tabularnewline')
    new_parts = []
    for part in parts:
        if not part.strip():
            new_parts.append(part)
            continue
        cells = part.split('&')
        new_cells = [f'\\thd{{{c.strip()}}}' for c in cells]
        new_parts.append(' & '.join(new_cells))
    return r'\hline' + '\n' + r'\tabularnewline'.join(new_parts) + r'\hline'

tex = re.sub(r'\\toprule(.*?)\\midrule', color_header, tex, flags=re.DOTALL)
tex = tex.replace(r'\bottomrule', r'\hline')
# Also we need to make sure rows have \hline between them if user wants "nổi bật các đường khung"
tex = re.sub(r'(\\\\)\s*(\n\s*[^\\&]+&)', r'\1\n\\hline\2', tex)

# Strip pandoc's minipages inside tables so they can actually resize to p{...}
tex = re.sub(r'\\begin\{minipage\}\[.*?\]\{.*?\}', '', tex)
tex = tex.replace(r'\end{minipage}', '')

# Fix code blocks wrapping
tex = tex.replace(
    r'\DefineVerbatimEnvironment{Highlighting}{Verbatim}{commandchars=\\\{\}}',
    r'\DefineVerbatimEnvironment{Highlighting}{Verbatim}{commandchars=\\\{\},breaklines=true,breakanywhere=true,fontsize=\small,frame=single,framesep=2mm,rulecolor=\color{gray}}'
)

# Fix verbatim block wrapping
tex = tex.replace(r'\begin{verbatim}', r'\begin{Verbatim}[breaklines=true, breakanywhere=true, frame=single, framesep=2mm, rulecolor=\color{gray}]')
tex = tex.replace(r'\end{verbatim}', r'\end{Verbatim}')

# Fix image newlines so they aren't inline
tex = re.sub(r'(\\textgreater\{\})\s*(\n\s*\\includegraphics)', r'\1\n\2', tex)

# Wrap images in fbox for borders
tex = re.sub(r'\\includegraphics\{(.*?)\}', r'\\fbox{\\includegraphics{\1}}', tex)

# 4. Extract Cover Page Content
cover_match = re.search(r'\\hypertarget\{[^}]*\}\{%\n\\section\{(.*?)\}.*?(?=\\section\*?\{Các thuật ngữ|\\addcontentsline\{toc\}\{section\}\{Các thuật ngữ)', tex, re.DOTALL)
if cover_match:
    cover_content = cover_match.group(0)
    title_text = cover_match.group(1)
    # Remove it from the main body
    tex = tex.replace(cover_content, '', 1)
    # Also remove any horizontal rules that might be around
    tex = re.sub(r'\\begin\{center\}\\rule\{.*?\}\{.*?\}\\end\{center\}', '', tex)
    
    # Format the cover content properly
    formatted_title = title_text.replace(': ', ':\\\\ ')
    cover_content = cover_content.replace(f'\\section{{{title_text}}}', f'\\begin{{center}}\\color{{primary}}\\fontsize{{26}}{{32}}\\selectfont\\bfseries {formatted_title}\\end{{center}}\\vspace{{1cm}}')
    
    # Add Author at the bottom of the cover page
    cover_content += r"""
\vfill
\begin{center}
\textbf{Tác giả:} Kỹ sư AI Phạm Thành Thái\\
AI Guru x TiniX
\end{center}
\newpage
"""
else:
    cover_content = ""

# Old author string deletion removed to prevent deleting the bibliography.

# Remove pandoc date
tex = re.sub(r'\\date\{\}', '', tex)

# Combine TOC
toc_code = r"""
\renewcommand{\contentsname}{\begin{center}\color{primary}\textbf{\MakeUppercase{Mục Lục}}\end{center}}
\tableofcontents
\newpage
"""

# Inject everything
insertion = preamble + "\n\\begin{document}\n\\thispagestyle{fancy}\n" + cover_content + toc_code
tex = tex.replace('\\begin{document}', insertion)

# Fix 2-column table wrapping and add vertical lines (Glossary)
tex = tex.replace(r'\begin{longtable}[]{@{}ll@{}}', r'\begin{longtable}{| p{0.25\textwidth} | p{0.7\textwidth} |}')

# Add horizontal lines between all table rows
tex = tex.replace(r'\tabularnewline', r'\tabularnewline \hline')
tex = tex.replace(r'\hline\n\endhead', r'\endhead') # Remove duplicate hline if any

with open('bai_1_qdrant_tutorial.tex', 'w', encoding='utf-8') as f:
    f.write(tex)

print("Generated Final Tex")
