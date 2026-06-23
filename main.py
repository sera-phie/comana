import csv
import json
import os
import platform
import subprocess
import sys
import re
import uuid
import shutil

abbrDict = {
    "clrScr": "Clear Screen",
    "iniApp": "Initialize Application",
    "svCfg": "Save Configuration",
    "setMnu": "Settings Menu",
    "cvCxs": "Convert CXS",
    "getLs": "Get Language List",
    "mkLng": "Make Language",
    "ldCsv": "Load CSV",
    "svCsv": "Save CSV",
    "ldPdm": "Load Paradigm CSV",
    "svPdm": "Save Paradigm CSV",
    "getOrt": "Get Orthography",
    "getSyms": "Get Symbols (Clustered)",
    "mkOrt": "Make Orthography",
    "mkPdm": "Make Paradigm",
    "aplyMut": "Apply Mutation",
    "trnSltr": "Translator",
    "addWrd": "Add Word",
    "srcWrd": "Search Word",
    "edtWrd": "Edit Word",
    "vwWrd": "View Words",
    "runLx": "Run Lexurgy",
    "applyLx": "Apply Lexurgy Headless",
    "getDaus": "Get Daughter Languages",
    "doSync": "Execute Synchronization",
    "syncWrd": "Sync Words",
    "mkDau": "Make Daughter Language",
    "edtPdm": "Edit Paradigm",
    "pdmMnu": "Paradigm Menu",
    "wrkSpc": "Workspace Environment",
    "mnApp": "Main Application Loop",
    "cmpLng": "Compare Languages",
    "getParent": "Get Parent Language",
    "setParent": "Set Parent Language",
    "vwTree": "View Language Family Tree",
    "evlWrdTr": "Evolve Word Tree",
    "prtWrdTr": "Print Word Tree",
    "nLng": "Node Language",
    "nIpa": "Node IPA",
    "nOrt": "Node Orthography",
    "pref": "Prefix",
    "isLst": "Is Last",
    "mkr": "Marker",
    "cPref": "Child Prefix",
    "isLChld": "Is Last Child",
    "evIpa": "Evolved IPA",
    "dirNm": "Directory Name",
    "hdrLst": "Header List",
    "pdmHdr": "Paradigm Header List",
    "cfgDat": "Configuration Data",
    "c2iMap": "CXS to IPA Mapping",
    "Col": "ANSI Colors",
    "lngNm": "Language Name",
    "csvDat": "CSV Data",
    "pdmDat": "Paradigm Data",
    "ortDat": "Orthography Data",
    "symSet": "Symbol Set",
    "mchObj": "Match Object",
    "qryStr": "Query String",
    "resLst": "Result List",
    "fldNm": "Field Name",
    "nwVal": "New Value",
    "lscTxt": "LSC Text",
    "inpPth": "Input Path",
    "outPth": "Output Path",
    "sncLst": "Sync List",
    "rcsChc": "Recurse Choice",
    "mnuChc": "Menu Choice",
    "tblNm": "Table Name",
    "rNm": "Row Name",
    "cNm": "Column Name",
    "aTy": "Affix Type",
    "mRl": "Mutation Rule",
    "mtxDat": "Matrix Data",
    "bStr": "Base String",
    "xCt": "X Count",
    "rMn": "Remaining Rule",
    "gInp": "Gloss Input",
    "wTks": "Word Tokens",
    "tLs": "Tags List",
    "mchLst": "Match List",
    "rGl": "Root Gloss",
    "pdmFlg": "Paradigm Flag",
    "tNms": "Table Names",
    "tgtTbl": "Target Table",
    "tblDat": "Table Data",
    "l1": "Language 1",
    "l2": "Language 2",
    "d1": "Data 1",
    "d2": "Data 2",
    "cvPts": "Converted Parts",
    "rLst": "Rule List",
    "tmpOrt": "Temporary Orthography"
}

dirNm = "lang"
hdrLst = ["Lemma", "Gloss", "IPA", "PoS", "Etymology", "Notes", "Tags", "Related Words"]
pdmHdr = ["tblNm", "rowNm", "colNm", "afxTy", "mutRl"]
cfgDat = {"cxs": False}

class Col:
    err = '\033[91m'
    ok = '\033[92m'
    hdr = '\033[93m'
    prm = '\033[96m'
    ipa = '\033[95m'
    rst = '\033[0m'

c2iMap = {
    "u\\": "ʉ", "&\\": "œ", "&": "æ", "'": "ˈ", ",": "ˌ",
    "A": "ɑ", "B": "β", "C": "ç", "D": "ð", "E": "ɛ", "F": "ɱ", "G": "ɣ",
    "H": "ɥ", "I": "ɪ", "J": "ɲ", "K": "ɬ", "L": "ʎ", "M": "ɯ", "N": "ŋ",
    "O": "ɔ", "P": "ʋ", "Q": "ɒ", "R": "ʁ", "S": "ʃ", "T": "θ", "U": "ʊ",
    "V": "ʌ", "W": "ʍ", "X": "χ", "Y": "ʏ", "Z": "ʒ", "?\\": "ʕ", "h\\": "ɦ",
    "j\\": "ʝ", "l\\": "ɺ", "n\\": "ɳ", "r\\": "ɹ", "s\\": "ɕ", "t\\": "ʈ",
    "v\\": "ʋ", "x\\": "ɧ", "z\\": "ʑ", "@\\": "ɘ", "@": "ə", "3\\": "ɞ",
    "3": "ɜ", "6": "ɐ", "7": "ɤ", "8": "ɵ", "9": "œ", "!": "ꜜ",
    "|\\": "ǀ", "|\\|\\": "ǁ", "!\\": "ǃ", "=\\": "ǂ", "-\\": "‿",
    "4": "ɾ", "5": "ɫ", "1": "ɨ", "2": "ø", "b_<": "ɓ", "d_<": "ɗ",
    "g_<": "ɠ", "G\\_<": "ʛ", "p\\": "ɸ", "B\\": "ʙ", "d\\": "ɖ",
    "_>": "ʼ",
    "J\\": "ɟ", "K\\": "ɮ", "G\\": "ɢ", "N\\": "ɴ", "X\\": "ħ",
    "R\\": "ʀ", "H\\": "ʜ", "?": "ʔ", "O\\": "ʘ", "r\\`": "ɻ",
    "L\\": "ʟ", "M\\": "ɰ", "~": "̃", ":": "ː", ":\\": "ˑ", "=": "̩",
    "_j": "ʲ", "_w": "ʷ", "_h": "ʰ", "_n": "ⁿ", "_l": "ˡ", "_~": "̃",
    "_T": "̋", "_H": "́", "_M": "̄", "_L": "̀", "_B": "̏", "_R": "̌", "_F": "̂"
}

