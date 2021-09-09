import requests
import ezsheets
import json

with open('tags.txt') as fp:
    tags = fp.readlines()

    ss = ezsheets.createSpreadsheet(title="Touhou lewding")
    sheet = ss.sheets[0]
    sheet.updateRow(1, ("Name", "Total", "Safe count", "Questionable count", "Explicit count", "Safe%", "Questionable%", "Explicit%", "NSFW% (Questionable + Explicit)"))

    row = 2

    for tag in tags:
        #total number of posts for a tag
        r = requests.get("https://danbooru.donmai.us/counts/posts.json?tags=%s" % tag)
        loadr = r.json()
        total = str(loadr["counts"])
        total = total.replace("{'posts': ", "").replace("}", "")

        #number of safe rated posts for a tag
        s = requests.get("https://danbooru.donmai.us/counts/posts.json?tags=%s+rating:s" % tag)
        loads = s.json()
        safe = str(loads["counts"])
        safe = safe.replace("{'posts': ", "").replace("}", "")

        #number of questionable rated posts for a tag
        q = requests.get("https://danbooru.donmai.us/counts/posts.json?tags=%s+rating:q" % tag)
        loadq = q.json()
        questionable = str(loadq["counts"])
        questionable = questionable.replace("{'posts': ", "").replace("}", "")

        #number of explicit rated posts for a tag
        e = requests.get("https://danbooru.donmai.us/counts/posts.json?tags=%s+rating:e" % tag)
        loade = e.json()
        explicit = str(loade["counts"])
        explicit = explicit.replace("{'posts': ", "").replace("}", "")

        #counting the percentages of each rating
        safeperc = int(safe)*100/int(total)
        questionableperc = int(questionable)*100/int(total)
        explicitperc = int(explicit)*100/int(total)
        nsfwperc = questionableperc+explicitperc

        name = tag.replace("_", " ").replace("%28", "(").replace("%29", ")").replace("%27", "'")

        if "(touhou)" in name:
            name = name.replace("(touhou)", "")

        if r.status_code == 200 and s.status_code == 200 and q.status_code == 200 and e.status_code == 200:
            sheet.updateRow(row, (name.title(), total, safe, questionable, explicit, "{:.2f}".format(safeperc), "{:.2f}".format(questionableperc), "{:.2f}".format(explicitperc), "{:.2f}".format(nsfwperc)))
            print(row, name.title(), total, safe, questionable, explicit, 
            "{:.2f}".format(safeperc), "%", "{:.2f}".format(questionableperc), "%", "{:.2f}".format(explicitperc), "%", "{:.2f}".format(nsfwperc), "%")
            row = row + 1