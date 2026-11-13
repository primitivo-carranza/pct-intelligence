#!/usr/bin/env python3
"""Weekly bibliographic discovery. Candidate matches require human validation."""
import json, os, re, datetime, urllib.parse, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
feed=json.loads((ROOT/"data/robotics-feed.json").read_text())
path=ROOT/"data/robotics-publications.json"
previous=json.loads(path.read_text()) if path.exists() else {"publications":[]}
today=datetime.date.today()
terms=["construction robot inspection","autonomous construction site monitoring","robotic infrastructure inspection","construction digital twin computer vision"]
def get(query):
    params=urllib.parse.urlencode({"query.title":query,"rows":20,"filter":"from-pub-date:"+str(today-datetime.timedelta(days=120)),"select":"DOI,title,author,published,container-title,URL,abstract"})
    req=urllib.request.Request("https://api.crossref.org/works?"+params,headers={"User-Agent":"PCT-RoboInspector-Radar/1.0 (research bibliographic monitor)"})
    with urllib.request.urlopen(req,timeout=25) as response:return json.load(response)["message"]["items"]
def norm(x):return re.sub(r"[^a-z0-9]+"," ",x.lower()).strip()
keywords=("robot","inspect","construction","autonom","digital twin","computer vision","site monitoring","infrastructure")
known={norm(p["name"]):p for p in feed.get("people",[])}
records={x["doi"].lower():x for x in previous.get("publications",[]) if x.get("doi")}
for term in terms:
    try: items=get(term)
    except Exception as exc:
        print("Crossref failed:",term,str(exc))
        continue
    for item in items:
        doi=item.get("DOI","").lower()
        title=(item.get("title") or [""])[0]
        if not doi or not any(k in norm(title) for k in keywords):continue
        authors=item.get("author",[])
        author_names=[(a.get("given","")+" "+a.get("family","")).strip() for a in authors]
        matches=[{"id":known[norm(n)]["id"],"name":n,"matchType":"nombre exacto; identidad no verificada"} for n in author_names if norm(n) in known]
        affs=list(dict.fromkeys(a.get("name","") for author in authors for a in author.get("affiliation",[]) if a.get("name")))
        institution_matches=[{"id":inst["id"],"name":inst["name"],"matchType":"texto de afiliación; verificar"} for inst in feed.get("institutions",[]) if any(norm(inst["name"].split(" · ")[0]) in norm(a) for a in affs) and len(norm(inst["name"].split(" · ")[0]))>3]
        pubdate=item.get("published",{}).get("date-parts",[[None]])[0]
        date="-".join(str(v).zfill(2) for v in pubdate) if pubdate else ""
        records[doi]={"doi":doi,"name":title,"date":date,"journal":(item.get("container-title") or [""])[0],"authors":"; ".join(author_names),"affiliations":"; ".join(affs),"source":"https://doi.org/"+doi,"peopleMatches":matches,"institutionMatches":institution_matches,"technology":"Inspección / robótica / IA (clasificación preliminar)","application":"Evaluar posible aplicación a Robo-Inspector","priority":"Por evaluar","contactOpportunity":"Revisar autores y afiliaciones; contacto no confirmado","validation":"Candidato bibliográfico; vínculos no verificados","discoveredAt":str(today)}
previous["generatedAt"]=str(today)
previous["source"]="Crossref REST API; consultas temáticas; coincidencias de autor/afiliación no verificadas"
previous["publications"]=sorted(records.values(),key=lambda x:x.get("date",""),reverse=True)[:500]
path.write_text(json.dumps(previous,ensure_ascii=False,indent=2)+"\n")
print("Publications:",len(previous["publications"]))
