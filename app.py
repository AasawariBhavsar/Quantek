from fastapi import FastAPI
import re
import sys
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse

app = FastAPI()


storeArray = []
storeObj = {}
stringResult = ""

# lines = []
# while True:
#     line = input()
#     if line:
#         lines.append(line.strip())
#     else:
#         break
# htmlString = '\n'.join(lines)

# htmlString = """
# <html>
# <body>
#
# <button value="Foo" class="aa"/>
# <button value="Foo" class="aa"/>
# <button value="Boo" class="bb"/>
# <div>
#   <h1 class="red-text"> My Text </h1>
# </div>
#
# <div>
#   <h1 class="red-text"> My Text </h1>
# </div>
#
# <div>
#   <h1 class="red-text"> My Text </h1>
# </div>
#
# </body>
# </html>
# """
# htmlString = sys.stdin.readlines()

def countTags(tag):
    storeArray.append(tag)
    if tag in storeObj.keys():
        storeObj[tag] += 1
    else:
        storeObj[tag] = 1


def isNonSingularOrNonSelfClosing(tagName):
    singularTags = ['br', 'hr']
    if re.search(r"[^/]/\s*$", tagName):
        return False
    if tagName in singularTags:
        return False
    return True


def parseUpperTags(string, level, prevTag):
    global stringResult

    # print(htmlString)

    if not re.search(r"(.*?)<(/?\w+).*?>(.*)", string, flags=re.IGNORECASE | re.DOTALL):
        return string
    finalString = ""
    m = re.search(r"(.*?)(<(/?\w+).*?(/?)\s*>)(.*)", string, flags=re.IGNORECASE | re.DOTALL)

    [beforeTag, tag, tagName, selfCloseSlash, remainingTag] = m.groups()
    print(type(beforeTag))
    tagName += selfCloseSlash or ""

    if prevTag:
        if ((not "/" in prevTag and (not "/" in tagName) and isNonSingularOrNonSelfClosing(
                re.sub(r"<|>", "", tag, flags=re.IGNORECASE | re.DOTALL))
             and isNonSingularOrNonSelfClosing(prevTag))
                or (not "/" in prevTag and isNonSingularOrNonSelfClosing(prevTag) and not isNonSingularOrNonSelfClosing(
                    re.sub(r"<|>", "", tag, flags=re.IGNORECASE | re.DOTALL)))):
            level += 1
        elif (
                ("/" in prevTag and "/" in tagName and isNonSingularOrNonSelfClosing(
                    re.sub(r"<|>", "", tag, flags=re.IGNORECASE | re.DOTALL))
                 and isNonSingularOrNonSelfClosing(prevTag))
                or (not isNonSingularOrNonSelfClosing(prevTag) and isNonSingularOrNonSelfClosing(
            re.sub(r"<|>", "", tag, flags=re.IGNORECASE | re.DOTALL))
                    and "/" in tagName)):
            level -= 1
    finalString += beforeTag + tag

    stringResult += finalString

    if level == 1 and "/" in tagName:
        countTags(re.sub(r">\s+<", '><', stringResult.strip(), flags=re.IGNORECASE | re.DOTALL))
        stringResult = ""
    finalString += parseUpperTags(remainingTag, level, tagName)
    return finalString



def counter(html):
    body = re.search(r"<body>(.*)</body>", html, flags=re.DOTALL | re.IGNORECASE).group(1)
    print(body)
    level = 1
    parseUpperTags(body, level, '')

    return storeObj


# counter(htmlString)
class Item(BaseModel):
    htmlString:str=Field(example="<html><body><button value=\"Foo\" class=\"aa\"/><button value=\"Boo\" class=\"bb\"/><button value=\"Foo\" class=\"aa\"/><div><h1 class=\"red-text\">My Text</h1></div><div><h1 class=\"red-text\">My Text</h1></div><div><h1 class=\"red-text\">My Text</h1></div></body></html>")


@app.get("/")
async def index():
    return "Go to swagger ui"

@app.post("/items/")
async def createitem(item:Item):
    # htmlString= item.htmlString.replace('"', '\"').strip()
    # print(htmlString)
    htmlparse = counter(item.htmlString)
    return htmlparse
    # return item


# @app.get("/")
# async def index():
#     htmlparse=counter()
#     return htmlparse
