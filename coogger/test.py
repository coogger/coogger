from bs4 import BeautifulSoup
renderer = mistune.Renderer(escape=False)
markdown = mistune.Markdown(renderer=renderer)
content = markdown(content)
content = BeautifulSoup(content,"html.parser")
src = content.find("img").get("src")
alt = content.find("img").get("alt")
renderer.image(src = src,title = alt,text = alt)