def clrScr():
    os.system('cls' if os.name == 'nt' else 'clear')

def iniApp():
    global cfgDat
    if not os.path.exists(dirNm): os.makedirs(dirNm)
    if os.path.exists("config.json"):
        with open("config.json", "r") as f: cfgDat = json.load(f)
    else: svCfg()

def svCfg():
    with open("config.json", "w") as f: json.dump(cfgDat, f)

def setMnu():
    cfgDat["cxs"] = not cfgDat.get("cxs", False)
    svCfg()
    print(f"{Col.ok}CXS input is now {'ON' if cfgDat['cxs'] else 'OFF'}.{Col.rst}")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def cvCxs(inStr, lscFlg=False, pdmFlg=False):
    if lscFlg or pdmFlg:
        mskDct = {}
        def mskRpl(mchObj):
            k = chr(0xE000 + len(mskDct))
            mskDct[k] = mchObj.group(0)
            return k
            
        if lscFlg:
            inStr = re.sub(r'(?m)^\s*[A-Za-z0-9_-]+\s*:', mskRpl, inStr)
            inStr = re.sub(r'\b(?:Class|Feature|Symbol)\s+[A-Za-z0-9_-]+', mskRpl, inStr)
            inStr = re.sub(r'\b(then)\b', mskRpl, inStr)
            inStr = re.sub(r'[@\$][A-Za-z0-9_-]+', mskRpl, inStr)
            inStr = re.sub(r'=>|//|\[\[|\]\]|\{|\}|\$|/', mskRpl, inStr)
            inStr = re.sub(r'(?<!\\)_', mskRpl, inStr)
            inStr = re.sub(r'(?<!\\):', mskRpl, inStr)
            inStr = re.sub(r'(?<!\\),', mskRpl, inStr)
            inStr = inStr.replace(r"\_", "_").replace(r"\:", ":").replace(r"\,", ",")

        if pdmFlg:
            inStr = re.sub(r'[/<>]', mskRpl, inStr)

    for k, v in sorted(c2iMap.items(), key=lambda x: -len(x[0])):
        inStr = inStr.replace(k, v)
        
    inStr = re.sub(r"(.)(.)\)", r"\1͡\2", inStr)
    
    if lscFlg or pdmFlg:
        for k, v in mskDct.items(): inStr = inStr.replace(k, v)
            
    return inStr

def getLs():
    lst = []
    for d in os.listdir(dirNm):
        p = os.path.join(dirNm, d)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, f"{d}.csv")):
            lst.append(d)
    return lst

