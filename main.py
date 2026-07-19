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
    "genWrd": "Generate Word",
    "genStl": "Generate Settlement Name",
    "chkSwd": "Check Swadesh List",
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
    "renLng": "Rename Language",
    "delLng": "Delete Language",
    "lonWrd": "Loan Word",
    "vwCht": "View Chart",
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
    "d`": "ɖ", "l`": "ɭ", "n`": "ɳ", "r`": "ɽ", "s`": "ʂ", "t`": "ʈ", "z`": "ʐ",
    "J\\": "ɟ", "K\\": "ɮ", "G\\": "ɢ", "N\\": "ɴ", "X\\": "ħ",
    "R\\": "ʀ", "H\\": "ʜ", "?": "ʔ", "O\\": "ʘ", "r\\`": "ɻ",
    "L\\": "ʟ", "M\\": "ɰ", "~": "̃", ":": "ː", ":\\": "ˑ", "=": "̩",
    "_j": "ʲ", "_w": "ʷ", "_h": "ʰ", "_n": "ⁿ", "_l": "ˡ", "_~": "̃",
    "_T": "̋", "_H": "́", "_M": "̄", "_L": "̀", "_B": "̏", "_R": "̌", "_F": "̂",
    "_>": "ʼ"
}

swadeshLst = [
    "I", "you", "we", "this", "that", "who", "what", "not", "all", "many", "one", "two", "big", "long", "small",
    "woman", "man", "person", "fish", "bird", "dog", "louse", "tree", "seed", "leaf", "root", "bark", "skin",
    "flesh", "blood", "bone", "grease", "egg", "horn", "tail", "feather", "hair", "head", "ear", "eye", "nose",
    "mouth", "tooth", "tongue", "fingernail", "foot", "knee", "hand", "belly", "neck", "breasts", "heart", "liver",
    "drink", "eat", "bite", "see", "hear", "know", "sleep", "die", "kill", "swim", "fly", "walk", "come", "lie",
    "sit", "stand", "give", "say", "sun", "moon", "star", "water", "rain", "stone", "sand", "earth", "cloud",
    "smoke", "fire", "ashes", "burn", "path", "mountain", "red", "green", "yellow", "white", "black", "night",
    "hot", "cold", "full", "new", "good", "bad", "round", "dry", "name", "three", "four", "five", "child",
    "husband", "wife", "mother", "father", "animal", "snake", "worm", "fruit", "grass", "rope", "salt", "claw",
    "leg", "suck", "spit", "vomit", "blow", "breathe", "laugh", "think", "smell", "fear", "live", "fight",
    "hunt", "hit", "cut", "split", "stab", "scratch", "dig", "turn", "fall", "hold", "squeeze", "rub", "wash",
    "wipe", "pull", "push", "throw", "tie", "sew", "sing", "play", "float", "flow", "freeze", "swell", "river",
    "lake", "sea", "dust", "fog", "sky", "wind", "snow", "ice", "road", "day", "year", "warm", "old", "rotten",
    "dirty", "straight", "sharp", "dull", "smooth", "wet", "correct", "near", "far", "right", "left", "at",
    "in", "with", "and", "if", "because"
]

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
            if nxt in "ːˑʰʷʲⁿˡ̩̃ʼ" or ('\u0300' <= nxt <= '\u036F'):
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
    
    with open(jf, "w", encoding="utf-8") as f: json.dump(ortDat, f, indent=2, ensure_ascii=False)
    
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

