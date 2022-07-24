import re

storeArray = []
storeObj = {}
stringResult = ""


htmlString = """
<html>
<body>

<button value="Foo" class="aa"/>
<button value="Foo" class="aa"/>
<button value="Boo" class="bb"/>
<div>
  <h1 class="red-text"> My Text </h1>
</div>

<div>
  <h1 class="red-text"> My Text </h1>
</div>

<div>
  <h1 class="red-text"> My Text </h1>
</div>

</body>
</html>
"""





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

    print(htmlString)

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
    body = re.search(r"<body>(.*)</body>", html,flags=re.DOTALL | re.IGNORECASE).group(1)

    level = 1
    parseUpperTags(body, level, '')

    print(storeObj)


counter(htmlString)