def getParent(dNm):
    pPth = os.path.join(dirNm, dNm, "parent.txt")
    if os.path.exists(pPth):
        with open(pPth, "r", encoding="utf-8") as f: 
            return f.read().strip()
    
    csvPth = os.path.join(dirNm, dNm, f"{dNm}.csv")
    if os.path.exists(csvPth):
        with open(csvPth, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
            for r in reader:
                m = re.match(r"Derived from (.*?):", r.get("Etymology", ""))
                if m:
                    p = m.group(1).strip()
                    if p != dNm and os.path.exists(os.path.join(dirNm, p)):
                        setParent(dNm, p)
                        return p
    return None

def setParent(dNm, pNm):
    with open(os.path.join(dirNm, dNm, "parent.txt"), "w", encoding="utf-8") as f:
        f.write(pNm)

def mkLng(lngNm=None):
    clrScr()
    if not lngNm: lngNm = input(f"{Col.prm}New language name: {Col.rst}").strip()
    p = os.path.join(dirNm, lngNm)
    if not os.path.exists(p): os.makedirs(p)
    csvPth = os.path.join(p, f"{lngNm}.csv")
    if not os.path.exists(csvPth):
        with open(csvPth, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(hdrLst)
    return lngNm

def ldCsv(lngNm):
    with open(os.path.join(dirNm, lngNm, f"{lngNm}.csv"), "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def svCsv(lngNm, csvDat):
    with open(os.path.join(dirNm, lngNm, f"{lngNm}.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=hdrLst)
        w.writeheader()
        w.writerows(csvDat)

def ldPdm(lngNm):
    pth = os.path.join(dirNm, lngNm, "paradigms.csv")
    if not os.path.exists(pth): return []
    with open(pth, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def svPdm(lngNm, pdmDat):
    pth = os.path.join(dirNm, lngNm, "paradigms.csv")
    with open(pth, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=pdmHdr)
        w.writeheader()
        w.writerows(pdmDat)

def getOrt(lngNm, ipaStr):
    jf = os.path.join(dirNm, lngNm, f"{lngNm}.json")
    if not os.path.exists(jf): return ipaStr
    with open(jf, "r", encoding="utf-8") as f: ortDat = json.load(f)
    
    srtKeys = sorted(ortDat.keys(), key=len, reverse=True)
    outStr = ""
    idx = 0
    
    while idx < len(ipaStr):
        isMch = False
        for k in srtKeys:
            if ipaStr.startswith(k, idx):
                outStr += ortDat[k]
                idx += len(k)
                isMch = True
                break
        if not isMch:
            outStr += ipaStr[idx]
            idx += 1
            
    return outStr

def getSyms(ipaStr):
    symLst = []
    idx = 0
    ipaStr = ipaStr.replace(" ", "")
    while idx < len(ipaStr):
        c = ipaStr[idx]
        idx += 1
        while idx < len(ipaStr):
            nxt = ipaStr[idx]
            if nxt in "ːˑʰʷʲⁿˡ̩̃" or ('\u0300' <= nxt <= '\u036F'):
                c += nxt
                idx += 1
            elif nxt == '͡' and idx + 1 < len(ipaStr):
                c += nxt + ipaStr[idx+1]
                idx += 2
            else:
                break
        symLst.append(c)
    return symLst

def mkOrt(lngNm):
    clrScr()
    csvDat = ldCsv(lngNm)
    symSet = set()
    for r in csvDat:
        for c in getSyms(r["IPA"]):
            if c.strip(): symSet.add(c)
    
    print(f"{Col.hdr}Current IPA:{Col.rst} {Col.ipa}{', '.join(symSet)}{Col.rst}\n")
    wh = input(f"{Col.prm}Add more IPA symbols? (space separated): {Col.rst}").strip()
    if wh:
        if cfgDat.get("cxs", False): wh = cvCxs(wh)
        symSet.update(wh.split())
    
    ortDat = {}
    jf = os.path.join(dirNm, lngNm, f"{lngNm}.json")
    if os.path.exists(jf):
        with open(jf, "r", encoding="utf-8") as f: ortDat = json.load(f)

    print(f"\n{Col.prm}Define orthography. Press Ctrl+C to quit and save early.{Col.rst}")
    try:
        for s in sorted(list(symSet), key=lambda x: -len(x)):
            if s not in ortDat:
                v = input(f"Glyph for {Col.ipa}'{s}'{Col.rst} (leave blank for '{s}'): ").strip()
                ortDat[s] = v if v else s
    except KeyboardInterrupt:
        print(f"\n{Col.hdr}Saving early...{Col.rst}")
    
    with open(jf, "w", encoding="utf-8") as f: json.dump(ortDat, f, indent=2)
    
    for r in csvDat: r["Lemma"] = getOrt(lngNm, r["IPA"])
    svCsv(lngNm, csvDat)
    
    for dNm in getLs():
        if dNm == lngNm: continue
        dDat = ldCsv(dNm)
        chg = False
        for r in dDat:
            ety = r["Etymology"]
            m = re.match(rf"(Derived from {lngNm}: )(.*?) /(.*?)/", ety)
            if m:
                nOrt = getOrt(lngNm, m.group(3))
                if m.group(2) != nOrt:
                    r["Etymology"] = f"{m.group(1)}{nOrt} /{m.group(3)}/"
                    chg = True
        if chg: svCsv(dNm, dDat)

def mkPdm(lngNm):
    clrScr()
    print(f"{Col.hdr}--- Paradigm Creator ---{Col.rst}\n")
    tNm = input(f"{Col.prm}Table Name (e.g. VerbConj): {Col.rst}").strip()
    rWs = [x.strip() for x in input(f"{Col.prm}Row Glosses (comma sep, e.g. 1SG,2SG): {Col.rst}").split(',') if x.strip()]
    cLs = [x.strip() for x in input(f"{Col.prm}Col Glosses (comma sep, optional, e.g. PRES,PAST): {Col.rst}").split(',')]
    if not cLs or cLs[0] == '': cLs = [""]

    pdmDat = ldPdm(lngNm)
    mtxDat = {r: {c: "" for c in cLs} for r in rWs}

    for rNm in rWs:
        for cNm in cLs:
            clrScr()
            print(f"{Col.hdr}--- {tNm} ---{Col.rst}\n")
            
            hdr = f"{'':<8} | " + " | ".join([f"{Col.hdr}{c:^10}{Col.rst}" for c in cLs])
            print(hdr)
            print("-" * (11 + 13 * len(cLs)))
            
            for row in rWs:
                rowStr = f"{Col.hdr}{row:<8}{Col.rst} | " + " | ".join([f"{mtxDat[row][col]:^10}" for col in cLs])
                print(rowStr)
            
            print(f"\n{Col.prm}Defining cell for Row: {Col.ok}{rNm}{Col.rst} {Col.prm}| Col: {Col.ok}{cNm}{Col.rst}")
            mRl = input(f"{Col.prm}Mutation Rule (e.g. p:a4*s://s<<<a): {Col.rst}").strip()
            if not mRl: continue
            
            cvPts = []
            for p in mRl.split('*'):
                if p.startswith('p:'):
                    rule = p[2:]
                    if cfgDat.get("cxs", False): rule = cvCxs(rule, pdmFlg=True)
                    cvPts.append(f"p:{rule}")
                elif p.startswith('s:'):
                    rule = p[2:]
                    if cfgDat.get("cxs", False): rule = cvCxs(rule, pdmFlg=True)
                    cvPts.append(f"s:{rule}")
                else:
                    rule = p
                    if cfgDat.get("cxs", False): rule = cvCxs(rule, pdmFlg=True)
                    cvPts.append(rule)
            fnlRl = '*'.join(cvPts)
            
            mtxDat[rNm][cNm] = fnlRl
            
            nwRw = {"tblNm": tNm, "rowNm": rNm, "colNm": cNm, "afxTy": "combined", "mutRl": fnlRl}
            pdmDat.append(nwRw)
            
    svPdm(lngNm, pdmDat)
    print(f"\n{Col.ok}Paradigm saved.{Col.rst}")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def edtPdm(lngNm):
    pdmDat = ldPdm(lngNm)
    if not pdmDat:
        print(f"{Col.err}No paradigms exist.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    clrScr()
    print(f"{Col.hdr}--- Edit Paradigm ---{Col.rst}\n")
    
    tNms = list(dict.fromkeys(p["tblNm"] for p in pdmDat))
    for idx, t in enumerate(tNms):
        print(f"{Col.prm}{idx}.{Col.rst} {t}")
        
    c = input(f"\n{Col.prm}Choose table to edit: {Col.rst}").strip()
    try: tgtTbl = tNms[int(c)]
    except:
        print(f"{Col.err}Invalid choice.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    tblDat = [p for p in pdmDat if p["tblNm"] == tgtTbl]
    rWs = list(dict.fromkeys(p["rowNm"] for p in tblDat))
    cLs = list(dict.fromkeys(p["colNm"] for p in tblDat))
    
    mtxDat = {r: {c: "" for c in cLs} for r in rWs}
    for p in tblDat:
        if p["afxTy"] == "combined" or "p:" in p["mutRl"] or "s:" in p["mutRl"]:
            mtxDat[p["rowNm"]][p["colNm"]] = p['mutRl']
        else:
            mtxDat[p["rowNm"]][p["colNm"]] = f"{p['afxTy'][0]}:{p['mutRl']}"
        
    clrScr()
    print(f"{Col.hdr}--- Editing Table: {tgtTbl} ---{Col.rst}\n")
    
    hdr = f"{'':<8} | " + " | ".join([f"{Col.hdr}{c:^10}{Col.rst}" for c in cLs])
    print(hdr)
    print("-" * (11 + 13 * len(cLs)))
    
    for row in rWs:
        rowStr = f"{Col.hdr}{row:<8}{Col.rst} | " + " | ".join([f"{mtxDat[row][col]:^10}" for col in cLs])
        print(rowStr)
        
    q = input(f"\n{Col.prm}Enter cell tags to edit (e.g. SG1:NOM1 or just SG1): {Col.rst}").strip()
    tLs = q.split(':')
    
    tgt = -1
    for i, p in enumerate(pdmDat):
        if p["tblNm"] == tgtTbl:
            if len(tLs) == 1:
                if (p["rowNm"] == tLs[0] and p["colNm"] == "") or (p["colNm"] == tLs[0] and p["rowNm"] == ""):
                    tgt = i
                    break
            elif len(tLs) >= 2:
                if (p["rowNm"] == tLs[0] and p["colNm"] == tLs[1]) or (p["colNm"] == tLs[0] and p["rowNm"] == tLs[1]):
                    tgt = i
                    break
                    
    if tgt == -1:
        print(f"{Col.err}No matching cell found in this table.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    p = pdmDat[tgt]
    print(f"\n{Col.prm}Editing: {Col.ok}{p['rowNm']}:{p['colNm']}{Col.rst}")
    
    curRl = p['mutRl']
    if p['afxTy'] != 'combined' and 'p:' not in curRl and 's:' not in curRl:
        curRl = f"{p['afxTy'][0]}:{curRl}"
        
    mRl = input(f"{Col.prm}New Mutation Rule (leave blank to keep '{curRl}'): {Col.rst}").strip()
    if mRl:
        cvPts = []
        for pt in mRl.split('*'):
            if pt.startswith('p:'):
                rule = pt[2:]
                if cfgDat.get("cxs", False): rule = cvCxs(rule, pdmFlg=True)
                cvPts.append(f"p:{rule}")
            elif pt.startswith('s:'):
                rule = pt[2:]
                if cfgDat.get("cxs", False): rule = cvCxs(rule, pdmFlg=True)
                cvPts.append(f"s:{rule}")
            else:
                rule = pt
                if cfgDat.get("cxs", False): rule = cvCxs(rule, pdmFlg=True)
                cvPts.append(rule)
        pdmDat[tgt]["mutRl"] = '*'.join(cvPts)
        pdmDat[tgt]["afxTy"] = "combined"
        
    svPdm(lngNm, pdmDat)
    print(f"{Col.ok}Paradigm cell updated.{Col.rst}")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def pdmMnu(lngNm):
    clrScr()
    print(f"{Col.hdr}--- Paradigm Menu ---{Col.rst}\n")
    c = input(f"{Col.prm}(n)ew table or (e)dit cell? {Col.rst}").strip().lower()
    if c == 'n': mkPdm(lngNm)
    elif c == 'e': edtPdm(lngNm)

def aplyMut(bStr, mRl, isSx, isIpa=False):
    if not mRl: return bStr
    lst = getSyms(bStr) if isIpa else list(bStr)
    
    xCt = 0
    while xCt < len(mRl) and mRl[xCt] == '/': xCt += 1
    rMn = mRl[xCt:]
    
    for _ in range(xCt):
        if lst:
            if isSx: lst.pop()
            else: lst.pop(0)
            
    idx = len(lst) if isSx else 0
    rlSy = getSyms(rMn) if isIpa else list(rMn)
    
    isIns = True
    
    for c in rlSy:
        if c == '<':
            idx = max(0, idx - 1)
            isIns = False
        elif c == '>':
            idx = min(len(lst), idx + 1)
            isIns = False
        else:
            if isIns:
                lst.insert(idx, c)
            else:
                if idx == len(lst):
                    lst.append(c)
                else:
                    lst[idx] = c
            idx += 1
            
    return "".join(lst)

def trnSltr(lngNm):
    clrScr()
    csvDat = ldCsv(lngNm)
    pdmDat = ldPdm(lngNm)
    
    print(f"{Col.hdr}--- Translator ({lngNm}) ---{Col.rst}\n")
    gInp = input(f"{Col.prm}Enter gloss sentence (e.g. child-PL see-PAST:1SG): {Col.rst}").strip()
    if not gInp: return
    
    wTks = gInp.split()
    print("\n" + "="*40 + "\n")
    
    fnlOrt = []
    fnlIpa = []
    brkLst = []
    
    for w in wTks:
        prts = re.split(r'[-:]', w)
        rGl = prts[0]
        tLs = prts[1:]
        
        mch = next((r for r in csvDat if r["Gloss"].lower() == rGl.lower() or r["Lemma"].lower() == rGl.lower()), None)
        if not mch:
            fnlOrt.append(f"[{rGl}?]")
            fnlIpa.append(f"[{rGl}?]")
            continue
            
        curOrt = mch["Lemma"]
        curIpa = mch["IPA"]
        brkOrt = curOrt
        
        tTks = re.split(r'([-:])', w)
        glsStr = tTks[0]
        for p in tTks[1:]:
            if p in ['-', ':']: glsStr += p
            else: glsStr += f"{Col.ipa}{p}{Col.rst}"
        
        if tLs:
            rlMch = None
            
            if len(tLs) == 1:
                t = tLs[0]
                for p in pdmDat:
                    if (p["rowNm"] == t and p["colNm"] == "") or (p["colNm"] == t and p["rowNm"] == ""):
                        rlMch = p
                        break
            elif len(tLs) >= 2:
                t1, t2 = tLs[0], tLs[1]
                for p in pdmDat:
                    if (p["rowNm"] == t1 and p["colNm"] == t2) or (p["colNm"] == t1 and p["rowNm"] == t2):
                        rlMch = p
                        break

            if rlMch:
                mRl = rlMch["mutRl"]
                rLst = []
                if "p:" in mRl or "s:" in mRl:
                    for pt in mRl.split('*'):
                        if pt.startswith('p:'): rLst.append((pt[2:], False))
                        elif pt.startswith('s:'): rLst.append((pt[2:], True))
                else:
                    rLst.append((mRl, rlMch["afxTy"] == "suffix"))
                    
                for rl, isSx in rLst:
                    curIpa = aplyMut(curIpa, rl, isSx, True)
                    
                curOrt = getOrt(lngNm, curIpa)
                
                isCmplx = False
                for rl, isSx in rLst:
                    xCt = 0
                    while xCt < len(rl) and rl[xCt] == '/': xCt += 1
                    rMn = rl[xCt:]
                    if '<' in rMn or '>' in rMn or '/' in rl: isCmplx = True
                    
                if not isCmplx:
                    pref = ""
                    suff = ""
                    for rl, isSx in rLst:
                        if isSx: suff += getOrt(lngNm, rl)
                        else: pref += getOrt(lngNm, rl)
                        
                    tmpOrt = curOrt
                    if pref and tmpOrt.startswith(pref): tmpOrt = tmpOrt[len(pref):]
                    if suff and tmpOrt.endswith(suff): tmpOrt = tmpOrt[:-len(suff)]
                    
                    brkOrt = ""
                    if pref: brkOrt += f"{Col.ipa}{pref}{Col.rst}-"
                    brkOrt += tmpOrt
                    if suff: brkOrt += f"-{Col.ipa}{suff}{Col.rst}"
                    
                    if tmpOrt == curOrt and (pref or suff):
                        brkOrt = f"{Col.ipa}{curOrt}{Col.rst}"
                else:
                    brkOrt = f"{Col.ipa}{curOrt}{Col.rst}"
                    
        fnlOrt.append(curOrt)
        fnlIpa.append(curIpa)
        brkLst.append((brkOrt, glsStr))
        
    print(f"{Col.hdr}{' '.join(fnlOrt)}{Col.rst}")
    print(f"{Col.ipa}Pronunciation: /{' '.join(fnlIpa)}/{Col.rst}\n")
    
    print("Breakdown of grammar:")
    for bO, gS in brkLst:
        print(f"  {bO}")
        print(f"  {gS}\n")
        
    input(f"{Col.prm}[Enter] to continue...{Col.rst}")

def addWrd(lngNm):
    clrScr()
    print(f"{Col.hdr}--- Add Word to {lngNm} ---{Col.rst}\n")
    print(f"{Col.prm}(Press Ctrl+C at any time to skip remaining fields and save){Col.rst}\n")
    
    ipa = ""
    gls = ""
    pos = ""
    ety = ""
    nts = ""
    tgs = ""
    rel = ""
    
    try:
        ipa = input(f"{Col.prm}IPA (or CXS): {Col.rst}").strip()
        if cfgDat.get("cxs", False): ipa = cvCxs(ipa)
        
        gls = input(f"{Col.prm}Gloss: {Col.rst}").strip()
        pos = input(f"{Col.prm}PoS: {Col.rst}").strip()
        ety = input(f"{Col.prm}Etymology: {Col.rst}").strip()
        nts = input(f"{Col.prm}Notes: {Col.rst}").strip()
        tgs = input(f"{Col.prm}Tags: {Col.rst}").strip()
        rel = input(f"{Col.prm}Related Words: {Col.rst}").strip()
    except KeyboardInterrupt:
        print(f"\n{Col.hdr}Skipping remaining fields and saving...{Col.rst}")
        
    if not ipa and not gls:
        print(f"\n{Col.err}Aborted. Minimum data (IPA or Gloss) required.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    csvDat = ldCsv(lngNm)
    lem = getOrt(lngNm, ipa)
    csvDat.append({"Lemma": lem, "Gloss": gls, "IPA": ipa, "PoS": pos, "Etymology": ety, "Notes": nts, "Tags": tgs, "Related Words": rel})
    svCsv(lngNm, csvDat)
    
    jf = os.path.join(dirNm, lngNm, f"{lngNm}.json")
    if not os.path.exists(jf):
        print(f"\n{Col.err}No orthography for {lngNm}.{Col.rst}")
        if input(f"{Col.prm}Make one now? (y/n): {Col.rst}").strip().lower() == 'y': 
            mkOrt(lngNm)
            lem = getOrt(lngNm, ipa)
            
    print(f"\n{Col.ok}Added: {Col.hdr}{lem}{Col.rst} (/{Col.ipa}{ipa}{Col.rst}/) - {gls}{Col.rst}")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def srcWrd(lngNm):
    clrScr()
    csvDat = ldCsv(lngNm)
    q = input(f"{Col.prm}Search term: {Col.rst}").strip().lower()
    print()
    resLst = [r for r in csvDat if q in r["Lemma"].lower() or q in r["Gloss"].lower() or q in r["IPA"].lower()]
    if not resLst: print(f"{Col.err}No matches found.{Col.rst}")
    for r in resLst:
        print(f"{Col.hdr}{r['Lemma']}{Col.rst} /{Col.ipa}{r['IPA']}{Col.rst}/ ({Col.prm}{r['PoS']}{Col.rst}) - {Col.ok}{r['Gloss']}{Col.rst} [Ety: {r['Etymology']}]")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def vwWrd(lngNm):
    clrScr()
    csvDat = ldCsv(lngNm)
    if not csvDat:
        print(f"{Col.err}Dictionary is empty.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    print(f"{Col.hdr}Sort by: {Col.rst}1. A-Z | 2. Z-A | 3. Newest Added")
    c = input(f"{Col.prm}Choice (1-3): {Col.rst}").strip()
    
    if c == '1': csvDat.sort(key=lambda x: x["Lemma"].lower())
    elif c == '2': csvDat.sort(key=lambda x: x["Lemma"].lower(), reverse=True)
    elif c == '3': csvDat.reverse()
    
    pg = 0
    while pg * 20 < len(csvDat):
        clrScr()
        print(f"{Col.hdr}--- {lngNm} Dictionary (Page {pg+1}) ---{Col.rst}\n")
        for i in range(pg * 20, min((pg + 1) * 20, len(csvDat))):
            r = csvDat[i]
            print(f"{i+1}. {Col.hdr}{r['Lemma']}{Col.rst} /{Col.ipa}{r['IPA']}{Col.rst}/ ({Col.prm}{r['PoS']}{Col.rst}) - {Col.ok}{r['Gloss']}{Col.rst}")
            
        if (pg + 1) * 20 >= len(csvDat):
            print(f"\n{Col.hdr}End of dictionary.{Col.rst}")
            break
            
        nx = input(f"\n{Col.prm}[Enter] for next page, (q)uit: {Col.rst}").strip().lower()
        if nx == 'q': break
        pg += 1
    if (pg + 1) * 20 >= len(csvDat): input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def edtWrd(lngNm):
    clrScr()
    csvDat = ldCsv(lngNm)
    q = input(f"{Col.prm}Search term to edit: {Col.rst}").strip().lower()
    resLst = [(i, r) for i, r in enumerate(csvDat) if q in r["Lemma"].lower() or q in r["Gloss"].lower() or q in r["IPA"].lower()]
    if not resLst:
        print(f"{Col.err}No matches.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
    print()
    for idx, (i, r) in enumerate(resLst):
        print(f"{Col.prm}{idx}.{Col.rst} {Col.hdr}{r['Lemma']}{Col.rst} /{Col.ipa}{r['IPA']}{Col.rst}/ - {Col.ok}{r['Gloss']}{Col.rst}")
    c = input(f"\n{Col.prm}Choice: {Col.rst}").strip()
    try: tgt = resLst[int(c)][0]
    except:
        print(f"{Col.err}Invalid choice.{Col.rst}")
        return
    
    print(f"\n{Col.hdr}Fields: {Col.rst}1.Gloss 2.IPA 3.PoS 4.Etymology 5.Notes 6.Tags 7.Related Words")
    fC = input(f"{Col.prm}Field (1-7): {Col.rst}").strip()
    flds = {"1":"Gloss", "2":"IPA", "3":"PoS", "4":"Etymology", "5":"Notes", "6":"Tags", "7":"Related Words"}
    if fC not in flds: return
    fldNm = flds[fC]
    
    nwVal = input(f"{Col.prm}New {fldNm}: {Col.rst}").strip()
    if fldNm == "IPA":
        if cfgDat.get("cxs", False): nwVal = cvCxs(nwVal)
        csvDat[tgt]["IPA"] = nwVal
        csvDat[tgt]["Lemma"] = getOrt(lngNm, nwVal)
    else:
        csvDat[tgt][fldNm] = nwVal
        
    svCsv(lngNm, csvDat)
    print(f"{Col.ok}Entry updated.{Col.rst}")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def runLx(lngNm):
    lsc = os.path.join(dirNm, lngNm, f"{lngNm}.lsc")
    if not os.path.exists(lsc):
        csvDat = ldCsv(lngNm)
        symSet = set()
        for r in csvDat:
            for s in getSyms(r["IPA"]):
                if s.strip(): symSet.add(s)
        
        vBase = "aeiouyøœɒɔɛɪʊʌʏəɘɞɜɐɤɵɨʉɯæɑ"
        vLst = []
        cLst = []
        for s in symSet:
            if any(v in s for v in vBase): vLst.append(s)
            else: cLst.append(s)
            
        isCxs = cfgDat.get("cxs", False)
        if isCxs:
            def toCxs(st):
                st = st.replace("͡", "")
                for cxs, ipa in sorted(c2iMap.items(), key=lambda x: -len(x[1])):
                    st = st.replace(ipa, cxs)
                st = st.replace('_', '\\_').replace(':', '\\:').replace(',', '\\,')
                return st
            vLst = [toCxs(s) for s in vLst]
            cLst = [toCxs(s) for s in cLst]

        with open(lsc, "w", encoding="utf-8") as f:
            f.write(f"# {'CXS' if isCxs else 'IPA'}\n")
            if cLst: f.write(f"Class c {{{', '.join(cLst)}}}\n")
            else: f.write("Class c {p, t, k, n, m, r, w, s, j}\n")
            
            if vLst: f.write(f"Class v {{{', '.join(vLst)}}}\n\n")
            else: f.write("Class v {a, e, i, o, u, ə}\n\n")
            
            f.write("v:\n    ə => o\n    e => e / $ _\n    then: e => i / @c _ @c\n")
    
    if platform.system() == "Windows" and platform.release() == "7":
        npp_path = r"C:\Program Files\Notepad++\notepad++.exe"
        npp_x86 = r"C:\Program Files (x86)\Notepad++\notepad++.exe"
        exe_cmd = npp_path if os.path.exists(npp_path) else (npp_x86 if os.path.exists(npp_x86) else "notepad")
        
        print(f"{Col.hdr}Opening {lsc} in Notepad++...{Col.rst}")
        subprocess.run([exe_cmd, lsc])
    else:
        if shutil.which("code"):
            print(f"{Col.hdr}Opening {lsc} in code...{Col.rst}")
            subprocess.run(["code", "--wait", lsc])
        else:
            print(f"{Col.hdr}Opening {lsc} in neovim...{Col.rst}")
            subprocess.run(["nvim", lsc])
    
    with open(lsc, "r", encoding="utf-8") as f:
        lns = f.readlines()
        
    if not lns: return
    ln1 = lns[0].strip()
        
    if ln1 not in ["# CXS", "# IPA"]:
        print(f"{Col.err}Error: The .lsc file must have '# CXS' or '# IPA' on the first line.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    if ln1 == "# CXS":
        lscTxt = "".join(lns[1:])
        lscTxt = cvCxs(lscTxt, lscFlg=True)
        with open(lsc, "w", encoding="utf-8") as f:
            f.write("# IPA\n" + lscTxt)
        print(f"{Col.ok}Converted .lsc file to IPA.{Col.rst}")
    
    if input(f"{Col.prm}Apply changes to {lngNm}.csv? (y/n): {Col.rst}").strip().lower() == 'y':
        csvDat = ldCsv(lngNm)
        inpPth = os.path.join(dirNm, lngNm, "words.wli")
        outPth = os.path.join(dirNm, lngNm, "words_ev.wli")
        wlmPth = os.path.join(dirNm, lngNm, "words_ev.wlm")
        
        with open(inpPth, "w", encoding="utf-8") as f:
            for r in csvDat: f.write(r["IPA"] + "\n")
            
        try:
            lexExe = os.path.join("tools", "lexurgy", "bin", "lexurgy.bat" if os.name == "nt" else "lexurgy")
            subprocess.run([lexExe, "sc", lsc, inpPth], check=True, capture_output=True, text=True)
            with open(outPth, "r", encoding="utf-8") as f: mod = [l.strip() for l in f.readlines() if l.strip()]
            for i, r in enumerate(csvDat):
                if i < len(mod):
                    r["IPA"] = mod[i]
                    r["Lemma"] = getOrt(lngNm, mod[i])
            svCsv(lngNm, csvDat)
            print(f"{Col.ok}Sound changes applied.{Col.rst}")
        except subprocess.CalledProcessError as e:
            print(f"{Col.err}Lexurgy failed:\n{e.stderr}{Col.rst}")
        except Exception as e: print(f"{Col.err}Lexurgy failed: {e}{Col.rst}")
        finally:
            if os.path.exists(inpPth): os.remove(inpPth)
            if os.path.exists(outPth): os.remove(outPth)
            if os.path.exists(wlmPth): os.remove(wlmPth)
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def getDaus(pNm):
    dLst = []
    for dNm in getLs():
        if dNm == pNm: continue
        if getParent(dNm) == pNm:
            dLst.append(dNm)
    return dLst

def applyLx(lngNm, ipaLst):
    lsc = os.path.join(dirNm, lngNm, f"{lngNm}.lsc")
    if not os.path.exists(lsc): return list(ipaLst)
    inpPth = os.path.join(dirNm, lngNm, "sync_in.wli")
    outPth = os.path.join(dirNm, lngNm, "sync_in_ev.wli")
    wlmPth = os.path.join(dirNm, lngNm, "sync_in_ev.wlm")
    resLst = list(ipaLst)
    try:
        with open(inpPth, "w", encoding="utf-8") as f:
            for i in ipaLst: f.write(i + "\n")
        lexExe = os.path.join("tools", "lexurgy", "bin", "lexurgy.bat" if os.name == "nt" else "lexurgy")
        subprocess.run([lexExe, "sc", lsc, inpPth], check=True, capture_output=True, text=True)
        if os.path.exists(outPth):
            with open(outPth, "r", encoding="utf-8") as f:
                mod = [l.strip() for l in f.readlines() if l.strip()]
            for i in range(len(resLst)):
                if i < len(mod): resLst[i] = mod[i]
    except subprocess.CalledProcessError as e: 
        print(f"{Col.err}Lexurgy failed for {lngNm}:\n{e.stderr}{Col.rst}")
    except Exception as e: 
        print(f"{Col.err}Lexurgy failed for {lngNm}: {e}{Col.rst}")
    finally:
        if os.path.exists(inpPth): os.remove(inpPth)
        if os.path.exists(outPth): os.remove(outPth)
        if os.path.exists(wlmPth): os.remove(wlmPth)
    return resLst

def doSync(sNm, sLst, rcsFlg):
    dLst = getDaus(sNm)
    if not dLst: return
    
    for dNm in dLst:
        dDat = ldCsv(dNm)
        nwLst = []
        for w in sLst:
            nwEty = f"Derived from {sNm}: {w['Lemma']} /{w['IPA']}/"
            
            nW = w.copy()
            oldEty = w.get("Etymology", "").strip()
            if oldEty and not oldEty.startswith(f"Derived from {sNm}:"):
                nW["Etymology"] = f"{nwEty} < {oldEty}"
            else:
                nW["Etymology"] = nwEty
                
            nW["Notes"] = ""
            nW["Tags"] = ""
            nW["Related Words"] = ""
            nwLst.append((nW, w["IPA"]))
        
        if nwLst:
            pIpa = [x[1] for x in nwLst]
            evIpa = applyLx(dNm, pIpa)
            
            adLst = []
            for i, (nW, _) in enumerate(nwLst):
                nW["IPA"] = evIpa[i]
                nW["Lemma"] = getOrt(dNm, nW["IPA"])
                
                mch = False
                for dr in dDat:
                    if dr["Gloss"].lower() == nW["Gloss"].lower():
                        dr["IPA"] = nW["IPA"]
                        dr["Lemma"] = nW["Lemma"]
                        dr["Etymology"] = nW["Etymology"]
                        adLst.append(dr)
                        mch = True
                        break
                if not mch:
                    dDat.append(nW)
                    adLst.append(nW)
            
            svCsv(dNm, dDat)
            print(f"{Col.ok}Synced {len(adLst)} words to {dNm}.{Col.rst}")
            
            if rcsFlg:
                doSync(dNm, adLst, True)

def syncWrd(lngNm):
    clrScr()
    csvDat = ldCsv(lngNm)
    c = input(f"{Col.prm}Sync (1) word or (a)ll words? {Col.rst}").strip().lower()
    sncLst = []
    
    if c == '1':
        q = input(f"{Col.prm}Search term: {Col.rst}").strip().lower()
        resLst = [(i, r) for i, r in enumerate(csvDat) if q in r["Lemma"].lower() or q in r["Gloss"].lower() or q in r["IPA"].lower()]
        if not resLst:
            print(f"{Col.err}No matches.{Col.rst}")
            input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
            return
        print()
        for idx, (i, r) in enumerate(resLst):
            print(f"{Col.prm}{idx}.{Col.rst} {Col.hdr}{r['Lemma']}{Col.rst} /{Col.ipa}{r['IPA']}{Col.rst}/ - {Col.ok}{r['Gloss']}{Col.rst}")
        sc = input(f"\n{Col.prm}Choice: {Col.rst}").strip()
        try: sncLst.append(resLst[int(sc)][1])
        except:
            print(f"{Col.err}Invalid.{Col.rst}")
            input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
            return
    elif c == 'a':
        sncLst = csvDat
    else:
        return
        
    if not sncLst: return
        
    rcsChc = input(f"{Col.prm}Sync to (i)mmediate daughters or (r)ecursive? {Col.rst}").strip().lower()
    if rcsChc not in ['i', 'r']: return
    
    print()
    doSync(lngNm, sncLst, rcsChc == 'r')
    print(f"{Col.ok}Sync complete.{Col.rst}")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def mkDau(pNm):
    dNm = mkLng()
    setParent(dNm, pNm)
    pDat = ldCsv(pNm)
    for r in pDat:
        nwEty = f"Derived from {pNm}: {r['Lemma']} /{r['IPA']}/"
        oldEty = r.get("Etymology", "").strip()
        if oldEty and not oldEty.startswith(f"Derived from {pNm}:"):
            r["Etymology"] = f"{nwEty} < {oldEty}"
        else:
            r["Etymology"] = nwEty
        r["Lemma"] = getOrt(dNm, r["IPA"])
    svCsv(dNm, pDat)
    print(f"{Col.ok}Created daughter: {dNm}{Col.rst}")
    if input(f"{Col.prm}Setup sound changes for {dNm}? (y/n): {Col.rst}").strip().lower() == 'y': runLx(dNm)

def cmpLng():
    ls = getLs()
    if len(ls) < 2:
        print(f"{Col.err}Need at least 2 languages to compare.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
    
    clrScr()
    print(f"{Col.hdr}--- Compare Languages ---{Col.rst}\n")
    for i, l in enumerate(ls): print(f"{Col.prm}{i+1}.{Col.rst} {l}")
    
    try:
        i1 = int(input(f"\n{Col.prm}First language number: {Col.rst}")) - 1
        i2 = int(input(f"{Col.prm}Second language number: {Col.rst}")) - 1
        l1, l2 = ls[i1], ls[i2]
    except:
        print(f"{Col.err}Invalid choice.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return

    d1 = ldCsv(l1)
    d2 = ldCsv(l2)
    
    mchLst = []
    for w1 in d1:
        for w2 in d2:
            if w1["Gloss"].lower() == w2["Gloss"].lower():
                mchLst.append((w1, w2, w1["Gloss"]))
                
    mchLst.sort(key=lambda x: x[2].lower())
    
    if not mchLst:
        print(f"{Col.err}No matching glosses found.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    pg = 0
    while pg * 10 < len(mchLst):
        clrScr()
        print(f"{Col.hdr}--- Comparing {l1} & {l2} (Page {pg+1}) ---{Col.rst}\n")
        
        print(f"{Col.hdr}{l1:<25} | {l2:<25} | Gloss{Col.rst}")
        print("-" * 70)
        
        for i in range(pg * 10, min((pg + 1) * 10, len(mchLst))):
            w1, w2, gls = mchLst[i]
            s1 = f"{w1['Lemma']} /{w1['IPA']}/"
            s2 = f"{w2['Lemma']} /{w2['IPA']}/"
            print(f"{Col.ok}{s1:<25}{Col.rst} | {Col.prm}{s2:<25}{Col.rst} | {gls}")
            
        if (pg + 1) * 10 >= len(mchLst):
            print(f"\n{Col.hdr}End of comparison.{Col.rst}")
            break
            
        nx = input(f"\n{Col.prm}[Enter] for next page, (q)uit: {Col.rst}").strip().lower()
        if nx == 'q': break
        pg += 1
        
    if (pg + 1) * 10 >= len(mchLst): input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def vwTree():
    clrScr()
    print(f"{Col.hdr}--- Language Family Tree ---{Col.rst}\n")
    ls = getLs()
    
    roots = [l for l in ls if not getParent(l)]
    
    def prtTr(node, ind=""):
        print(f"{ind}- {Col.ok}{node}{Col.rst}")
        daus = getDaus(node)
        for d in daus:
            prtTr(d, ind + "  ")
            
    if not roots:
        print(f"{Col.err}No languages found.{Col.rst}")
    else:
        for r in roots:
            prtTr(r)
            print()
            
    input(f"{Col.prm}[Enter] to continue...{Col.rst}")

def evlWrdTr(lngNm):
    clrScr()
    print(f"{Col.hdr}--- Evolve Word Tree ({lngNm}) ---{Col.rst}\n")
    c = input(f"{Col.prm}Use (1) Dictionary word or (2) Custom word? {Col.rst}").strip()
    ipa = ""
    
    if c == '1':
        q = input(f"{Col.prm}Search term: {Col.rst}").strip().lower()
        csvDat = ldCsv(lngNm)
        resLst = [(i, r) for i, r in enumerate(csvDat) if q in r["Lemma"].lower() or q in r["Gloss"].lower() or q in r["IPA"].lower()]
        if not resLst:
            print(f"{Col.err}No matches.{Col.rst}")
            input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
            return
        print()
        for idx, (i, r) in enumerate(resLst):
            print(f"{Col.prm}{idx}.{Col.rst} {Col.hdr}{r['Lemma']}{Col.rst} /{Col.ipa}{r['IPA']}{Col.rst}/ - {Col.ok}{r['Gloss']}{Col.rst}")
        sc = input(f"\n{Col.prm}Choice: {Col.rst}").strip()
        try: 
            ipa = resLst[int(sc)][1]["IPA"]
        except:
            print(f"{Col.err}Invalid.{Col.rst}")
            input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
            return
    elif c == '2':
        ipa = input(f"{Col.prm}Enter IPA (or CXS): {Col.rst}").strip()
        if cfgDat.get("cxs", False): ipa = cvCxs(ipa)
    else:
        return
        
    if not ipa: return
    
    showIpa = input(f"{Col.prm}Show IPA in tree? (y/n): {Col.rst}").strip().lower() == 'y'

    print("\n" + "="*40 + "\n")
    
    def prtWrdTr(nLng, nIpa, pref="", isLst=True):
        nOrt = getOrt(nLng, nIpa)
        dispStr = f"{nOrt}"
        if showIpa:
            dispStr += f" /{Col.ipa}{nIpa}{Col.rst}/"

        if pref == "":
            print(f"{Col.hdr}*{dispStr}{Col.rst}")
            cPref = "    "
        else:
            mkr = "└── " if isLst else "├── "
            print(f"{pref}{mkr}{Col.hdr}{dispStr}{Col.rst}")
            cPref = pref + ("    " if isLst else "│   ")
            
        daus = getDaus(nLng)
        for i, d in enumerate(daus):
            evIpa = applyLx(d, [nIpa])[0]
            isLChld = (i == len(daus) - 1)
            prtWrdTr(d, evIpa, cPref, isLChld)
            
    prtWrdTr(lngNm, ipa)
    print("\n" + "="*40 + "\n")
    input(f"{Col.prm}[Enter] to continue...{Col.rst}")

def wrkSpc(lngNm):
    while True:
        clrScr()
        print(f"{Col.hdr}=== Workspace: {lngNm} ==={Col.rst}\n")
        mnuChc = input(f"{Col.prm}(a)dd, (e)dit, (s)earch, (v)iew, s(y)nc, (o)rtho, (l)exurgy, (p)aradigm, (t)ranslate, (w)ord tree, (c)onfig, (b)ack: {Col.rst}").strip().lower()
        if mnuChc == 'a': addWrd(lngNm)
        elif mnuChc == 'e': edtWrd(lngNm)
        elif mnuChc == 's': srcWrd(lngNm)
        elif mnuChc == 'v': vwWrd(lngNm)
        elif mnuChc == 'y': syncWrd(lngNm)
        elif mnuChc == 'o': mkOrt(lngNm)
        elif mnuChc == 'l': runLx(lngNm)
        elif mnuChc == 'p': pdmMnu(lngNm)
        elif mnuChc == 't': trnSltr(lngNm)
        elif mnuChc == 'w': evlWrdTr(lngNm)
        elif mnuChc == 'c': setMnu()
        elif mnuChc == 'b': break

def mnApp():
    iniApp()
    while True:
        clrScr()
        ls = getLs()
        if not ls:
            print(f"{Col.hdr}No languages found.{Col.rst}")
            mkLng()
            continue
            
        print(f"{Col.hdr}=== Languages ==={Col.rst}\n")
        for i, l in enumerate(ls): print(f"{Col.prm}{i+1}.{Col.rst} {l}")
        
        c = input(f"\n{Col.prm}Choose number, (n)ew, (d)aughter, co(m)pare, (t)ree, (c)onfig, or (q)uit: {Col.rst}").strip().lower()
        if c == 'q': break
        elif c == 'n': mkLng()
        elif c == 'c': setMnu()
        elif c == 'm': cmpLng()
        elif c == 't': vwTree()
        elif c == 'd':
            try:
                idx = int(input(f"{Col.prm}Parent number: {Col.rst}")) - 1
                mkDau(ls[idx])
            except:
                print(f"{Col.err}Invalid choice.{Col.rst}")
                input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        else:
            try: wrkSpc(ls[int(c)-1])
            except: 
                print(f"{Col.err}Invalid choice.{Col.rst}")
                input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

if __name__ == "__main__": mnApp()