def vwCht(lngNm):
    clrScr()
    jf = os.path.join(dirNm, lngNm, f"{lngNm}.json")
    if not os.path.exists(jf):
        print(f"{Col.err}No orthography data found for {lngNm}. Please create an orthography first.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    with open(jf, "r", encoding="utf-8") as f:
        ortDat = json.load(f)
        
    vBase = "aeiouyøœɒɔɛɪʊʌʏəɘɞɜɐɤɵɨʉɯæɑ"
    vLst = []
    cLst = []
    
    for ipa, ort in ortDat.items():
        if any(v in ipa for v in vBase):
            vLst.append((ipa, ort))
        else:
            cLst.append((ipa, ort))
            
    print(f"{Col.hdr}--- {lngNm} Orthography & IPA Chart ---{Col.rst}\n")
    
    print(f"{Col.hdr}Consonants:{Col.rst}")
    print("-" * 30)
    for ipa, ort in sorted(cLst, key=lambda x: x[0]):
        print(f" /{Col.ipa}{ipa:<5}{Col.rst}/ -> {Col.ok}{ort}{Col.rst}")
        
    print(f"\n{Col.hdr}Vowels:{Col.rst}")
    print("-" * 30)
    for ipa, ort in sorted(vLst, key=lambda x: x[0]):
        print(f" /{Col.ipa}{ipa:<5}{Col.rst}/ -> {Col.ok}{ort}{Col.rst}")
        
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

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
    print(f"\n{Col.hdr}--- Editing Table: {tgtTbl} ---{Col.rst}\n")
    
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

def addWrd(lngNm, args=None):
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
    
    if args:
        ipa = args[0]
        if len(args) > 1: gls = args[1]
        if len(args) > 2: pos = " ".join(args[2:])
    
    try:
        if not ipa:
            ipa = input(f"{Col.prm}IPA (or CXS): {Col.rst}").strip()
        else:
            print(f"{Col.prm}IPA (or CXS): {Col.rst}{ipa}")
            
        if cfgDat.get("cxs", False): ipa = cvCxs(ipa)
        
        if not gls:
            gls = input(f"{Col.prm}Gloss: {Col.rst}").strip()
        else:
            print(f"{Col.prm}Gloss: {Col.rst}{gls}")
            
        if not pos:
            pos = input(f"{Col.prm}PoS: {Col.rst}").strip()
        else:
            print(f"{Col.prm}PoS: {Col.rst}{pos}")
            
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

def genWrd(lngNm):
    def_name = lngNm.replace(" ", "-").lower()
    tmp_file = os.path.join(dirNm, lngNm, "lexifer_tmp.txt")
    lex_script = os.path.join("tools", "lexifer", "lexifer.py")
    def_file = f"{def_name}.def"
    
    def runLexifer():
        cwd = os.path.join("tools", "lexifer")
        try:
            res = subprocess.run([sys.executable, "lexifer.py", def_file], cwd=cwd, capture_output=True, text=True, check=True)
            return res.stdout
        except subprocess.CalledProcessError as e:
            return f"{Col.err}Lexifer Error:\n{e.stderr}{Col.rst}"
        except Exception as e:
            return f"{Col.err}Failed to run Lexifer: {e}{Col.rst}"
            
    if not os.path.exists(tmp_file):
        out_text = runLexifer()
        with open(tmp_file, "w", encoding="utf-8") as f: f.write(out_text)
        
    while True:
        clrScr()
        print(f"{Col.hdr}--- Generate Words for {lngNm} ---{Col.rst}\n")
        
        if os.path.exists(tmp_file):
            with open(tmp_file, "r", encoding="utf-8") as f:
                out_text = f.read()
            print(f"{Col.prm}Lexifer Output:{Col.rst}\n{out_text}\n")
            
        print(f"{Col.prm}(Type '/rg' in IPA to regenerate, or Press Ctrl+C to skip remaining fields and save){Col.rst}\n")
        
        ipa = ""
        gls = ""
        pos = ""
        ety = ""
        nts = ""
        tgs = ""
        rel = ""
        
        try:
            ipa = input(f"{Col.prm}IPA (or CXS): {Col.rst}").strip()
            if ipa == "/rg":
                out_text = runLexifer()
                with open(tmp_file, "w", encoding="utf-8") as f: f.write(out_text)
                continue
            
            if not ipa:
                print(f"\n{Col.err}Aborted. Minimum data (IPA or Gloss) required.{Col.rst}")
            else:
                if cfgDat.get("cxs", False): ipa = cvCxs(ipa)
                
                gls = input(f"{Col.prm}Gloss: {Col.rst}").strip()
                pos = input(f"{Col.prm}PoS: {Col.rst}").strip()
                ety = input(f"{Col.prm}Etymology: {Col.rst}").strip()
                nts = input(f"{Col.prm}Notes: {Col.rst}").strip()
                tgs = input(f"{Col.prm}Tags: {Col.rst}").strip()
                rel = input(f"{Col.prm}Related Words: {Col.rst}").strip()
        except KeyboardInterrupt:
            print(f"\n{Col.hdr}Skipping remaining fields and saving...{Col.rst}")
            
        if ipa or gls:
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
            
        c = input(f"\n{Col.prm}Add another word from this list? (y/n): {Col.rst}").strip().lower()
        if c != 'y':
            break

def genStl(lngNm):
    clrScr()
    csvDat = ldCsv(lngNm)
    if not csvDat:
        print(f"{Col.err}Dictionary is empty.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return

    bGl = ["town", "city", "village", "settlement", "fort", "castle", "port", "haven", "house", "home", "mouth", "valley", "hill", "mountain", "field"]
    mGl = ["new", "old", "big", "great", "small", "high", "low", "stone", "rock", "water", "river", "lake", "forest", "wood", "black", "white", "red", "cold", "hot"]

    misB = [g for g in bGl if not any(g in r["Gloss"].lower() for r in csvDat)]
    misM = [g for g in mGl if not any(g in r["Gloss"].lower() for r in csvDat)]

    if misB or misM:
        print(f"{Col.hdr}=== Settlement Component Recommendations ==={Col.rst}\n")
        if misB: print(f"Missing bases     : {Col.ipa}{', '.join(misB)}{Col.rst}")
        if misM: print(f"Missing modifiers : {Col.ipa}{', '.join(misM)}{Col.rst}")
        
        ans = input(f"\n{Col.prm}Would you like to generate/add missing words? (y/n): {Col.rst}").strip().lower()
        if ans == 'y':
            def_name = lngNm.replace(" ", "-").lower()
            def_file = os.path.join("tools", "lexifer", f"{def_name}.def")
            has_lex = os.path.exists(def_file)
            cands = []
            if has_lex:
                try:
                    cwd = os.path.join("tools", "lexifer")
                    res = subprocess.run([sys.executable, "lexifer.py", f"{def_name}.def"], cwd=cwd, capture_output=True, text=True, check=True)
                    cands = [w.strip() for l in res.stdout.split('\n') for w in [l.strip()] if w and not w.startswith('#')][:25]
                except Exception as e:
                    print(f"{Col.err}Lexifer run error: {e}{Col.rst}")
            
            for g in (misB + misM):
                clrScr()
                pos = "noun" if g in misB else "adjective"
                print(f"{Col.hdr}--- Creating Word for: {Col.ok}{g}{Col.rst} ({Col.prm}{pos}{Col.rst}) ---{Col.rst}\n")
                if cands:
                    print(f"{Col.hdr}Lexifer suggestions:{Col.rst}")
                    for idx, c in enumerate(cands[:10]):
                        print(f"  {Col.prm}{idx+1}.{Col.rst} {Col.ipa}{c}{Col.rst}")
                    print()
                
                wh = input(f"{Col.prm}Enter IPA (or choice #, or blank to skip): {Col.rst}").strip()
                if not wh: continue
                
                if wh.isdigit() and cands and 1 <= int(wh) <= min(len(cands), 10):
                    ipa = cands[int(wh)-1]
                else:
                    ipa = wh
                
                if cfgDat.get("cxs", False): ipa = cvCxs(ipa)
                lem = getOrt(lngNm, ipa)
                
                csvDat.append({
                    "Lemma": lem, "Gloss": g, "IPA": ipa, "PoS": pos,
                    "Etymology": "", "Notes": "Settlement generator component",
                    "Tags": "settlement-suggested", "Related Words": ""
                })
                svCsv(lngNm, csvDat)
                print(f"\n{Col.ok}Saved: {Col.hdr}{lem}{Col.rst} (/{Col.ipa}{ipa}{Col.rst}/) as '{g}'.{Col.rst}")
                if ipa in cands: cands.remove(ipa)
                input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
            csvDat = ldCsv(lngNm)

    clrScr()
    bLst = [r for r in csvDat if any(g in r["Gloss"].lower() for g in bGl)]
    mLst = [r for r in csvDat if any(g in r["Gloss"].lower() for g in mGl)]

    print(f"{Col.hdr}--- Settlement Name Generator ---{Col.rst}\n")
    print(f"Found {Col.ok}{len(bLst)}{Col.rst} base words and {Col.ok}{len(mLst)}{Col.rst} modifier words.\n")

    if not bLst or not mLst:
        print(f"{Col.err}Insufficient vocabulary. Falling back to all nouns/adjectives...{Col.rst}")
        bLst = [r for r in csvDat if r["PoS"].lower() in ["n", "noun", "proper noun"]]
        mLst = [r for r in csvDat if r["PoS"].lower() in ["adj", "adjective", "n", "noun"]]

    if not bLst or not mLst:
        print(f"{Col.err}Still not enough words.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return

    print(f"Choose order:")
    print(f"  {Col.prm}1.{Col.rst} Modifier + Base")
    print(f"  {Col.prm}2.{Col.rst} Base + Modifier")
    ordChc = input(f"\n{Col.prm}Choice (1-2): {Col.rst}").strip()
    
    lnk = input(f"{Col.prm}Compounding linker vowel (optional): {Col.rst}").strip()
    if cfgDat.get("cxs", False) and lnk: lnk = cvCxs(lnk)
    
    ctInp = input(f"{Col.prm}How many names to generate? (default 10): {Col.rst}").strip()
    ct = int(ctInp) if ctInp.isdigit() else 10

    import random
    print(f"\n{Col.hdr}--- Generated Settlements ---{Col.rst}\n")
    resLst = []
    for _ in range(ct):
        b = random.choice(bLst)
        m = random.choice(mLst)
        
        if ordChc == '2':
            ipa = b["IPA"] + lnk + m["IPA"]
            gls = f"{b['Gloss'].capitalize()}-{m['Gloss']}"
        else:
            ipa = m["IPA"] + lnk + b["IPA"]
            gls = f"{m['Gloss'].capitalize()}-{b['Gloss']}"
            
        ipa = ipa.replace(" ", "")
        lem = getOrt(lngNm, ipa)
        resLst.append((lem, ipa, gls))
        print(f"  {Col.ok}{lem:<18}{Col.rst} /{Col.ipa}{ipa:<15}{Col.rst}/ ({gls})")

    print(f"\n{Col.prm}Save any of these to your dictionary?{Col.rst}")
    svNm = input(f"{Col.prm}Enter name to save (or press Enter to skip): {Col.rst}").strip()
    if svNm:
        mch = next((r for r in resLst if r[0].lower() == svNm.lower()), None)
        if mch:
            csvDat.append({
                "Lemma": mch[0], "Gloss": f"Place name ({mch[2]})", "IPA": mch[1],
                "PoS": "proper noun", "Etymology": f"Compound of {mch[2].lower()}",
                "Notes": "Settlement generator", "Tags": "settlement, place", "Related Words": ""
            })
            svCsv(lngNm, csvDat)
            print(f"{Col.ok}Saved {mch[0]} to dictionary.{Col.rst}")
            
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def chkSwd(lngNm):
    clrScr()
    csvDat = ldCsv(lngNm)
    
    hasGls = {r["Gloss"].lower() for r in csvDat}
    misS = [g for g in swadeshLst if g.lower() not in hasGls]
    
    total = len(swadeshLst)
    found = total - len(misS)
    
    print(f"{Col.hdr}=== Swadesh 200 List Explorer: {lngNm} ==={Col.rst}\n")
    print(f"Vocabulary status: {Col.ok}{found}/{total}{Col.rst} Swadesh words found. ({Col.err}{len(misS)}{Col.rst} missing)\n")
    
    if not misS:
        print(f"{Col.ok}Congratulations! You have completed the Swadesh 200 vocabulary!{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    ans = input(f"\n{Col.prm}Would you like to generate/add missing words? (y/n): {Col.rst}").strip().lower()
    if ans == 'y':
        def_name = lngNm.replace(" ", "-").lower()
        def_file = os.path.join("tools", "lexifer", f"{def_name}.def")
        has_lex = os.path.exists(def_file)
        cands = []
        if has_lex:
            try:
                cwd = os.path.join("tools", "lexifer")
                res = subprocess.run([sys.executable, "lexifer.py", f"{def_name}.def"], cwd=cwd, capture_output=True, text=True, check=True)
                cands = [w.strip() for l in res.stdout.split('\n') for w in [l.strip()] if w and not w.startswith('#')][:100]
            except Exception as e:
                print(f"{Col.err}Lexifer run error: {e}{Col.rst}")
        
        for g in misS:
            clrScr()
            print(f"{Col.hdr}--- Creating Swadesh Word for: {Col.ok}{g}{Col.rst} ---{Col.rst}\n")
            if cands:
                print(f"{Col.hdr}Lexifer suggestions:{Col.rst}")
                for idx, c in enumerate(cands[:10]):
                    print(f"  {Col.prm}{idx+1}.{Col.rst} {Col.ipa}{c}{Col.rst}")
                print()
            
            wh = input(f"{Col.prm}Enter IPA/CXS (or choice #, or blank to skip, 'q' to abort): {Col.rst}").strip()
            if wh.lower() == 'q':
                break
            if not wh: continue
            
            if wh.isdigit() and cands and 1 <= int(wh) <= min(len(cands), 10):
                ipa = cands[int(wh)-1]
            else:
                ipa = wh
            
            if cfgDat.get("cxs", False): ipa = cvCxs(ipa)
            lem = getOrt(lngNm, ipa)
            
            csvDat.append({
                "Lemma": lem, "Gloss": g, "IPA": ipa, "PoS": "swadesh",
                "Etymology": "", "Notes": "Swadesh List Vocab",
                "Tags": "swadesh", "Related Words": ""
            })
            svCsv(lngNm, csvDat)
            print(f"\n{Col.ok}Saved: {Col.hdr}{lem}{Col.rst} (/{Col.ipa}{ipa}{Col.rst}/) as '{g}'.{Col.rst}")
            if ipa in cands: cands.remove(ipa)
            input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def srcWrd(lngNm, args=None):
    clrScr()
    csvDat = ldCsv(lngNm)
    
    if not args:
        print(f"{Col.hdr}--- Recent Words ---{Col.rst}\n")
        revDat = list(reversed(csvDat))
        for r in revDat[:20]:
            print(f"{Col.hdr}{r['Lemma']}{Col.rst} /{Col.ipa}{r['IPA']}{Col.rst}/ ({Col.prm}{r['PoS']}{Col.rst}) - {Col.ok}{r['Gloss']}{Col.rst}")
        q = input(f"\n{Col.prm}Search term: {Col.rst}").strip().lower()
    else:
        q = " ".join(args).lower()
        
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

def edtWrd(lngNm, args=None):
    clrScr()
    csvDat = ldCsv(lngNm)
    
    if not args:
        print(f"{Col.hdr}--- Recent Words ---{Col.rst}\n")
        revDat = list(reversed(csvDat))
        for r in revDat[:20]:
            print(f"{Col.hdr}{r['Lemma']}{Col.rst} /{Col.ipa}{r['IPA']}{Col.rst}/ - {Col.ok}{r['Gloss']}{Col.rst}")
        q = input(f"\n{Col.prm}Search term to edit: {Col.rst}").strip().lower()
    else:
        q = " ".join(args).lower()
        
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
        print(f"{Col.hdr}Would you like to run Lexurgy in CXS mode or IPA mode (1: CXS, 2: IPA)?\n")
        inp = input().strip()
        if inp in ['1']:
            if isCxs:
                def toCxs(st):
                    st = st.replace("͡", "")
                    for cxs, ipa in sorted(c2iMap.items(), key=lambda x: -len(x[1])):
                        st = st.replace(ipa, cxs)
                    st = st.replace('_', '\\_').replace(':', '\\:').replace(',', '\\,')
                    return st
                vLst = [toCxs(s) for s in vLst]
                cLst = [toCxs(s) for s in cLst]
        elif inp in ['2']:
            setMnu()

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
        print(f"{Col.hdr}Would you like to open kate, micro, or neovim? (k, m, n){Col.rst}")
        chcIdx = input().strip()
        if chcIdx in ['k', 'K']:
            subprocess.run(["kate", lsc])
        elif chcIdx in ['m', 'M']:
            subprocess.run(["micro", lsc])
        elif chcIdx in ['n', 'N']:
            subprocess.run(["nvim", lsc])
        else:
            print(f"{Col.err}Invalid.{Col.rst}")
            print(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
            return
    
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
    
    while True:
        ans = input(f"{Col.prm}Apply changes to {lngNm}.csv? (y: yes, n: no, p: preview): {Col.rst}").strip().lower()
        if ans == 'y':
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
                msg = []
                if e.stdout and e.stdout.strip():
                    msg.append(f"Stdout:\n{e.stdout.strip()}")
                if e.stderr and e.stderr.strip():
                    msg.append(f"Stderr:\n{e.stderr.strip()}")
                err_details = "\n\n".join(msg) if msg else "No output details available."
                print(f"{Col.err}Lexurgy failed:\n{err_details}{Col.rst}")
            except Exception as e: print(f"{Col.err}Lexurgy failed: {e}{Col.rst}")
            finally:
                if os.path.exists(inpPth): os.remove(inpPth)
                if os.path.exists(outPth): os.remove(outPth)
                if os.path.exists(wlmPth): os.remove(wlmPth)
            input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
            break
        elif ans == 'p':
            csvDat = ldCsv(lngNm)
            if not csvDat:
                print(f"{Col.err}Vocabulary is empty. Nothing to preview.{Col.rst}")
                continue
            inpPth = os.path.join(dirNm, lngNm, "words.wli")
            outPth = os.path.join(dirNm, lngNm, "words_ev.wli")
            wlmPth = os.path.join(dirNm, lngNm, "words_ev.wlm")
            
            with open(inpPth, "w", encoding="utf-8") as f:
                for r in csvDat: f.write(r["IPA"] + "\n")
                
            try:
                lexExe = os.path.join("tools", "lexurgy", "bin", "lexurgy.bat" if os.name == "nt" else "lexurgy")
                subprocess.run([lexExe, "sc", lsc, inpPth], check=True, capture_output=True, text=True)
                with open(outPth, "r", encoding="utf-8") as f: mod = [l.strip() for l in f.readlines() if l.strip()]
                
                print(f"\n{Col.hdr}--- Preview of Lexurgy Sound Changes ---{Col.rst}")
                changed_count = 0
                for i, r in enumerate(csvDat):
                    if i < len(mod):
                        new_ipa = mod[i]
                        new_lemma = getOrt(lngNm, new_ipa)
                        if r["IPA"] != new_ipa or r["Lemma"] != new_lemma:
                            print(f"  {Col.hdr}{r['Lemma']}{Col.rst} > {Col.ok}{new_lemma}{Col.rst} (/{Col.ipa}{r['IPA']}{Col.rst}/ > /{Col.ipa}{new_ipa}{Col.rst}/)")
                            changed_count += 1
                if changed_count == 0:
                    print(f"  {Col.ok}No words in the vocabulary would change.{Col.rst}")
                else:
                    print(f"\nTotal changed: {Col.ok}{changed_count}{Col.rst} word(s).")
                print()
            except subprocess.CalledProcessError as e:
                msg = []
                if e.stdout and e.stdout.strip():
                    msg.append(f"Stdout:\n{e.stdout.strip()}")
                if e.stderr and e.stderr.strip():
                    msg.append(f"Stderr:\n{e.stderr.strip()}")
                err_details = "\n\n".join(msg) if msg else "No output details available."
                print(f"{Col.err}Lexurgy failed:\n{err_details}{Col.rst}")
            except Exception as e: print(f"{Col.err}Lexurgy failed: {e}{Col.rst}")
            finally:
                if os.path.exists(inpPth): os.remove(inpPth)
                if os.path.exists(outPth): os.remove(outPth)
                if os.path.exists(wlmPth): os.remove(wlmPth)
        elif ans == 'n':
            print(f"{Col.ok}Changes discarded.{Col.rst}")
            input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
            break
        else:
            print(f"{Col.err}Invalid choice. Please enter 'y', 'n', or 'p'.{Col.rst}")

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
        msg = []
        if e.stdout and e.stdout.strip():
            msg.append(f"Stdout:\n{e.stdout.strip()}")
        if e.stderr and e.stderr.strip():
            msg.append(f"Stderr:\n{e.stderr.strip()}")
        err_details = "\n\n".join(msg) if msg else "No output details available."
        print(f"{Col.err}Lexurgy failed for {lngNm}:\n{err_details}{Col.rst}")
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

def syncWrd(lngNm, args=None):
    clrScr()
    csvDat = ldCsv(lngNm)
    c = ""
    sncLst = []
    
    if args and len(args) > 0:
        c = args[0].lower()
    else:
        c = input(f"{Col.prm}Sync (1) word or (a)ll words? {Col.rst}").strip().lower()
        
    if c in ['1', 'one']:
        if args and len(args) > 1:
            q = " ".join(args[1:]).lower()
        else:
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
    elif c in ['a', 'all']:
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

def cmpLng(l1Nm=None, l2Nm=None):
    ls = getLs()
    if len(ls) < 2:
        print(f"{Col.err}Need at least 2 languages to compare.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    if not l1Nm or not l2Nm:
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
    else:
        l1, l2 = l1Nm, l2Nm

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
            
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

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

def delLng(lngNm):
    clrScr()
    ans = input(f"{Col.err}Are you sure you want to permanently delete '{lngNm}' and all its files? (y/n): {Col.rst}").strip().lower()
    if ans == 'y':
        shutil.rmtree(os.path.join(dirNm, lngNm))
        print(f"{Col.ok}Deleted {lngNm}.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def renLng(lngNm):
    clrScr()
    newNm = input(f"{Col.prm}Enter new name for '{lngNm}': {Col.rst}").strip()
    if not newNm or newNm == lngNm: return
    
    p = os.path.join(dirNm, lngNm)
    newP = os.path.join(dirNm, newNm)
    
    if os.path.exists(newP):
        print(f"{Col.err}A language named '{newNm}' already exists.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    exts = [".csv", ".json", ".lsc", ".txt"]
    for ext in exts:
        oldF = os.path.join(p, f"{lngNm}{ext}")
        newF = os.path.join(p, f"{newNm}{ext}")
        if os.path.exists(oldF):
            os.rename(oldF, newF)
            
    os.rename(p, newP)
    
    for d in os.listdir(dirNm):
        dp = os.path.join(dirNm, d)
        if os.path.isdir(dp) and d != newNm:
            pTxt = os.path.join(dp, "parent.txt")
            if os.path.exists(pTxt):
                with open(pTxt, "r", encoding="utf-8") as f:
                    currP = f.read().strip()
                if currP == lngNm:
                    with open(pTxt, "w", encoding="utf-8") as f:
                        f.write(newNm)
            
            csvF = os.path.join(dp, f"{d}.csv")
            if os.path.exists(csvF):
                with open(csvF, "r", encoding="utf-8") as f:
                    rows = list(csv.DictReader(f))
                chg = False
                for r in rows:
                    ety = r.get("Etymology", "")
                    if f"Derived from {lngNm}:" in ety:
                        r["Etymology"] = ety.replace(f"Derived from {lngNm}:", f"Derived from {newNm}:")
                        chg = True
                if chg:
                    with open(csvF, "w", newline="", encoding="utf-8") as f:
                        w = csv.DictWriter(f, fieldnames=hdrLst)
                        w.writeheader()
                        w.writerows(rows)
    
    print(f"{Col.ok}Renamed '{lngNm}' to '{newNm}'.{Col.rst}")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def lonWrd(lngNm, args=None):
    clrScr()
    ls = getLs()
    avail = [l for l in ls if l != lngNm]
    if not avail:
        print(f"{Col.err}No other languages available to loan from.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    print(f"{Col.hdr}--- Loan Word into {lngNm} ---{Col.rst}\n")
    print("Available Source Languages:")
    for i, l in enumerate(avail):
        print(f"{Col.prm}{i+1}.{Col.rst} {l}")
        
    c = input(f"\n{Col.prm}Choose source language number: {Col.rst}").strip()
    try:
        srcLng = avail[int(c)-1]
    except:
        print(f"{Col.err}Invalid choice.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    clrScr()
    print(f"{Col.hdr}--- Loaning from {srcLng} ---{Col.rst}\n")
    q = input(f"{Col.prm}Search term in {srcLng}: {Col.rst}").strip().lower()
    srcDat = ldCsv(srcLng)
    resLst = [(i, r) for i, r in enumerate(srcDat) if q in r["Lemma"].lower() or q in r["Gloss"].lower() or q in r["IPA"].lower()]
    
    if not resLst:
        print(f"{Col.err}No matches found in {srcLng}.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    print()
    for idx, (i, r) in enumerate(resLst):
        print(f"{Col.prm}{idx}.{Col.rst} {Col.hdr}{r['Lemma']}{Col.rst} /{Col.ipa}{r['IPA']}{Col.rst}/ - {Col.ok}{r['Gloss']}{Col.rst}")
        
    sc = input(f"\n{Col.prm}Choose word to loan: {Col.rst}").strip()
    try: 
        srcWrd = resLst[int(sc)][1]
    except:
        print(f"{Col.err}Invalid choice.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    clrScr()
    print(f"{Col.hdr}--- Adapting Loan Word ---{Col.rst}\n")
    print(f"Original: {Col.hdr}{srcWrd['Lemma']}{Col.rst} /{Col.ipa}{srcWrd['IPA']}{Col.rst}/")
    print(f"Gloss: {Col.ok}{srcWrd['Gloss']}{Col.rst} | PoS: {Col.prm}{srcWrd['PoS']}{Col.rst}\n")
    print(f"{Col.prm}(Press Ctrl+C to abort){Col.rst}\n")
    
    try:
        nIpa = input(f"{Col.prm}Adapted IPA (or CXS) in {lngNm}: {Col.rst}").strip()
        if not nIpa:
            print(f"{Col.err}Aborted. Adapted IPA required.{Col.rst}")
            input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
            return
        if cfgDat.get("cxs", False): nIpa = cvCxs(nIpa)
        
        nGls = input(f"{Col.prm}Gloss [{srcWrd['Gloss']}]: {Col.rst}").strip()
        if not nGls: nGls = srcWrd['Gloss']
        
        nPos = input(f"{Col.prm}PoS [{srcWrd['PoS']}]: {Col.rst}").strip()
        if not nPos: nPos = srcWrd['PoS']
        
        defEty = f"Loan from {srcLng}: {srcWrd['Lemma']} /{srcWrd['IPA']}/"
        nEty = input(f"{Col.prm}Etymology [{defEty}]: {Col.rst}").strip()
        if not nEty: nEty = defEty
        
        nNts = input(f"{Col.prm}Notes: {Col.rst}").strip()
        nTgs = input(f"{Col.prm}Tags: {Col.rst}").strip()
        nRel = input(f"{Col.prm}Related Words: {Col.rst}").strip()
        
    except KeyboardInterrupt:
        print(f"\n{Col.err}Aborted.{Col.rst}")
        input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        return
        
    csvDat = ldCsv(lngNm)
    lem = getOrt(lngNm, nIpa)
    csvDat.append({"Lemma": lem, "Gloss": nGls, "IPA": nIpa, "PoS": nPos, "Etymology": nEty, "Notes": nNts, "Tags": nTgs, "Related Words": nRel})
    svCsv(lngNm, csvDat)
    
    jf = os.path.join(dirNm, lngNm, f"{lngNm}.json")
    if not os.path.exists(jf):
        print(f"\n{Col.err}No orthography for {lngNm}.{Col.rst}")
        if input(f"{Col.prm}Make one now? (y/n): {Col.rst}").strip().lower() == 'y': 
            mkOrt(lngNm)
            lem = getOrt(lngNm, nIpa)
            
    print(f"\n{Col.ok}Added Loan: {Col.hdr}{lem}{Col.rst} (/{Col.ipa}{nIpa}{Col.rst}/) - {nGls}{Col.rst}")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def prtWrkHlp(has_lexifer):
    print(f"{Col.hdr}--- Workspace Commands ---{Col.rst}")
    print(f"  {Col.prm}/a, /add [ipa/cxs] [gloss] [pos]{Col.rst} : Add a new word (args optional)")
    print(f"  {Col.prm}/lo, /loan{Col.rst} : Loan a word from another language")
    if has_lexifer:
        print(f"  {Col.prm}/g, /gen, /generate{Col.rst} : Generate words with Lexifer")
    print(f"  {Col.prm}/town, /settle{Col.rst} : Generate town/settlement names")
    print(f"  {Col.prm}/sw, /swadesh{Col.rst} : Check/Generate Swadesh 200 vocabulary")
    print(f"  {Col.prm}/e, /edit [query]{Col.rst} : Edit a word (leave blank to see newest)")
    print(f"  {Col.prm}/s, /search [query]{Col.rst} : Search words (leave blank to see newest)")
    print(f"  {Col.prm}/v, /view{Col.rst} : View full vocabulary")
    print(f"  {Col.prm}/y, /sync [all | 1] [query]{Col.rst} : Sync words to daughters")
    print(f"  {Col.prm}/ch, /chart{Col.rst} : View IPA & Orthography chart")
    print(f"  {Col.prm}/o, /orth, /orthography{Col.rst} : Orthography editor")
    print(f"  {Col.prm}/p, /par, /para, /paradigm{Col.rst} : Paradigm editor")
    print(f"  {Col.prm}/l, /lex, /lexurgy{Col.rst} : Run Lexurgy sound changes")
    print(f"  {Col.prm}/tr, /translate{Col.rst} : Translator tool")
    print(f"  {Col.prm}/wt, /wordtree{Col.rst} : Evolve word tree")
    print(f"  {Col.prm}/b, /back{Col.rst} : Go back to main menu")
    print(f"  {Col.prm}/h, /help{Col.rst} : Show this list")
    print(f"  {Col.prm}/q, /quit{Col.rst} : Quit application")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def wrkSpc(lngNm):
    def_name = lngNm.replace(" ", "-").lower()
    def_file = os.path.join("tools", "lexifer", f"{def_name}.def")
    
    while True:
        has_lexifer = os.path.exists(def_file)
        clrScr()
        print(f"{Col.hdr}=== Workspace: {lngNm} ==={Col.rst}\n")
        
        print(f"{Col.prm}Enter command (/h for help): {Col.rst}", end="")
        inp = input().strip()
        if not inp: continue
        parts = inp.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd in ['/b', '/back']: break
        elif cmd in ['/h', '/help']: prtWrkHlp(has_lexifer)
        elif cmd in ['/a', '/add']: addWrd(lngNm, args)
        elif cmd in ['/lo', '/loan']: lonWrd(lngNm, args)
        elif cmd in ['/g', '/gen', '/generate'] and has_lexifer: genWrd(lngNm)
        elif cmd in ['/town', '/settle']: genStl(lngNm)
        elif cmd in ['/sw', '/swadesh']: chkSwd(lngNm)
        elif cmd in ['/e', '/edit']: edtWrd(lngNm, args)
        elif cmd in ['/s', '/search']: srcWrd(lngNm, args)
        elif cmd in ['/v', '/view']: vwWrd(lngNm)
        elif cmd in ['/y', '/sync']: syncWrd(lngNm, args)
        elif cmd in ['/ch', '/chart']: vwCht(lngNm)
        elif cmd in ['/o', '/orth', '/orthography']: mkOrt(lngNm)
        elif cmd in ['/l', '/lex', '/lexurgy']: runLx(lngNm)
        elif cmd in ['/p', '/par', '/para', '/paradigm']: pdmMnu(lngNm)
        elif cmd in ['/tr', '/translate']: trnSltr(lngNm)
        elif cmd in ['/wt', '/wordtree']: evlWrdTr(lngNm)
        elif cmd in ['/c', '/conf', '/config', '/cxs']: setMnu()
        elif cmd in ['/q', '/quit']: exit()
        else:
            print(f"{Col.err}Invalid command.{Col.rst}")
            input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def prtMnHlp():
    print(f"{Col.hdr}--- Main Menu Commands ---{Col.rst}")
    print(f"  {Col.prm}[number]{Col.rst} : Open workspace for language [number]")
    print(f"  {Col.prm}/n, /new [name]{Col.rst} : Create a new language")
    print(f"  {Col.prm}/d, /dau, /daughter [number]{Col.rst} : Create daughter of language [number]")
    print(f"  {Col.prm}/r, /re, /rename [number]{Col.rst} : Rename language [number]")
    print(f"  {Col.prm}/x, /del [number]{Col.rst} : Delete language [number]")
    print(f"  {Col.prm}/c, /com, /compare [num1] [num2]{Col.rst} : Compare two languages")
    print(f"  {Col.prm}/t, /tree{Col.rst} : View language family trees")
    print(f"  {Col.prm}/conf, /config, /cxs{Col.rst} : Toggle CXS input on/off")
    print(f"  {Col.prm}/q, /quit{Col.rst} : Quit application")
    print(f"  {Col.prm}/h, /help{Col.rst} : Show this list")
    input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

def mnApp():
    iniApp()
    while True:
        clrScr()
        ls = getLs()
        if not ls:
            print(f"{Col.hdr}No languages found.{Col.rst}")
            print(f"{Col.prm}Type /new [name] to create one.{Col.rst}\n")
        else:
            print(f"{Col.hdr}=== Languages ==={Col.rst}\n")
            for i, l in enumerate(ls): print(f"{Col.prm}{i+1}.{Col.rst} {l}")
        
        print(f"\n{Col.prm}Enter command (/h for help): {Col.rst}", end="")
        inp = input().strip()
        if not inp: continue
        parts = inp.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd in ['/q', '/quit']: exit()
        elif cmd in ['/h', '/help']: prtMnHlp()
        elif cmd in ['/n', '/new']: 
            name = " ".join(args) if args else None
            mkLng(name)
        elif cmd in ['/d', '/dau', '/daughter']:
            try: mkDau(ls[int(args[0])-1])
            except: 
                print(f"{Col.err}Invalid language number.{Col.rst}")
                input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        elif cmd in ['/r', '/re', '/rename']:
            try: renLng(ls[int(args[0])-1])
            except: 
                print(f"{Col.err}Invalid language number.{Col.rst}")
                input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        elif cmd in ['/x', '/del']:
            try: delLng(ls[int(args[0])-1])
            except: 
                print(f"{Col.err}Invalid language number.{Col.rst}")
                input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        elif cmd in ['/c', '/com', '/compare']:
            try: cmpLng(ls[int(args[0])-1], ls[int(args[1])-1])
            except:
                cmpLng()
        elif cmd in ['/t', '/tree']: vwTree()
        elif cmd in ['/conf', '/config', '/cxs']: setMnu()
        elif cmd.isdigit():
            idx = int(cmd) - 1
            if 0 <= idx < len(ls):
                wrkSpc(ls[idx])
            else:
                print(f"{Col.err}Invalid language number.{Col.rst}")
                input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")
        else:
            print(f"{Col.err}Invalid command.{Col.rst}")
            input(f"\n{Col.prm}[Enter] to continue...{Col.rst}")

if __name__ == "__main__": mnApp()
