import html
import json
import re

# Load census 2021
with open('data/census_2021.json', 'r', encoding='utf-8') as f:
    CENSUS_LIST = json.load(f)

# Read raw source text
with open('raw_source.txt', 'r', encoding='utf-8') as f:
    raw_text = f.read()

decoded = html.unescape(raw_text)
body_idx = decoded.find('1. Acharya')
body_text = decoded[body_idx:]

pattern = re.compile(r'(\d+)\.\s*(.*?)(?=<br\s*/?>|</br>|</p>)', re.DOTALL | re.IGNORECASE)
matches = pattern.findall(body_text)

if matches and not matches[-1][1].strip():
    matches = matches[:-1]

print(f"Total raw lines matched: {len(matches)}")

DEVANAGARI_MAP = {
    "acharya": "आचार्य",
    "adhikari": "अधिकारी",
    "agnihotri": "अग्निहोत्री",
    "agri": "आग्री",
    "airi": "ऐरी",
    "ale": "आले",
    "amast": "अमष्ट",
    "amatya": "अमात्य",
    "amgai/amgain": "अम्गाईं",
    "angbahang": "आङ्बाहाङ",
    "angraten": "आङ्ग्रतेन",
    "angthupuhang": "आङ्थुपुहाङ",
    "ansari": "अन्सारी",
    "araqi": "अराकी",
    "arjal/arjyal/arjel/aryal": "अर्याल / अर्ज्याल",
    "aryal": "अर्याल",
    "aslami": "अस्लामी",
    "athpahare": "अठपहरिया",
    "awa": "अवा",
    "awasthi": "अवस्थी",
    "bachhgoti chauhan": "बछगोती चौहान",
    "badahi": "बढई",
    "badal": "बादल",
    "badi": "वादी",
    "bagyal": "बग्याल",
    "baijali": "बैजाली",
    "bainge": "बैङ्गे",
    "bajgain": "बजगाईं",
    "bajyu": "बज्युल",
    "bakharel/bakhrel": "बाख्रेल",
    "balam": "बलम",
    "balami": "बलामी",
    "bam": "बम",
    "bamanayata": "बामनायात",
    "bammala": "बम्मल",
    "bania/baniya": "बानियाँ / बनियाँ",
    "baniya": "बानियाँ",
    "banshi": "वंशी",
    "bantar": "बान्तर",
    "bantava": "बान्तवा",
    "banth": "बान्थ",
    "bantr": "बान्तर",
    "barai": "बरई",
    "baral": "बराल",
    "bardiya": "बर्दिया",
    "barma": "बर्मा",
    "barman/varman": "वर्मन",
    "baruwal": "बरुवाल",
    "baskota/banskota": "बास्कोटा",
    "basnet/basnyat": "बस्नेत / बस्न्यात",
    "basti": "बस्ती",
    "bastola": "बास्तोला",
    "basyal/bashyal": "बस्याल",
    "beduwar": "बेदुवार",
    "belbase": "बेलबासे",
    "benglasi": "बेङ्ग्लासी",
    "bha": "भा",
    "bhadel": "भदेल",
    "bhagat": "भगत",
    "bhandari": "भण्डारी",
    "bhanya": "भन्या",
    "bhat": "भट",
    "bhatnagar": "भटनागर",
    "bhatta": "भट्ट",
    "bhattachan": "भट्टाचन",
    "bhattarai": "भट्टराई",
    "bhetwal/bhetuwal": "भेटवाल",
    "bhihar": "भिहर",
    "bhotgamiya": "भोटगमिया",
    "bhul/bhool": "भुल",
    "bhusal": "भुसाल",
    "bhurtel/bhurtyal": "भुर्तेल",
    "bidari": "बिडारी",
    "bikral": "बिक्राल",
    "birkatta": "बिर्काट्टा",
    "bisen": "बिसेन",
    "bishwokarma": "विश्वकर्मा",
    "bista": "बिष्ट",
    "bista/bisht": "बिष्ट",
    "biswas": "विश्वास",
    "blon": "ब्लोन",
    "bogati": "बोगटी",
    "bohra/bohara": "बोहरा",
    "boksha": "बोक्सा",
    "boktan": "बोक्तान",
    "bomjan": "बोम्जन",
    "bote": "बोटे",
    "brachey": "ब्राचे",
    "buda": "बुढा",
    "budha": "बुढा",
    "budhaer/budhair": "बुढायर",
    "budhatoki": "बुढाथोकी",
    "bura": "बुरा",
    "burathoki": "बुढाथोकी",
    "camkhala": "चामखल",
    "chaelengarten": "चेलेंङार्तेन",
    "chalise": "चालिसे",
    "chamar": "चमार",
    "chami": "चामी",
    "chamlagain": "चम्लागाईं",
    "chamlinge": "चाम्लिङ",
    "chand": "चन्द",
    "chandra": "चन्द्र",
    "chapagain": "चापगाईं",
    "charmakar": "चर्मकार",
    "chataut": "चटौत",
    "chaturvedi": "चतुर्वेदी",
    "chauden": "चौदेन",
    "chaudhari": "चौधरी",
    "chaudhari/chaudhary": "चौधरी",
    "chaudhary": "चौधरी",
    "chauhan": "चौहान",
    "chaulagain": "चौलागाईं",
    "chaurasiya": "चौरसिया",
    "chavey": "चावे",
    "chhetri": "क्षेत्री",
    "chhungpate": "छुङपाते",
    "chidimar": "चिडीमार",
    "chik": "चिक",
    "chitauniya": "चितौनिया",
    "chitrakar": "चित्रकार",
    "chobeguhang": "चोबेगुहाङ",
    "chongbang": "चोङबाङ",
    "chunanra": "चुनँरा",
    "churihar": "चुरीहार",
    "chyame": "च्यामे",
    "chyamkhal": "च्यामखल",
    "chyawa": "च्यावा",
    "dafali": "दफाली",
    "dahal": "दाहाल",
    "dali": "दली",
    "damai": "दमाई",
    "damrang": "दाम्राङ",
    "dangal": "दङ्गाल",
    "dangauriya": "दङ्गौरा",
    "dangi": "डाँगी",
    "dangol": "डङ्गोल",
    "dangora": "दङ्गोरा",
    "danwar": "दनुवार",
    "danya": "दान्या",
    "darden": "दार्देन",
    "dargarcha": "दर्गार्छा",
    "darji/darjee": "दर्जी",
    "darlami": "दर्लामी",
    "darnal": "दर्नाल",
    "darpa": "दार्पा",
    "darzi": "दर्जी",
    "das": "दास",
    "daubhadel": "दौभडेल",
    "dawadi": "दवाडी",
    "deola": "देउला",
    "deppacha": "देप्पाछा",
    "deuba": "देउवा",
    "deula": "देउला",
    "dev": "देव",
    "devkota": "देवकोटा",
    "devlinga": "देवलिङ्गा",
    "dhakal": "ढकाल",
    "dhami": "धामी",
    "dhandi": "धान्डी",
    "dhanuk": "धानुक",
    "dharikar/dhankar": "धारीकार",
    "dhital": "धिताल",
    "dhobi": "धोबी",
    "dholi": "ढोली",
    "dhungana": "ढुङ्गाना",
    "dhungel/dhungyal": "ढुङ्गेल",
    "dhuniya": "धुनिया",
    "dhyapa": "ध्यापा",
    "dimdu": "दिम्दु",
    "dixit": "दीक्षित",
    "dixit/dikshit": "दीक्षित",
    "doeja": "दोजा",
    "dom": "डोम",
    "dong": "दोङ",
    "dotel/dotiyal": "डोटेल",
    "dudh": "दुध",
    "dulal": "दुलाल",
    "durbicha": "दुर्बिछा",
    "dushadh": "दुसाध",
    "duwadi": "दुवाडी",
    "duwal": "दुवाल",
    "ektinhang": "एक्तिन्हाङ",
    "esmali": "इस्माली",
    "faqir": "फकिर",
    "gachhadar": "गच्छदार",
    "gaddi": "गद्दी",
    "gaha": "गाहा",
    "gaine": "गाईने",
    "gaire": "गैरे",
    "gaithaula": "गैह्रेथौला",
    "gandharba/gandharva": "गन्धर्व",
    "garbhar": "गार्भर",
    "garden": "गार्देन",
    "garmeba": "गार्मेबा",
    "garshejata": "गार्सेजटा",
    "gartola": "गर्तौला",
    "gauchan": "गौचन",
    "gaudel": "गौडेल",
    "gautam": "गौतम",
    "g.c.": "जि.सी. (घर्ती क्षेत्री)",
    "ghale": "घले",
    "ghartel/ghartyal": "घर्तेल",
    "gharti": "घर्ती",
    "gharti/gharti": "घर्ती",
    "ghartmel": "घर्तमेल",
    "ghimire/ghimirya": "घिमिरे",
    "ghising": "घिसिङ",
    "ghodane": "घोडाने",
    "ghurcholi": "घुरचोली",
    "ghyalang": "घ्यालाङ",
    "gilal": "गिलाल",
    "giri": "गिरी",
    "glan": "ग्लान",
    "gole": "गोले",
    "gomden": "गोम्देन",
    "gonga": "गोङ्गा",
    "gorkhali": "गोर्खाली",
    "gotame": "गोतामे",
    "grandan": "ग्रन्दन",
    "guragain/gurangain": "गुरागाईं",
    "gurung": "गुरुङ",
    "gurwacharya": "गुर्वाचार्य",
    "gwala": "ग्वाला",
    "gyawali": "ज्ञावली",
    "hada": "हाडा",
    "haeljliya": "हैलज्लिया",
    "hajam": "हजाम",
    "hajara": "हजरा",
    "hajjam": "हज्जाम",
    "halahulu": "हलाहुलु",
    "halal-khor": "हलालखोर",
    "haldaliya": "हल्दलिया",
    "halkhor": "हलखोर",
    "halocha": "हालोछा",
    "haluwai/halwai": "हलुवाई",
    "hamal": "हमाल",
    "harijan": "हरिजन",
    "hellok": "हेल्लोक",
    "hemjliya": "हेम्ज्लिया",
    "hina": "हिना",
    "hiski": "हिस्की",
    "humagain/hamyagain": "हुमागाईं",
    "hudke": "हुड्के",
    "ingbadokpa": "इङ्बादोकपा",
    "jalari": "जलारी",
    "jat": "जाट",
    "jauhari": "जौहरी",
    "jha": "झा",
    "jhainti": "झैन्ती",
    "jhankri": "झाँक्री",
    "jhupucha": "झुपुछा",
    "jijicha": "जिजिछा",
    "jogi": "जोगी",
    "jonche": "जोन्छे",
    "joshi": "जोशी",
    "juju": "जुजु",
    "julaha": "जुलाहा",
    "kabhuja": "कभुजा",
    "kadariya": "कडरिया",
    "kadayat": "कडायत",
    "kadel": "कँडेल",
    "kaji": "काजी",
    "kakaihiya": "ककैहिया",
    "kalar": "कलार",
    "kalwar": "कलवार",
    "kalyal": "कल्याल",
    "kambang": "कम्बाङ",
    "kami": "कामी",
    "kamsakar": "कंसकार",
    "kandariya": "कण्डरिया",
    "kandel/kandyal": "कँडेल",
    "kanga": "काङ्गा",
    "kanphata": "कानफाटा",
    "kanphatta": "कानफट्टा",
    "kaphalya": "कफल्या",
    "kaphle/kafle": "काफ्ले",
    "karanjit": "करञ्जित",
    "karcholiya": "करचोलिया",
    "karki": "कार्की",
    "karmaba": "कर्माबा",
    "karmacharya": "कर्माचार्य",
    "karn": "कर्ण",
    "karte": "कार्ते",
    "kasain": "कसाइँ",
    "kasaju": "कसाजु",
    "kathayat": "कठायत",
    "katicha": "कातिछा",
    "katriya": "कटरिया",
    "katawal/katwal/katuwal": "कटवाल / कटुवाल",
    "kawar": "कँवर",
    "kayastha": "कायस्थ",
    "ketra": "केत्रा",
    "kewat": "केवट",
    "khadayat": "खडायत",
    "khadgi": "खड्गी",
    "khadka/khadga": "खड्का",
    "khakurel": "खकुरेल",
    "khalinge": "खालिङ",
    "khan": "खान",
    "khanal": "खनाल",
    "khand": "खाँण",
    "khang": "खङ्ग",
    "kharal": "खराल",
    "kharel": "खरेल",
    "khas": "खस",
    "khasu": "खसु",
    "khatave": "खतवे",
    "khati": "खाती",
    "khatik": "खटिक",
    "khatiwada": "खतिवडा",
    "khatri": "खत्री",
    "khatri chhetri/k.c.": "खत्री क्षेत्री (के.सी.)",
    "khatwe": "खत्वे",
    "khausiya": "खौसिया",
    "khawas": "खवास",
    "khulal": "खुलाल",
    "khunaha": "खुनाहा",
    "khusa": "खुसा",
    "khwakhali": "ख्वाखली",
    "khyargoli": "ख्यार्गोली",
    "kochila": "कोचिला",
    "koikyal": "कोइक्याल",
    "koirala": "कोइराला",
    "koiri/koeri": "कोइरी",
    "kori": "कोरी",
    "kuinkel": "कुइँकेल",
    "kulu": "कुलु",
    "kulunge": "कुलुङ",
    "kumale": "कुमाले",
    "kumar chauhan": "कुमार चौहान",
    "kunwar": "कुँवर",
    "kurmi": "कुर्मी",
    "kusle": "कुस्ले",
    "laeden": "लाएदेन",
    "lakaul/lakoul": "लकौल",
    "lakhey": "लाखे",
    "lalpuriya": "लालबुरिया",
    "lama": "लामा",
    "lamichhane": "लामिछाने",
    "lampuchhwa": "लाम्पूछ्वा",
    "lamsal": "लम्साल",
    "lawat": "लवट",
    "lawati": "लावाती",
    "layeku": "लयेकु",
    "lekhak": "लेखक",
    "likhim": "लिखिम",
    "lingden": "लिङ्देन",
    "lo": "लो",
    "lochan": "लोचन",
    "lohamkami": "लोहँकमी",
    "lohani": "लोहनी",
    "lohar": "लोहार",
    "lohorong": "लोहोरुङ",
    "lopchan": "लोप्चन",
    "luitel/luintel": "लुइँटेल",
    "mabuhang": "माबुहाङ",
    "madikami": "मधिकमी",
    "magar": "मगर",
    "mahaju": "महाजु",
    "mahant": "महन्त",
    "mahara": "महारा",
    "mahapatra": "महापात्र",
    "maharjan": "महर्जन",
    "mahat": "महत",
    "mahatara": "महतरा",
    "mahato": "महतो",
    "mainali": "मैनाली",
    "maithili": "मैथिली",
    "majhaura": "मझौरा",
    "majhi": "माझी",
    "malbariya": "मलबारिया",
    "mali": "माली",
    "malla": "मल्ल",
    "mallah": "मल्लाह",
    "manandhar": "मानन्धर",
    "mandaen": "मान्देन",
    "mandal": "मण्डल",
    "mangyung": "माङयुङ",
    "mardaniyan": "मर्दानियाँ",
    "marhatta": "मरहट्टा",
    "marik": "मरीक",
    "martu": "मार्तु",
    "marwadi/marwari": "मारवाडी",
    "maske/maskey": "मास्के",
    "maski": "मास्की",
    "mathur": "माथुर",
    "mathema": "माथेमा",
    "mayam": "मायम",
    "mayokpa": "मायोक्पा",
    "mestar": "मेस्तर",
    "mijar": "मिजार",
    "mishra": "मिश्र",
    "miyan": "मियाँ",
    "mochi": "मोची",
    "moktan": "मोक्तान",
    "moktung": "मोक्तुङ",
    "morangiya": "मोरङ्गिया",
    "mudbhari": "मुडभरी",
    "mughal": "मुगल",
    "mul/mool": "मूल",
    "mulepati": "मुलेपती",
    "mulicha": "मुलिछा",
    "munankarmi": "मुनाकर्मी",
    "murung": "मुरुङ",
    "musa": "मुसा",
    "musahar": "मुसहर",
    "nagarchi": "नगर्ची",
    "nakami": "नकःमी",
    "napit": "नापित",
    "nat": "नट",
    "natuwa": "नटुवा",
    "nepal/nepalya": "नेपाल",
    "neupane/nyaupane": "न्यौपाने",
    "ngarden": "ङार्देन",
    "ngarpa": "ङार्पा",
    "niraula": "निराला",
    "novlicha": "नोब्लिछा",
    "nuniyar": "नुनियार",
    "od": "ओड",
    "ojha": "ओझा",
    "ojhatanchhe": "ओझातान्छे",
    "oli": "ओली",
    "ongchongbo": "ओङचोङ्बो",
    "onta": "ओन्ता",
    "pageni": "पागेनी",
    "pahari": "पहाडी",
    "paitola": "पैतोला",
    "pajunden": "पाजुन्देन",
    "pakhrin": "पाख्रिन",
    "pal/paal": "पाल",
    "pal": "पाल",
    "palikhe": "पालिखे",
    "palung": "पालुङ",
    "pandey/pandeya": "पाण्डेय / पाण्डे",
    "pandey": "पाण्डे",
    "pandey/pande": "पाण्डे",
    "pandit": "पण्डित",
    "paneru": "पनेरु",
    "pangeni": "पाङ्गेनी",
    "pant": "पन्त",
    "panthi/panthee": "पन्थी",
    "parajuli": "पराजुली",
    "parihar": "परिहार",
    "pariyar": "परियार",
    "parki": "पार्की",
    "pasi": "पासी",
    "paswan": "पासवान",
    "pathak": "पाठक",
    "pathan": "पठान",
    "patharkat": "पत्थरकट",
    "patra": "पात्र",
    "patrabansh": "पात्रवंश",
    "paudel/paudyal/poudyal": "पौडेल / पौड्याल",
    "payen": "पाएन",
    "pegahang": "पेगाहाङ",
    "pelmange": "पेल्माङ्गे",
    "pethegimbang": "पेथेगिम्बाङ",
    "phalinge": "फालिङ्गे",
    "phanghang": "फाङहाङ",
    "phembu": "फेम्बु",
    "phenduwa": "फेन्दुवा",
    "phengdi": "फेङ्दी",
    "phewali": "फेवाली",
    "phungja": "फुङ्जा",
    "phurumbo": "फुरुम्बो",
    "phuyal": "फुयाँल",
    "piya": "पिया",
    "pode": "पोडे",
    "pokhrel/pokharel": "पोखरेल",
    "pradhan": "प्रधान",
    "pradhananga": "प्रधानाङ्ग",
    "praja": "प्रजा",
    "prajapati": "प्रजापति",
    "pramuba": "प्रमुबा",
    "prasai": "प्रसाईं",
    "prengel": "प्रेङ्गेल",
    "prihar": "प्रिहार",
    "pudasaini": "पुडासैनी",
    "pujari": "पुजारी",
    "pulami": "पुलामी",
    "pulu": "पुलु",
    "pun": "पुन",
    "punglang": "पुङ्लाङ",
    "punwal": "पुनवाल",
    "purtel": "पुर्तेल",
    "putwar": "पुत्वार",
    "pyakurel/pyakuryal": "प्याकुरेल",
    "qassab": "कस्साब",
    "raghubansi": "रघुवंशी",
    "rahachey": "राहाचे",
    "rai": "राई",
    "rajak": "रजक",
    "rajbaidya": "राजवैद्य",
    "rajbanshi": "राजवंशी",
    "rajbhandari": "राजभण्डारी",
    "rajhatya": "राजहत्य",
    "rajhtiya": "राजह्तिया",
    "rajkul": "राजकुल",
    "rajlawat": "राजलवट",
    "rajput": "राजपूत",
    "rajopadhyaya": "राजोपाध्याय",
    "rajvamshi": "राजवंशी",
    "rakaskoti": "राकास्कोटी",
    "rakhal": "राखाल",
    "ram": "राम",
    "ramjoli": "रामजोली",
    "rana": "राणा / राना",
    "ranabhat": "रानाभाट",
    "rangrez": "रङ्ग्रज",
    "ranjitkar": "रञ्जितकार",
    "rathaur": "राठौर",
    "rathore": "राठौर",
    "raut": "राउत",
    "rautar": "रौतार",
    "ravanrajghariya": "रावणराजघरिया",
    "ravidas": "रविदास",
    "rawal": "रावल",
    "rawat": "रावत",
    "raya": "राया",
    "rayamajhi": "रायामाझी",
    "regmi": "रेग्मी",
    "rewali": "रेवाली",
    "rijal": "रिसाल / रिजाल",
    "rimal": "रिमाल",
    "risal/risyal": "रिसाल",
    "roka/rokaya/rokka": "रोका / रोकाय",
    "rokaha/roka/rokaya": "रोका / रोकाहा",
    "rukain": "रुकैन",
    "rumba": "रुम्बा",
    "rumdali": "रुम्दाली",
    "rumkhami": "रुमखामी",
    "rupakheti": "रुपाखेती",
    "rupihang": "रुपीहाङ",
    "saam": "साम",
    "sabrey": "साब्रे",
    "sabzi-farosh": "सब्जीफरोश",
    "sahi": "शाही",
    "sahikh": "शेख",
    "sahukhala": "साहुखलः",
    "sainju": "सैँजू",
    "saksena/saxena": "सक्सेना",
    "samahang": "सामाहाङ",
    "samal": "सामल",
    "samant": "सामन्त",
    "sampange": "साम्पाङ",
    "sangraula/sangroula": "सङ्ग्रौला",
    "sanjel": "सञ्जेल",
    "sapkota": "सापकोटा",
    "sapu": "सापू",
    "sarbhang/sarbariya": "सरभङ्ग",
    "sardar": "सरदार",
    "sarki": "सार्की",
    "saru": "सारु",
    "satihangma": "सातीहाङ्मा",
    "satyal": "सत्याल",
    "sawad/saund/saud": "साउद",
    "sayyid": "सय्यद",
    "sedhai/sedhain": "सेढाईं",
    "sen": "सेन",
    "shah": "शाह",
    "shahi": "शाही",
    "shakya": "शाक्य",
    "shamden": "शाम्देन",
    "shamsher/shumsher": "शमशेर",
    "sharma": "शर्मा",
    "shelle": "शेल्ले",
    "sherchan": "शेरचन",
    "sherpa": "शेर्पा",
    "sherwa": "शेर्वा",
    "shewan": "शेवान",
    "shigu": "शिगु",
    "shingden": "शिङ्देन",
    "shrestha": "श्रेष्ठ",
    "shrivastava": "श्रीवास्तव",
    "shukla": "शुक्ल",
    "shyangbo": "श्याङ्बो",
    "sidari": "सिदारी",
    "sigdel": "सिग्देल",
    "sijapati": "सिजापती",
    "sikami": "सीकर्मी",
    "silwal": "सिलवाल",
    "simkhara": "सिम्खडा",
    "singh": "सिंह",
    "singthebe": "सिङ्थेबे",
    "sinjali": "सिञ्जाली",
    "sinjapati": "सिञ्जापती",
    "sinkhada": "सिङ्खडा",
    "sitaula": "सिटौला",
    "siwakoti": "सिवाकोटी",
    "solriya": "सोलरिया",
    "sotange": "सोताङ्गे",
    "soti": "सोती",
    "subba": "सुब्बा",
    "subedi": "सुवेदी",
    "suchikar": "सुचीकार",
    "sudhi": "सुँढी",
    "sunaha": "सुनहा",
    "sunar": "सुनार",
    "suryabansi": "सूर्यवंशी",
    "suwal": "सुवाल",
    "suyal": "सुयाल",
    "swangsabu": "स्वाङ्साबु",
    "swansabu": "स्वाँसबु",
    "syangtang": "स्याङताङ",
    "tabdar": "तब्दार",
    "talchabhadel": "ताल्चाभडेल",
    "tamaden": "तामादेन",
    "tamang": "तामाङ",
    "tamata": "टमटा",
    "tamchhange": "ताम्छाङ्गे",
    "tamrakar": "ताम्राकार",
    "tamu": "तमु",
    "tandukar": "तण्डुकार",
    "tanglami": "ताङ्ग्लामी",
    "tanti": "ताँती",
    "tarali": "तराली",
    "tatma/tatwa": "तत्मा",
    "teli": "तेली",
    "tepe": "तेपे",
    "thaiba": "थैव",
    "thakur/thakul": "ठाकुर",
    "thakur": "ठाकुर",
    "thakurai": "ठकुराई",
    "thakurathi": "ठकुराठी",
    "thakuri": "ठकुरी",
    "thamsuhang": "थाम्सुहाङ",
    "thandar": "थान्दार",
    "thapa": "थापा",
    "thapalia/thapaliya": "थपलिया",
    "thatal": "थटाल",
    "thavo": "थाभो",
    "thebe": "थेबे",
    "thing": "थिङ",
    "thokur": "थोकर",
    "thulung": "थुलुङ",
    "thulunge": "थुलुङ",
    "thumsing": "थुम्सिङ",
    "thuppoko": "थुप्पोको",
    "timila": "तिमीला",
    "timilsina/timalsina": "तिमिल्सिना",
    "tirkey": "तिर्की",
    "titung": "तितुङ",
    "tiwari": "तिवारी",
    "torchaki": "तोर्चाकी",
    "tripathi": "त्रिपाठी",
    "tulachan": "तुलाचन",
    "tuladhar": "तुलाधर",
    "tumbahamphe": "तुम्बाहाम्फे",
    "tumyangpa": "तुम्याङ्पा",
    "tupa": "तुपा",
    "ujjain": "उज्जैन",
    "upadhyaya/upadhyay": "उपाध्याय",
    "upadhyaya": "उपाध्याय",
    "upreti/uprety": "उप्रेती",
    "vaidya/baidya": "वैद्य",
    "vaish": "वैश्य",
    "vajracharya": "वज्राचार्य",
    "wagle": "वाग्ले",
    "waiba": "वाइबा",
    "woli": "ओली",
    "yadav": "यादव",
    "yamphu": "यामफु",
    "yongya": "योङ्या",
    "yonjan": "योन्जन",
    "yorka": "योर्का",
    "zimba": "जिम्बा",
    "dharala": "धराला",
}

GOTRA_DATA = {
    "kaudinya": {
        "devanagari": "कौडिन्य",
        "pravara": "Tryarshi (Maitravaruna, Kaudinya, Vasishtha)",
        "kuldevata": "Baraha / Mahadev / Bindhyabasini",
        "region": "Gandaki, Bagmati, Koshi",
        "description": "Descendants of Sage Kundina/Kaundinya, prominent in Vedic scholarship and sacred rites."
    },
    "kashyap": {
        "devanagari": "कश्यप",
        "pravara": "Tryarshi (Kashyapa, Avatsara, Naidhruva)",
        "kuldevata": "Masto / Kalika / Shiva / Baraha",
        "region": "Karnali, Sudurpashchim, Gandaki, Bagmati",
        "description": "Sage Kashyapa lineage, one of the primary foundational Saptarshi gotras spanning Brahmins, Chhetris, and Dalits."
    },
    "bharadwaj": {
        "devanagari": "भारद्वाज",
        "pravara": "Tryarshi (Bharadvaja, Angirasa, Barhaspatya)",
        "kuldevata": "Baraha / Nilkantha / Kalika",
        "region": "Gandaki, Bagmati, Koshi, Karnali",
        "description": "Descendants of Sage Bharadvaja, renowned seer of the Rigveda. Historically counselors and ritual masters."
    },
    "atreya": {
        "devanagari": "आत्रेय",
        "pravara": "Tryarshi (Atreya, Archananasa, Shyavashva)",
        "kuldevata": "Masto / Baraha / Shiva",
        "region": "Gandaki, Lumbini, Bagmati, Koshi",
        "description": "Lineage of Sage Atri, noted for spiritual austerities and widespread presence across Western and Central Nepal."
    },
    "kaushik": {
        "devanagari": "कौशिक",
        "pravara": "Tryarshi (Kaushika, Vishvamitra, Devarata)",
        "kuldevata": "Kalika / Masto / Bhairav",
        "region": "Gandaki, Bagmati, Koshi",
        "description": "Lineage of Sage Vishvamitra (Kaushika), revered for royal origin and attainment of Brahma-rishi status."
    },
    "vatsa": {
        "devanagari": "वत्स",
        "pravara": "Pancharshi (Bhargava, Chyavana, Apnavana, Aurva, Jamadagnya)",
        "kuldevata": "Baraha / Bhairav / Bindhyabasini",
        "region": "Bagmati, Gandaki, Koshi",
        "description": "Bhargava branch lineage of Sage Vatsa, celebrated for scholarly knowledge and Vedic recitations."
    },
    "upamanyu": {
        "devanagari": "उपमन्यु",
        "pravara": "Tryarshi (Vasishtha, Indrapramada, Abharadvasu)",
        "kuldevata": "Nilkantha / Mahadev / Masto",
        "region": "Bagmati, Gandaki, Koshi",
        "description": "Vasishtha branch lineage of Sage Upamanyu, devoted worshiper of Lord Shiva."
    },
    "garga": {
        "devanagari": "गर्ग",
        "pravara": "Tryarshi (Garga, Angirasa, Barhaspatya)",
        "kuldevata": "Mahadev / Devi",
        "region": "Gandaki, Bagmati",
        "description": "Descendants of Sage Garga, celebrated astronomer and royal preceptor of antiquity."
    },
    "mandabya": {
        "devanagari": "माण्डव्य",
        "pravara": "Tryarshi (Mandavya, Angirasa, Barhaspatya)",
        "kuldevata": "Baraha / Vishnu / Shiva",
        "region": "Gandaki, Lumbini, Bagmati",
        "description": "Lineage of Sage Mandavya, recognized for deep perseverance and spiritual equanimity."
    },
    "parashar": {
        "devanagari": "पराशर",
        "pravara": "Tryarshi (Parashara, Vasishtha, Shaktya)",
        "kuldevata": "Shiva / Devi",
        "region": "Gandaki, Bagmati",
        "description": "Lineage of Maharishi Parashara, author of Vishnu Purana and father of Veda Vyasa."
    },
    "shandilya": {
        "devanagari": "शाण्डिल्य",
        "pravara": "Tryarshi (Shandilya, Asita, Devala)",
        "kuldevata": "Surya / Shiva",
        "region": "Koshi, Bagmati",
        "description": "Descendants of Sage Shandilya, proponent of devotional bhakti and the Shandilya Upanishad."
    },
    "dhananjaya": {
        "devanagari": "धनञ्जय",
        "pravara": "Tryarshi (Dhananjaya, Angirasa, Barhaspatya)",
        "kuldevata": "Baraha / Shiva",
        "region": "Koshi, Gandaki",
        "description": "Associated with Sage Dhananjaya, known for valor and spiritual synthesis."
    },
    "bashista": {
        "devanagari": "वशिष्ठ",
        "pravara": "Ekarshi or Tryarshi (Vasishtha, Mitravaruna)",
        "kuldevata": "Baraha / Mahadev",
        "region": "Gandaki, Koshi, Bagmati",
        "description": "Sage Vasishtha, prime guru of the solar dynasty and composer of major Vedic hymns."
    },
    "maudgalya": {
        "devanagari": "मौद्गल्य",
        "pravara": "Tryarshi (Maudgalya, Angirasa, Bharmashva)",
        "kuldevata": "Baraha / Kalika",
        "region": "Koshi, Bagmati",
        "description": "Descendants of Sage Mudgala, acclaimed for discipline and righteous living."
    },
    "agasti": {
        "devanagari": "अगस्ति",
        "pravara": "Tryarshi (Agastya, Mayobhuva, Idhmavaha)",
        "kuldevata": "Mahadev",
        "region": "Bagmati, Koshi",
        "description": "Lineage of Sage Agastya, legendary hermit and pioneer of medicinal and civil sciences."
    },
    "angiras": {
        "devanagari": "अङ्गिरा",
        "pravara": "Tryarshi (Angirasa, Ambarisha, Yauvanashva)",
        "kuldevata": "Surya / Shiva",
        "region": "Bagmati, Gandaki",
        "description": "Sage Angiras lineage, closely linked with sacred fire rituals and hymn composition."
    },
    "gautam": {
        "devanagari": "गौतम",
        "pravara": "Tryarshi (Gautama, Angirasa, Ayasya)",
        "kuldevata": "Masto / Mahadev",
        "region": "Gandaki, Lumbini, Koshi",
        "description": "Sage Gautama Maharishi lineage, founder of Nyaya philosophy and prominent Vedic seer."
    }
}

FALLBACK_GOTRA = {
    "amgai/amgain": ("Kaudinya", "कौडिन्य"),
    "awasthi": ("Garga", "गर्ग"),
    "bagyal": ("Bharadwaj", "भारद्वाज"),
    "bajgain": ("Mandabya", "माण्डव्य"),
    "bakharel/bakhrel": ("Kashyap", "कश्यप"),
    "basyal/bashyal": ("Kaushik", "कौशिक"),
    "belbase": ("Kashyap", "कश्यप"),
    "bidari": ("Kashyap", "कश्यप"),
    "bikral": ("Kaudinya", "कौडिन्य"),
    "chataut": ("Bharadwaj", "भारद्वाज"),
    "chamlagain": ("Bharadwaj", "भारद्वाज"),
    "dangal": ("Kashyap", "कश्यप"),
    "dawadi": ("Atreya", "आत्रेय"),
    "devkota": ("Upamanyu", "उपमन्यु"),
    "dotel/dotiyal": ("Kashyap", "कश्यप"),
    "dulal": ("Atreya", "आत्रेय"),
    "gaire": ("Atreya", "आत्रेय"),
    "gaithaula": ("Atreya", "आत्रेय"),
    "gartola": ("Kaudinya", "कौडिन्य"),
    "gaudel": ("Kaushik", "कौशिक"),
    "ghartel/ghartyal": ("Garga", "गर्ग"),
    "ghartmel": ("Garga", "गर्ग"),
    "ghurcholi": ("Bharadwaj", "भारद्वाज"),
    "gilal": ("Kaudinya", "कौडिन्य"),
    "gotame": ("Gautam", "गौतम"),
    "humagain/hamyagain": ("Kashyap", "कश्यप"),
    "kadariya": ("Bharadwaj", "भारद्वाज"),
    "kandariya": ("Bharadwaj", "भारद्वाज"),
    "kandel/kandyal": ("Bharadwaj", "भारद्वाज"),
    "kaphle/kafle": ("Kaushik", "कौशिक"),
    "koikyal": ("Kashyap", "कश्यप"),
    "dahal": ("Vatsa", "वत्स"),
    "lamsal": ("Vatsa", "वत्स"),
    "rupakheti": ("Vatsa", "वत्स"),
    "neupane/nyaupane": ("Bharadwaj", "भारद्वाज"),
    "oli": ("Bharadwaj", "भारद्वाज"),
    "pageni": ("Kaushik", "कौशिक"),
    "paitola": ("Kashyap", "कश्यप"),
    "pangeni": ("Kaushik", "कौशिक"),
    "phuyal": ("Atreya", "आत्रेय"),
    "punwal": ("Garga", "गर्ग"),
    "purtel": ("Garga", "गर्ग"),
    "rukain": ("Kashyap", "कश्यप"),
    "sangraula/sangroula": ("Kaudinya", "कौडिन्य"),
    "shukla": ("Shandilya", "शाण्डिल्य"),
    "sitaula": ("Bharadwaj", "भारद्वाज"),
    "soti": ("Kaushik", "कौशिक"),
    "subedi": ("Bharadwaj", "भारद्वाज"),
    "suyal": ("Bashista", "वशिष्ठ"),
    "thatal": ("Kashyap", "कश्यप"),
    "tripathi": ("Kashyap", "कश्यप"),
    "upadhyaya/upadhyay": ("Kaudinya / Bharadwaj", "कौडिन्य / भारद्वाज"),
    "airi": ("Kashyap", "कश्यप"),
    "baniya": ("Kashyap", "कश्यप"),
    "baruwal": ("Kaushik", "कौशिक"),
    "basnet/basnyat": ("Kaushik / Bharadwaj", "कौशिक / भारद्वाज"),
    "bhandari": ("Kashyap / Atreya", "कश्यप / आत्रेय"),
    "bista/bisht": ("Kashyap / Atreya", "कश्यप / आत्रेय"),
    "bogati": ("Kashyap", "कश्यप"),
    "bohra/bohara": ("Kashyap", "कश्यप"),
    "budha": ("Kashyap", "कश्यप"),
    "budhaer/budhair": ("Kashyap", "कश्यप"),
    "budhatoki": ("Kashyap / Bharadwaj", "कश्यप / भारद्वाज"),
    "bura": ("Kashyap", "कश्यप"),
    "chhetri": ("Kashyap / Atreya", "कश्यप / आत्रेय"),
    "dangi": ("Kashyap", "कश्यप"),
    "deuba": ("Kashyap", "कश्यप"),
    "dhami": ("Kashyap", "कश्यप"),
    "doeja": ("Kaushik", "कौशिक"),
    "kadayat": ("Kashyap", "कश्यप"),
    "kaji": ("Kashyap", "कश्यप"),
    "karki": ("Maudgalya / Kaushik", "मौद्गल्य / कौशिक"),
    "kathayat": ("Kashyap", "कश्यप"),
    "katawal/katwal/katuwal": ("Kashyap", "कश्यप"),
    "kawar": ("Kashyap", "कश्यप"),
    "khadayat": ("Kashyap", "कश्यप"),
    "khadka/khadga": ("Kaushik / Bharadwaj", "कौशिक / भारद्वाज"),
    "khati": ("Kashyap", "कश्यप"),
    "khatri": ("Atreya / Kashyap", "आत्रेय / कश्यप"),
    "khatri chhetri/k.c.": ("Atreya / Kashyap", "आत्रेय / कश्यप"),
    "khulal": ("Dhananjaya", "धनञ्जय"),
    "kunwar": ("Vatsa", "वत्स"),
    "mahara": ("Kashyap", "कश्यप"),
    "mahat": ("Kashyap", "कश्यप"),
    "mahatara": ("Kashyap", "कश्यप"),
    "dharala": ("Kashyap", "कश्यप"),
    "pahari": ("Kashyap", "कश्यप"),
    "pandey/pande": ("Kashyap / Bharadwaj", "कश्यप / भारद्वाज"),
    "rana": ("Kashyap", "कश्यप"),
    "ranabhat": ("Kashyap", "कश्यप"),
    "raut": ("Kashyap", "कश्यप"),
    "rawal": ("Kashyap", "कश्यप"),
    "rawat": ("Kashyap", "कश्यप"),
    "rayamajhi": ("Kashyap", "कश्यप"),
    "roka/rokaya/rokka": ("Kashyap", "कश्यप"),
    "samant": ("Kashyap", "कश्यप"),
    "sanjel": ("Kaushik", "कौशिक"),
    "sawad/saund/saud": ("Kashyap", "कश्यप"),
    "shamsher/shumsher": ("Kashyap", "कश्यप"),
    "sijapati": ("Kashyap", "कश्यप"),
    "silwal": ("Kashyap", "कश्यप"),
    "sinjali": ("Kashyap", "कश्यप"),
    "thakurathi": ("Kashyap", "कश्यप"),
    "thapa": ("Atreya / Kaushik / Kashyap", "आत्रेय / कौशिक / कश्यप"),
    "woli": ("Bharadwaj", "भारद्वाज"),
}


# Enrich Maudgalya, Sharadwata, and Belbase
GOTRA_DATA["maudgalya"] = {
    "devanagari": "मौद्गल्य",
    "pravara": "Tryarshi (Maudgalya, Angirasa, Bharmyashwa)",
    "kuldevata": "Baraha / Vishnu / Masto",
    "region": "Achham, Jumla, Karnali, Gandaki, Bagmati, Koshi",
    "description": "Descendants of Sage Mudgala, acclaimed for spiritual scholarship and ancient historic birtas in Western Nepal (Timilsain in Achham and Koirali in Bajhang)."
}

GOTRA_DATA["sharadwata"] = {
    "devanagari": "शरद्वत",
    "pravara": "Tryarshi (Gautama, Sharadwata, Kaushika)",
    "kuldevata": "Masto / Mahadev / Kalika",
    "region": "Gandaki, Bagmati, Koshi",
    "description": "Descendants of Sage Sharadwata Gautama, ancient seer associated with Vedic lore, valor, and sacred discipline (Kaphle/Kafle)."
}

FALLBACK_GOTRA["belbase"] = ("Maudgalya", "मौद्गल्य")
FALLBACK_GOTRA["timilsina/timalsina"] = ("Maudgalya", "मौद्गल्य")
FALLBACK_GOTRA["timilsina"] = ("Maudgalya", "मौद्गल्य")
FALLBACK_GOTRA["timalsina"] = ("Maudgalya", "मौद्गल्य")
FALLBACK_GOTRA["pyakurel/pyakuryal"] = ("Kaudinya", "कौडिन्य")
FALLBACK_GOTRA["pyakurel"] = ("Kaudinya", "कौडिन्य")

# Authentic Historic Origins Map (उद्गमस्थल तथा ऐतिहासिक मूलथलो)
HISTORIC_ORIGINS_MAP = {
    # Achham / Jumla / Sinja origins
    "timilsina/timalsina": ("Timilsain, Achham (Karnali-Sinja realm)", "तिमैलसैन, अछाम (सिञ्जा साम्राज्य)"),
    "timilsina": ("Timilsain, Achham (Karnali-Sinja realm)", "तिमैलसैन, अछाम (सिञ्जा साम्राज्य)"),
    "timalsina": ("Timilsain, Achham (Karnali-Sinja realm)", "तिमैलसैन, अछाम (सिञ्जा साम्राज्य)"),
    "timsina": ("Timilsain, Achham (Karnali-Sinja realm)", "तिमैलसैन, अछाम (सिञ्जा साम्राज्य)"),
    "timilsena": ("Timilsain, Achham (Karnali-Sinja realm)", "तिमैलसैन, अछाम (सिञ्जा साम्राज्य)"),
    "neupane/nyaupane": ("Naupani, Jumla (Sinja Valley)", "नौपानी, जुम्ला (सिञ्जा उपत्यका)"),
    "neupane": ("Naupani, Jumla (Sinja Valley)", "नौपानी, जुम्ला (सिञ्जा उपत्यका)"),
    "nyaupane": ("Naupani, Jumla (Sinja Valley)", "नौपानी, जुम्ला (सिञ्जा उपत्यका)"),
    "dahal": ("Daha, Jajarkot / Sinja, Jumla", "दह गाउँ, जाजरकोट / सिञ्जा, जुम्ला"),
    "bhattarai": ("Bhattara, Achham / Jumla", "भट्टरागाउँ, अछाम / जुम्ला"),
    "kaphle/kafle": ("Kaphalna, Achham / Jumla", "काफलना, अछाम / जुम्ला"),
    "kafle": ("Kaphalna, Achham / Jumla", "काफलना, अछाम / जुम्ला"),
    "kaphle": ("Kaphalna, Achham / Jumla", "काफलना, अछाम / जुम्ला"),
    "rijal": ("Rijhi / Rijikhola, Sinja, Jumla", "रिज्जु / रिजिखोला, सिञ्जा, जुम्ला"),
    "pokhrel/pokharel": ("Pokhara village, Rukum (Karnali realm)", "पोखरा गाउँ, रुकुम (कर्णाली प्रदेश)"),
    "pokhrel": ("Pokhara village, Rukum (Karnali realm)", "पोखरा गाउँ, रुकुम (कर्णाली प्रदेश)"),
    "pokharel": ("Pokhara village, Rukum (Karnali realm)", "पोखरा गाउँ, रुकुम (कर्णाली प्रदेश)"),
    "paudel/poudel": ("Paudi, Karnali / Gandaki basin", "पौडी खोला / गाउँ, कर्णाली"),
    "paudel": ("Paudi, Karnali / Gandaki basin", "पौडी खोला / गाउँ, कर्णाली"),
    "poudel": ("Paudi, Karnali / Gandaki basin", "पौडी खोला / गाउँ, कर्णाली"),
    "regmi": ("Regam, Jumla (Sinja Valley)", "रेगाम, जुम्ला (सिञ्जा उपत्यका)"),
    "ghimire/ghimirya": ("Dhamir / Ghamir, Achham", "धामिर / घमिर, अछाम"),
    "ghimire": ("Dhamir / Ghamir, Achham", "धामिर / घमिर, अछाम"),
    "pyakurel/pyakuryal": ("Pyakuri, Sinja, Jumla", "प्याकुरी, सिञ्जा, जुम्ला"),
    "pyakurel": ("Pyakuri, Sinja, Jumla", "प्याकुरी, सिञ्जा, जुम्ला"),
    "subedi": ("Suwa, Jumla (Sinja Valley)", "सुवा, जुम्ला (सिञ्जा उपत्यका)"),
    "koirala": ("Koirali, Achham / Bajhang", "कोइराली, अछाम / बझाङ"),
    "belbase": ("Belbas, Western Nepal / Karnali", "बेलबास, पश्चिम नेपाल / कर्णाली"),
    "lamsal": ("Lamso, Karnali realm", "लाम्सो, कर्णाली प्रदेश"),
    "silwal": ("Silla, Karnali / Western hills", "सिल्ला गाउँ, पश्चिम नेपाल"),
    "sapkota": ("Sapkot, Karnali / Western Nepal", "सापकोट, कर्णाली / पश्चिम नेपाल"),
    "devkota": ("Devkot, Bajura (Karnali realm)", "देवकोट, बाजुरा (कर्णाली प्रदेश)"),
    "chaulagain": ("Chawila, Jumla (Sinja Valley)", "चाविला, जुम्ला (सिञ्जा उपत्यका)"),
    "wagle": ("Wagling, Western Nepal", "वाग्ला, पश्चिम नेपाल"),
    "mainali": ("Mainali, Western Nepal", "मैनाली, पश्चिम नेपाल"),
    "panta": ("Pantana, Doti / Kumaon border", "पन्ताना, डोटी"),
    "aryal": ("Irji, Achham / Karnali realm", "इर्जी, अछाम / कर्णाली"),
    "arjal/arjyal/arjel/aryal": ("Irji, Achham / Karnali realm", "इर्जी, अछाम / कर्णाली"),
    "dhital": ("Dhiti, Jumla (Sinja Valley)", "धिती, जुम्ला (सिञ्जा उपत्यका)"),
    "sigdel": ("Sigdi, Karnali realm", "सिग्दी, कर्णाली प्रदेश"),
    "simkhada": ("Simkhet, Karnali realm", "सिमखेत, कर्णाली प्रदेश"),
    "simkhara": ("Simkhet, Karnali realm", "सिमखेत, कर्णाली प्रदेश"),
    "sinkhada": ("Simkhet, Karnali realm", "सिमखेत, कर्णाली प्रदेश"),
    "kandel/kandyal": ("Kandu, Karnali realm", "कन्दु, कर्णाली प्रदेश"),
    "bajgain": ("Bajhang / Bajura", "बझाङ / बाजुरा"),
    "oli": ("Olla / Wola, Karnali realm", "ओलागाउँ, कर्णाली प्रदेश"),
    "woli": ("Olla / Wola, Karnali realm", "ओलागाउँ, कर्णाली प्रदेश"),
    "parajuli": ("Parajul, Dailekh (Karnali realm)", "पराजुल, दैलेख (कर्णाली प्रदेश)"),
    "khanal": ("Khanigadh, Arghakhanchi / Western hills", "खानीगढ, अर्घाखाँची"),
    "acharya": ("Sinja Valley, Jumla (Khas Imperial Royal Preceptors)", "सिञ्जा उपत्यका, जुम्ला (राजगुरु / आचार्य पीठ)"),
    "kattel": ("Katte, Western Nepal", "कट्टे गाउँ, पश्चिम नेपाल"),
    "khakurel": ("Khaku, Karnali realm", "खाकु, कर्णाली प्रदेश"),
    "bhusal": ("Bhusala, Western Nepal", "भुसाला, पश्चिम नेपाल"),
    "dawadi": ("Dawada, Gandaki / Western hills", "दावाडा, गण्डकी प्रदेश"),
    "duwadi": ("Dawada, Gandaki / Western hills", "दावाडा, गण्डकी प्रदेश"),
    "siwakoti": ("Siwakot, Western hills", "सिवाकोट, पश्चिम नेपाल"),
    "prasai": ("Prasain, Western hills", "प्रसाइँ गाउँ, पश्चिम नेपाल"),
    "rimal": ("Rima, Karnali realm", "रिमा, कर्णाली प्रदेश"),
    "baral": ("Barahakhetra / Baralgadhi, Western hills", "बरालगाउँ, पश्चिम नेपाल"),
    "gautam": ("Gotam, Rukum (Karnali realm)", "गोताम गाउँ, रुकुम"),
    "gotame": ("Gotam, Rukum (Karnali realm)", "गोताम गाउँ, रुकुम"),
    "tiwari": ("Sinja Khas realm / Western hills", "तिवारी गाउँ, पश्चिम नेपाल"),
    "upadhyaya": ("Sinja Valley & Doti (Vedic Priesthood)", "सिञ्जा उपत्यका र डोटी"),
    "upadhyaya/upadhyay": ("Sinja Valley & Doti (Vedic Priesthood)", "सिञ्जा उपत्यका र डोटी"),
    "joshi": ("Sinja Imperial Court Astrologers (Doti & Kathmandu)", "सिञ्जा साम्राज्य (राजज्योतिषी) र डोटी"),
    "pandey/pande": ("Sinja Khas Court Scholars & Ministers", "सिञ्जा साम्राज्य (पण्डित / मन्त्री भारदार)"),
    "pande": ("Sinja Khas Court Scholars & Ministers", "सिञ्जा साम्राज्य (पण्डित / मन्त्री भारदार)"),
    "baskota/banskota": ("Banskota, Western hills", "बाँसकोट, पश्चिम नेपाल"),
    "bastola": ("Bastoli, Western hills", "बास्तोला गाउँ, पश्चिम नेपाल"),
    "basyal/bashyal": ("Basyal, Karnali / Gandaki", "बस्याल गाउँ, कर्णाली"),
    "bhetwal/bhetuwal": ("Bhetuwal, Western hills", "भेटुवाल, पश्चिम नेपाल"),
    "dangal": ("Danga, Western hills", "डाँगा गाउँ, पश्चिम नेपाल"),
    "dulal": ("Dula, Karnali realm", "दुला, कर्णाली प्रदेश"),
    "gaire": ("Gaira, Western hills", "गैरा, पश्चिम नेपाल"),
    "guragain/gurangain": ("Guragaun, Western hills", "गुराँगाउँ, पश्चिम नेपाल"),
    "gyawali": ("Gyawa, Gulmi (Gandaki realm)", "ज्ञावा, गुल्मी"),
    "luitel/luintel": ("Luintel, Western hills", "लुइँटेल, पश्चिम नेपाल"),
    "marashini/marasini": ("Marasin, Gulmi / Western hills", "मरासिन, गुल्मी"),
    "panthi/panthee": ("Pantha, Western hills", "पन्था, पश्चिम नेपाल"),
    "phuyal": ("Phuya, Western hills", "फुयाँ, पश्चिम नेपाल"),
    "sitaula": ("Sitaula, Western hills", "सिटौला गाउँ, पश्चिम नेपाल"),
    "tripathi/tiwary": ("Sinja Khas realm", "सिञ्जा साम्राज्य, कर्णाली"),
    "upreti/uprety": ("Uprada, Western hills / Doti", "उप्राडा, डोटी / सुदूरपश्चिम"),
    "dharala": ("Dharali, Karnali realm", "धराली गाउँ, कर्णाली"),

    # Chhetri / Thakuri administrative & martial titles
    "adhikari": ("Sinja Khas Empire (Chief Administrative Officers)", "सिञ्जा साम्राज्य (प्रशासकीय पद)"),
    "bhandari": ("Sinja Khas Empire (Royal Treasury Keepers)", "सिञ्जा साम्राज्य (राजकीय भण्डार संरक्षक)"),
    "bista": ("Sinja & Doti Courts (Distinguished Courtiers)", "सिञ्जा र डोटी दरबार (विशिष्ट भारदार)"),
    "karki": ("Sinja Khas Empire (Revenue Collectors)", "सिञ्जा साम्राज्य (राजकीय कर अधिकृत)"),
    "khadka": ("Sinja Khas Empire (Royal Swordsmen / Vanguard)", "सिञ्जा साम्राज्य (खड्गधारी अंगरक्षक)"),
    "khadka/khadga": ("Sinja Khas Empire (Royal Swordsmen / Vanguard)", "सिञ्जा साम्राज्य (खड्गधारी अंगरक्षक)"),
    "thapa": ("Sinja Khas Empire (Military Commanders / Generals)", "सिञ्जा साम्राज्य (सेनापति / थापा पदवी)"),
    "basnet/basnyat": ("Basan, Karnali / Salyan principality", "बासन, कर्णाली / सल्यान"),
    "bohora": ("Karnali & Sudurpashchim (Judicial/Revenue Officers)", "कर्णाली र सुदूरपश्चिम (लेखा-प्रशासक)"),
    "mahatara": ("Mahattara (Village Chieftains), Karnali", "महतरा (ग्रामप्रमुख), कर्णाली प्रदेश"),
    "rokay/rokaya/roka": ("Sinja Empire (Rokaya Chieftain Council)", "सिञ्जा साम्राज्य (रोकाया भारदार), कर्णाली"),
    "roka/rokaya/rokka": ("Sinja Empire (Rokaya Chieftain Council)", "सिञ्जा साम्राज्य (रोकाया भारदार), कर्णाली"),
    "budhathoki/budha": ("Sinja Empire Council of Elders (Dwadash Mandala)", "सिञ्जा साम्राज्य (द्वादश मण्डल / बुढाथोकी)"),
    "kunwar": ("Baise/Chaubisi Royal Lineage (Kaski, Gorkha)", "बाइसी/चौबिसी राजपरिवार (कास्की, गोर्खा)"),
    "rana": ("Khas-Magar & Rajput Martial Commanders", "सैन्य कमाण्डर / भित्री राज्यहरू"),
    "shahi/sahi": ("Sinja-Jumla & Jajarkot Thakuri Royal Dynasty", "सिञ्जा-जुम्ला र जाजरकोट राजघराना"),
    "shah": ("Kaski, Lamjung & Gorkha Shah Royal Dynasty", "कास्की, लमजुङ र गोर्खा राजघराना"),
    "malla": ("Sinja Khas Imperial Dynasty & Kathmandu Valley Kings", "सिञ्जा खस साम्राज्य र काठमाडौं उपत्यका"),
    "sen": ("Palpa, Makwanpur & Chaudandi Sen Dynasties", "पाल्पा, मकवानपुर र चौदण्डी सेन वंश"),
    "chand": ("Doti & Baitadi Chand Royal Principalities", "डोटी र बैतडी चन्द ठकुरी रजौटा"),
    "pal": ("Sinja & Askot-Darchula Pal Dynasty", "सिञ्जा र दार्चुला पाल राजवंश"),
    "bam": ("Doti & Bajhang Bam Thakuri Lineage", "डोटी र बझाङ बम ठकुरी"),
    "singh": ("Sinja Empire & Western Principalities", "सिञ्जा साम्राज्य र पश्चिम नेपाल"),
    "rayamajhi": ("Karnali & Western principalities (Ray-Majhi title)", "कर्णाली र पश्चिम नेपाल (रायामाझी पदवी)"),
    "kharel": ("Kharigadh, Western hills", "खरीगढ, पश्चिम नेपाल"),
    "rawat": ("Rawat Royal Guards, Karnali", "राउत (अंगरक्षक), कर्णाली प्रदेश"),
    "baniya": ("Sinja Empire Court Merchants (Baniya Guild)", "सिञ्जा साम्राज्य (दरबारी व्यापारी संघ)"),
    "bania/baniya": ("Sinja Empire Court Merchants (Baniya Guild)", "सिञ्जा साम्राज्य (दरबारी व्यापारी संघ)"),

    # Hill Dalit historic artisanal centers
    "bishwokarma": ("Sinja Khas Civilization (Divine Metallurgists / Architects)", "सिञ्जा खस सभ्यता (शिल्पकार / धातुविज्ञ)"),
    "kami": ("Sinja Khas Civilization (Master Blacksmiths & Weaponsmiths)", "सिञ्जा खस सभ्यता (फलाम तथा हतियार शिल्पी)"),
    "sunar": ("Sinja & Baise Courts (Goldsmiths & Royal Jewelers)", "सिञ्जा र बाइसी राज्यहरू (स्वर्ण शिल्पी)"),
    "tamata": ("Karnali & Sudurpashchim (Copper Artisans)", "कर्णाली र सुदूरपश्चिम (ताम्र शिल्पी)"),
    "lohar": ("Karnali & Terai (Iron Artisans)", "कर्णाली र तराई (लोहा शिल्पी)"),
    "pariyar": ("Sinja & Gandaki (Musical Virtuosos & Royal Couturiers)", "सिञ्जा र गण्डकी (पञ्चैबाजा संरक्षक / वस्त्र शिल्पी)"),
    "damai": ("Sinja & Gandaki (Panche Baja Guardians)", "सिञ्जा र गण्डकी (पञ्चैबाजा बादक)"),
    "sarki": ("Sinja & Western Hills (Master Leather Guilds)", "सिञ्जा र पहाडी राज्यहरू (चर्म शिल्पी)"),
    "mijar": ("Sinja & Western Hills (Leather Guild Chieftains)", "सिञ्जा र पश्चिम नेपाल (मिजार प्रमुख)"),
    "gandharba/gandharva": ("Kaski, Tanahun & Karnali (Folk Minstrels & Balladeers)", "कास्की, तनहुँ र कर्णाली (सुललित गाईने / सारङ्गी साधक)"),
    "gaine": ("Kaski, Tanahun & Karnali (Keepers of Historic Epics)", "कास्की, तनहुँ र कर्णाली (गाथा संरक्षक)"),
    "badi": ("Karnali & Bheri River Basins (Folk Musicians)", "कर्णाली र भेरी जलाधार (लोक संगीतकार)"),
    "thatal": ("Western Hills & Gandaki (Bishwokarma Artisans)", "पश्चिम नेपाल र गण्डकी (विश्वकर्मा शिल्पी)"),

    # Newar historic settlements
    "rajopadhyaya": ("Kathmandu Valley (Pashupatinath & Taleju Royal Preceptors)", "काठमाडौं उपत्यका (पशुपतिनाथ र तलेजु राजपुरोहित)"),
    "shrestha": ("Yen (Kathmandu), Yala (Lalitpur), Khwopa (Bhaktapur)", "काठमाडौं, ललितपुर, भक्तपुर, थिमी, बनेपा"),
    "maharjan": ("Kathmandu & Lalitpur Agricultural Heritage Settlements", "काठमाडौं र ललितपुरका परम्परागत नेवा: वस्तीहरू"),
    "dangol": ("Kathmandu Valley Surveyors & Agrarian Stewards", "काठमाडौं उपत्यका (जग्गा नापजाँच तथा कृषि विशेषज्ञ)"),
    "tuladhar": ("Asan, Kathmandu (Trans-Himalayan Merchant Guilds)", "असन, काठमाडौं (ल्हासा-काठमाडौं तिब्बत व्यापार संघ)"),
    "vajracharya": ("Kathmandu Valley Buddhist Viharas & Bahals", "काठमाडौं उपत्यकाका ऐतिहासिक विहार तथा बहालहरू"),
    "shakya": ("Patan / Lalitpur Bahals (Gold, Silver & Bronze Sculptors)", "ललितपुरका महाविहारहरू (धातु मूर्ति शिल्पी)"),
    "pradhan": ("Patan & Kathmandu Valley Courtiers", "ललितपुर र काठमाडौं (प्रधान भारदार)"),
    "amatya": ("Bhaktapur & Patan Royal Ministers", "भक्तपुर र पाटन (अमात्य मन्त्री)"),
    "rajbhandari": ("Kathmandu & Bhaktapur Taleju Treasurers", "काठमाडौं र भक्तपुर तलेजु भण्डारी"),
    "kamsakar": ("Kel Tole, Kathmandu (Bronze Artisans)", "केलटोल, काठमाडौं (काँस शिल्पी)"),
    "tamrakar": ("Patan & Maru, Kathmandu (Copper Artisans)", "पाटन र मरु, काठमाडौं (ताम्र शिल्पी)"),
    "shilpakar": ("Bhaktapur (Master Woodcarvers & Architects)", "भक्तपुर (काष्ठकला तथा मन्दिर शिल्पी)"),
    "chitrakar": ("Kathmandu Valley (Paubha & Sacred Mural Painters)", "काठमाडौं उपत्यका (पौभा तथा भित्तेचित्रकार)"),
    "suwal": ("Bhaktapur (Agrarian and Brick Guild Stewards)", "भक्तपुरका ऐतिहासिक नेवा: वस्तीहरू"),
    "byanjankar": ("Chyasal, Lalitpur", "च्यासल, ललितपुर"),
    "awale": ("Lalitpur (Pottery Artisans)", "ललितपुर (मृत्तिका शिल्पी)"),
    "prajapati": ("Bhaktapur & Thimi (Master Ceramicists & Potters)", "भक्तपुर र थिमी (माटोका भाँडा शिल्पी)"),

    # Indigenous Janajati historic homelands
    "rai": ("Majh Kirat (Dudh Koshi & Arun basins: Bhojpur, Khotang, Okhaldhunga)", "माझ किरात (खोटाङ, भोजपुर, ओखलढुङ्गा, सोलुखुम्बु)"),
    "limbu": ("Limbuwan / Pallo Kirat (Tamor basin: Taplejung, Panchthar, Ilam)", "लिम्बुवान (ताप्लेजुङ, पाँचथर, इलाम, तेह्रथुम)"),
    "yakthung": ("Limbuwan / Pallo Kirat (Tamor basin: Taplejung, Panchthar, Ilam)", "लिम्बुवान (ताप्लेजुङ, पाँचथर, इलाम, तेह्रथुम)"),
    "magar": ("Barha Magarat & Athara Magarat (Palpa, Gulmi, Syangja, Rolpa, Rukum)", "बाह्र मगरात र अठार मगरात (पाल्पा, गुल्मी, रोल्पा, रुकुम)"),
    "gurung": ("Tamuwan (Annapurna Himalayan slopes: Lamjung, Kaski, Gorkha)", "तमुवान (लमजुङ, कास्की, गोर्खा, मनाङ)"),
    "tamang": ("Tamsaling (Mahabharat range: Kavre, Sindhupalchok, Nuwakot, Makwanpur)", "ताम्सालिङ (काभ्रे, सिन्धुपाल्चोक, नुवाकोट, मकवानपुर)"),
    "tharu": ("Tharuhat (Terai forest plains: Dang, Chitwan, Kailali, Bardiya)", "थरुहट (दाङ, चितवन, कैलाली, बर्दिया, कञ्चनपुर)"),
    "sunuwar": ("Koinchwan (Likhu & Khimti basins: Ramechhap, Okhaldhunga)", "कोइँचवान (रामेछाप, ओखलढुङ्गा, दोलखा)"),
    "sherpa": ("Solukhumbu & High Himalayan Valleys (Khumbu, Rolwaling)", "सोलुखुम्बु र उच्च हिमाली उपत्यकाहरू"),
    "thakali": ("Thak Khola, Mustang (Kali Gandaki Trade Basin)", "थाक खोला, मुस्ताङ (कालीगण्डकी व्यापारिक मार्ग)"),
    "chepang": ("Mahabharat forest ridges (Chitwan, Makwanpur, Dhading)", "महाभारत वनक्षेत्र (चितवन, मकवानपुर, धादिङ)"),
    "praja": ("Mahabharat forest ridges (Chitwan, Makwanpur, Dhading)", "महाभारत वनक्षेत्र (चितवन, मकवानपुर, धादिङ)"),
    "rajbanshi": ("Jhapa & Morang (Koch-Rajbanshi historic kingdom)", "झापा र मोरङ (कोच-राजवंशी ऐतिहासिक क्षेत्र)"),
    "danuwar": ("Kamala & Bagmati river valleys (Sindhuli, Udayapur)", "सिन्धुली, उदयपुर र सर्लाहीका नदी उपत्यका"),
    "majhi": ("Sun Koshi, Tama Koshi & Saptakoshi river confluences", "सुनकोशी, तामाकोशी र सप्तकोशी तटीय क्षेत्र"),
    "kumal": ("Gandaki, Narayani & Rapti river valleys (Master Potters)", "गण्डकी, नारायणी र राप्ती नदी उपत्यका"),
    "yakkha": ("Yakkhaba homeland (Sankhuwasabha & Dhankuta)", "सङ्खुवासभा र धनकुटा"),
    "jirel": ("Jiri Valley, Dolakha", "जिरी उपत्यका, दोलखा"),
    "lepcha": ("Ilam & Kanchenjunga foothills", "इलाम र कञ्चनजङ्घा क्षेत्र"),

    # Madhesi / Terai homelands
    "yadav": ("Mithila Realm & Central Terai plains (Janakpur, Siraha, Saptari)", "प्राचीन मिथिला क्षेत्र (धनुषा, महोत्तरी, सिराहा, सप्तरी)"),
    "jha": ("Mithila Brahmin heartland (Janakpurdham, Madhesh)", "जनकपुरधाम, प्राचीन मिथिला क्षेत्र"),
    "mishra": ("Mithila Brahmin heartland (Janakpurdham, Madhesh)", "जनकपुरधाम, प्राचीन मिथिला क्षेत्र"),
    "thakur": ("Mithila & Bhojpuri plains", "मिथिला र भोजपुरी भूभाग"),
    "mahato": ("Central and Eastern Terai plains (Siraha, Dhanusha, Sarlahi)", "मध्य र पूर्वी तराई (सिराहा, धनुषा, सर्लाही)"),
    "sah": ("Mithila & Bhojpuri trade centers", "तराई-मधेशका ऐतिहासिक व्यापारिक केन्द्रहरू"),
    "gupta": ("Terai commerce towns (Birgunj, Janakpur, Biratnagar)", "तराई-मधेशका मुख्य व्यापारिक नगरहरू"),
    "mandal": ("Mithila agrarian heartland (Dhanusha, Mahottari, Siraha)", "मिथिला कृषि भूभाग (धनुषा, महोत्तरी, सिराहा)"),
    "chaudhary": ("Tharuhat & Mithila agrarian leadership", "तराई-मधेश र थरुहट क्षेत्र"),

    # Terai Dalit
    "chamar": ("Central & Eastern Terai plains (Dhanusha, Siraha, Sarlahi)", "मध्य तथा पूर्वी तराई भूभाग"),
    "paswan": ("Central & Eastern Terai plains (Raja Salhesh heritage)", "मध्य तथा पूर्वी तराई (राजा सलहेस परम्परा)"),
    "musahar": ("Terai agrarian plains (Dinanbhadri oral heritage)", "तराईका कृषिक्षेत्र (दीनाभद्री परम्परा)"),
    "dom": ("Terai municipal & cultural settlements", "तराई-मधेशका बस्तीहरू"),

    # Muslim
    "ansari": ("Terai border districts & historic weavers", "तराई-मधेशका ऐतिहासिक वस्तीहरू"),
    "sheikh": ("Terai commerce & cultural centers", "तराई-मधेशका ऐतिहासिक नगरहरू"),
    "pathan": ("Terai historic settlements", "तराई-मधेशका बस्तीहरू"),
    "kashmiri": ("Kathmandu Valley (Malla-era merchant quarter)", "काठमाडौं उपत्यका (मल्लकालीन कश्मीरी तकिया)")
}

def resolve_historic_origin(s_key, comm_norm, category, clan_words):
    # 1. Exact match in HISTORIC_ORIGINS_MAP
    if s_key in HISTORIC_ORIGINS_MAP:
        return HISTORIC_ORIGINS_MAP[s_key]
    
    # 2. Part before slash
    if "/" in s_key:
        p1 = s_key.split("/")[0].strip()
        if p1 in HISTORIC_ORIGINS_MAP:
            return HISTORIC_ORIGINS_MAP[p1]

    # 3. Substring match (require length >= 4 to avoid false matches like 'rai' in 'barai')
    for k, v in HISTORIC_ORIGINS_MAP.items():
        if len(k) >= 4 and (k in s_key or s_key in k):
            return v

    # 4. Community/Category defaults
    cn_lower = comm_norm.lower()
    cat_lower = category.lower()

    if "madhesi" in cat_lower or "tarai" in cat_lower or "maithil" in cn_lower:
        return ("Ancient Mithila & Terai-Madhesh plains", "प्राचीन मिथिला तथा तराई-मधेश भूभाग")
    elif "muslim" in cat_lower:
        return ("Terai-Madhesh & Historic Trade Centers", "तराई-मधेश तथा ऐतिहासिक व्यापारिक केन्द्रहरू")
    elif "dalit" in cat_lower or "dalit" in cn_lower:
        if "tarai" in cn_lower:
            return ("Central & Eastern Terai plains", "मध्य तथा पूर्वी तराई भूभाग")
        return ("Karnali-Khas Civilization & Western hills", "कर्णाली-खस सभ्यता तथा पहाडी भूभाग")
    elif "bahun" in cn_lower:
        return ("Sinja Valley & Western Karnali realm (स्थाननाम/विर्ता परम्परा)", "सिञ्जा उपत्यका तथा कर्णाली भूभाग (स्थाननाम/विर्ता परम्परा)")
    elif "chhetri" in cn_lower:
        return ("Khas Empire & Western principalities (कर्णाली/गण्डकी)", "खस साम्राज्य तथा बाइसी-चौबिसी राज्यहरू (कर्णाली/गण्डकी)")
    elif "thakuri" in cn_lower:
        return ("Karnali-Jumla, Doti & Baise-Chaubisi Royal Principalities", "सिञ्जा-जुम्ला, डोटी र बाइसी-चौबिसी राजदरबार")
    elif "newar" in cat_lower or "newar" in cn_lower:
        return ("Kathmandu Valley historic settlements (Yen, Yala, Khwopa)", "काठमाडौं उपत्यकाका ऐतिहासिक नेवा: वस्तीहरू")
    elif "limbu" in cn_lower:
        return ("Limbuwan / Pallo Kirat (Taplejung, Panchthar, Ilam, Sankhuwasabha)", "लिम्बुवान (ताप्लेजुङ, पाँचथर, इलाम, तेह्रथुम)")
    elif re.search(r'\brai\b', cn_lower) and "tarai" not in cn_lower:
        return ("Majh Kirat (Bhojpur, Khotang, Okhaldhunga, Solukhumbu)", "माझ किरात (भोजपुर, खोटाङ, ओखलढुङ्गा, सोलुखुम्बु)")
    elif "magar" in cn_lower:
        return ("Barha Magarat & Athara Magarat (Palpa, Gulmi, Syangja, Rolpa)", "बाह्र मगरात र अठार मगरात (पाल्पा, गुल्मी, रोल्पा)")
    elif "gurung" in cn_lower:
        return ("Tamuwan (Lamjung, Kaski, Gorkha, Manang)", "तमुवान (लमजुङ, कास्की, गोर्खा, मनाङ)")
    elif "tamang" in cn_lower:
        return ("Tamsaling (Kavre, Sindhupalchok, Nuwakot, Makwanpur)", "ताम्सालिङ (काभ्रे, सिन्धुपाल्चोक, नुवाकोट, मकवानपुर)")
    elif "tharu" in cn_lower:
        return ("Tharuhat (Dang, Chitwan, Kailali, Bardiya, Morang)", "थरुहट (दाङ, चितवन, कैलाली, बर्दिया, मोरङ)")

    return ("Historic Nepali ancestral settlements", "नेपालका ऐतिहासिक परम्परागत वस्तीहरू")

TARAI_HINDU_CLAN_MAP = {
    "kayastha": "Kayastha", "rajput": "Rajput", "vaishya": "Baniyan", "bania": "Baniyan",
    "baniya": "Baniyan", "barai": "Baraee", "badhai": "Badhee", "badahi": "Badhee",
    "teli": "Teli", "koiri": "Koiri/Kushwaha", "kushwaha": "Koiri/Kushwaha", "kurmi": "Kurmi",
    "kanu": "Kanu", "halwai": "Halwai", "kahar": "Kahar", "lodh": "Lodh", "mali": "Mali",
    "mallaha": "Mallaha", "kewat": "Kewat", "bhumihar": "Bhumihar", "beldar": "Beldar",
    "sudhi": "Sundi", "sundi": "Sundi", "sonar": "Sonar", "nuniya": "Nuniya",
    "kumhar": "Kumhar/Kohar", "kohar": "Kumhar/Kohar", "kamhar": "Kumhar/Kohar", "dhobi": "Dhobi",
    "tatma": "Tatma/Tatwa", "tatwa": "Tatma/Tatwa", "khatik": "Khatik", "chamar": "Chamar/Harijan/Ram",
    "harijan": "Chamar/Harijan/Ram", "ram": "Chamar/Harijan/Ram", "dusadh": "Dusadh/Pasawan/Pasi",
    "dushadh": "Dusadh/Pasawan/Pasi", "paswan": "Dusadh/Pasawan/Pasi", "pasi": "Dusadh/Pasawan/Pasi",
    "musahar": "Musahar", "bantar": "Bantar", "dom": "Dom", "halkhor": "Halkhor",
    "mestar": "Halkhor", "dharikar": "Dharikar", "dhankar": "Dharikar", "chidimar": "Chidimar", "kori": "Kori"
}

TARAI_SURNAMES_DIRECT = {
    "amast": "Kayastha", "bhatnagar": "Kayastha", "karna": "Kayastha", "shrivastav": "Kayastha",
    "shrivastava": "Kayastha", "bachhgoti chauhan": "Rajput", "beduwar": "Rajput", "bisen": "Rajput",
    "garbhar": "Rajput", "singh": "Rajput", "chauhan": "Rajput", "rathore": "Rajput", "badahi": "Badhee",
    "barai": "Baraee", "chaurasiya": "Baraee", "bhagat": "Koiri/Kushwaha", "mahato": "Koiri/Kushwaha",
    "kushwaha": "Koiri/Kushwaha", "patel": "Kurmi", "chaudhary": "Tharu", "sah": "Teli", "sahu": "Teli",
    "teli": "Teli", "gupta": "Baniyan", "rauniyar": "Rauniyar", "bania/baniya": "Baniyan",
    "baniya": "Baniyan", "yadav": "Yadav", "ahir": "Yadav", "ray": "Yadav", "gautam": "Rajput",
    "gwala": "Yadav", "hajam": "Hajam/Thakur", "thakur": "Brahman - Tarai", "jha": "Brahman - Tarai",
    "mishra": "Brahman - Tarai", "pathak": "Brahman - Tarai", "chaturvedi": "Brahman - Tarai",
    "tripathi": "Brahman - Tarai", "tiwari": "Brahman - Tarai", "shukla": "Brahman - Tarai",
    "pandey": "Brahman - Tarai", "bhatta": "Brahman - Tarai", "dixit/dikshit": "Brahman - Tarai",
    "das": "Tatma/Tatwa", "chamar": "Chamar/Harijan/Ram", "ram": "Chamar/Harijan/Ram",
    "dushadh": "Dusadh/Pasawan/Pasi", "halkhor": "Halkhor", "dom": "Dom", "musahar": "Musahar",
    "dhandi": "Dhangar/Jhangad", "bantar": "Bantar", "dharikar/dhankar": "Dharikar",
    "chidimar": "Chidimar", "dhobi": "Dhobi", "kori": "Kori", "kewat": "Kewat", "mallaha": "Mallaha",
    "kumhar": "Kumhar/Kohar", "kohar": "Kumhar/Kohar", "kamhar": "Kumhar/Kohar", "dhanuk": "Dhanuk",
    "mandal": "Dhanuk", "nuniya": "Nuniya", "halwai": "Halwai", "kanu": "Kanu", "bhihar": "Bhumihar"
}

def match_census_data(comm_norm, category, s_key, clan_words):
    comm = comm_norm.lower()
    cat = category.lower()
    clan_lower = " ".join(clan_words).lower()

    # Census map lookup
    c_map = {c['caste'].lower(): c for c in CENSUS_LIST}

    # 1. Direct Tarai surname mapping
    if s_key in TARAI_SURNAMES_DIRECT:
        t = TARAI_SURNAMES_DIRECT[s_key]
        if t.lower() in c_map:
            c = c_map[t.lower()]
            return c['caste'], c['population'], c['rank'], c['percent']

    # 2. Check clan/subcaste in TARAI_HINDU_CLAN_MAP
    for k, t in TARAI_HINDU_CLAN_MAP.items():
        if k in clan_lower or k in comm:
            if t.lower() in c_map:
                c = c_map[t.lower()]
                return c['caste'], c['population'], c['rank'], c['percent']

    # 3. Khas-Arya Brahmin / Chhetri / Thakuri / Sanyasi
    if "bahun" in comm or "brahman (purbiya)" in comm or "kumai" in comm:
        c = c_map['brahman - hill']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "thakuri" in comm:
        c = c_map['thakuri']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "chhetri" in comm or "khas-chhetri" in comm:
        c = c_map['kshetri']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "sanyasi" in comm or "dashnami" in comm:
        c = c_map['sanyasi/dasnami']
        return c['caste'], c['population'], c['rank'], c['percent']

    # 4. Hill Dalits
    if any(k in comm or k in clan_lower or k in s_key for k in ["bishwokarma", "kami", "sunar", "lohar", "tamata", "thatal", "darnal"]):
        c = c_map['bishwokarma']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif any(k in comm or k in clan_lower or k in s_key for k in ["pariyar", "damai", "suchikar", "dholi", "darji"]):
        c = c_map['pariyar']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif any(k in comm or k in clan_lower or k in s_key for k in ["mijar", "sarki", "charmakar", "bhul", "roka"]):
        c = c_map['mijar']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "badi" in comm or "badi" in s_key:
        c = c_map['badi']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif any(k in comm or k in clan_lower or k in s_key for k in ["gaine", "gandharba", "gandharva"]):
        c = c_map['gaine']
        return c['caste'], c['population'], c['rank'], c['percent']

    # 5. Major Nationalities
    if "newar" in comm or cat == "newar":
        c = c_map['newa: (newar)']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "magar" in comm:
        c = c_map['magar']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "tharu" in comm:
        c = c_map['tharu']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "tamang" in comm:
        c = c_map['tamang']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "gurung" in comm:
        c = c_map['gurung']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "limbu" in comm or "yakthung" in comm:
        c = c_map['yakthung/limbu']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif re.search(r'\brai\b', comm) and "tarai" not in comm:
        c = c_map['rai']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "sherpa" in comm:
        c = c_map['sherpa']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "sunuwar" in comm:
        c = c_map['sunuwar']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "jirel" in comm:
        c = c_map['jirel']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "danuwar" in comm:
        c = c_map['danuwar']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "kumal" in comm:
        c = c_map['kumal']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "majhi" in comm:
        c = c_map['majhi']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "thakali" in comm:
        c = c_map['thakali']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "chepang" in comm:
        c = c_map['chepang/praja']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "rajbanshi" in comm or "rajbansi" in comm:
        c = c_map['rajbansi']
        return c['caste'], c['population'], c['rank'], c['percent']
    elif "muslim" in comm or cat == "muslim":
        c = c_map['musalman']
        return c['caste'], c['population'], c['rank'], c['percent']

    # Fallback for remaining Tarai
    if "tarai" in comm or cat == "madhesi / terai":
        c = c_map.get('brahman - tarai') if 'brahman' in comm else c_map.get('yadav')
        if c:
            return c['caste'], c['population'], c['rank'], c['percent']

    return "", 0, 0, 0.0

records = []
id_counter = 1

for num, line in matches:
    parts = [p.strip() for p in line.split('>')]
    if not parts or not parts[0]:
        continue

    surname_raw = parts[0].strip()
    comm_raw = parts[1].strip() if len(parts) > 1 else ""
    clan_raw = parts[2].strip() if len(parts) > 2 else ""

    # Fact-checking filters
    if surname_raw.lower() == "acharya" and "newar" in comm_raw.lower():
        continue
    if surname_raw.lower() == "agnihotri" and "newar" in comm_raw.lower():
        continue
    if surname_raw.lower() == "chaurasiya":
        comm_raw = "Tarai-Hindu"
        clan_raw = "Barai"
    if surname_raw.lower() == "giri" and "newar" in comm_raw.lower():
        continue
    if surname_raw.lower() == "pant" and "newar" in comm_raw.lower():
        continue
    if surname_raw.lower() == "sahi" and "tamang" in comm_raw.lower():
        continue
    if surname_raw.lower() == "jha" and "newar" in comm_raw.lower():
        continue
    if surname_raw.lower() == "mishra" and "newar" in comm_raw.lower():
        continue
    if surname_raw.lower() == "bhatta" and "newar" in comm_raw.lower():
        continue
    if surname_raw.lower() == "khas" and "tharu" in comm_raw.lower():
        continue
    if surname_raw.lower() == "chataut" and any(r["surname"] == "Chataut" for r in records):
        continue
    if surname_raw.lower() == "dev" and "newar" in comm_raw.lower():
        continue
    if surname_raw.lower() == "sharma" and "newar" in comm_raw.lower():
        continue
    if surname_raw.lower() == "thatal":
        comm_raw = "Dalit"
        clan_raw = "Bishwokarma"

    if comm_raw.lower() == "chan" and len(parts) > 2 and parts[2].lower() == "magar":
        comm_raw = "Magar"
        clan_raw = "Chan"

    comm_norm = comm_raw
    c_lower = comm_raw.lower()

    if c_lower in ["chhetri", "khas-chhetri"]:
        comm_norm = "Khas-Chhetri"
    elif c_lower in ["dalt", "dalit"]:
        comm_norm = "Dalit"
    elif c_lower in ["bahun (purbiya)", "bahun"]:
        comm_norm = "Bahun"
    elif "newar uray" in c_lower or "udhas" in c_lower:
        comm_norm = "Newar-Buddhist"
        if not clan_raw:
            clan_raw = "Uray / Udhas"
    elif "newar nau" in c_lower:
        comm_norm = "Newar"
        clan_raw = "Nau (Napit)"

    cn_words = set(re.findall(r'[a-z]+', comm_norm.lower()))
    clan_words = set(re.findall(r'[a-z]+', clan_raw.lower()))
    s_key = surname_raw.lower().strip()

    category = "Other"
    if "dalit" in cn_words or "dalit" in clan_words:
        category = "Dalit"
    elif "tarai" in cn_words or "maithil" in cn_words or "maithili" in cn_words:
        category = "Madhesi / Terai"
    elif "muslim" in cn_words:
        category = "Muslim"
    elif "newar" in cn_words:
        category = "Newar"
    elif any(w in cn_words for w in ["bahun", "chhetri", "thakuri", "dashnami", "sanyasi"]):
        category = "Khas-Arya"
    elif any(w in cn_words for w in ["magar", "tamang", "gurung", "tharu", "limbu", "rai", "sunuwar", "jirel", "thakali", "sherpa", "chepang", "rajbanshi"]):
        category = "Indigenous Janajati"

    display_community = comm_norm
    if comm_norm == "Bahun":
        display_community = "Bahun (Khas Brahmin)"
    elif comm_norm == "Khas-Chhetri":
        display_community = "Khas-Chhetri (Kshatriya)"
    elif comm_norm == "Thakuri":
        display_community = "Thakuri (Royal / Aristocratic)"
    elif comm_norm == "Dalit":
        display_community = "Hill Dalit"
    elif comm_norm == "Tarai-Dalit":
        display_community = "Tarai Dalit"
    elif comm_norm == "Tarai-Hindu":
        display_community = "Madhesi / Tarai Hindu"
    elif comm_norm == "Tarai-Brahman":
        display_community = "Tarai Brahmin (Maithil / Tirhute)"

    devanagari = DEVANAGARI_MAP.get(s_key, "")
    if not devanagari and "/" in s_key:
        first_part = s_key.split("/")[0].strip()
        devanagari = DEVANAGARI_MAP.get(first_part, "")

    gotra_text = ""
    gotra_deva = ""
    subcaste_text = re.sub(r'\bbatsa\b', 'Vatsa', clan_raw, flags=re.IGNORECASE)
    pravara_text = ""
    kuldevata_text = ""
    region_text = ""
    notes_text = ""

    matched_gotra_key = None

    # Specific gotra overrides
    if s_key in ["timilsina/timalsina", "timilsina", "timalsina", "timsina", "timilsena", "timalsena"]:
        matched_gotra_key = "maudgalya"
        gotra_text = "Maudgalya"
        gotra_deva = "मौद्गल्य"
        pravara_text = "Tryarshi (Maudgalya, Angirasa, Bharmyashwa / त्र्यार्षेय: मौद्गल्य, आङ्गिरस, भार्म्यश्व)"
        kuldevata_text = "Masto (Dhadar / Babiro Masto), Bandevi, Baraha"
        subcaste_text = "Maudgalya (Purbiya Khas-Bahun)"
        origin_text = "Timilsain, Achham (Karnali-Sinja realm)"
        origin_deva = "तिमैलसैन, अछाम (सिञ्जा साम्राज्य)"
        surname_raw = "Timilsina / Timalsina / Timilsena / Timalsena / Timsina"
        devanagari = "तिमिल्सिना / तिमल्सिना / तिमिल्सेना / तिमल्सेना / तिम्सिना"
        notes_text = "Descendants of Sage Mudgala originating from Timilsain village in Achham (granted in 608 BS by Sinjapati King Mayurbhanjanpal to Ila, Visha, and Basu Bhatta). Historically and doctrinally of Maudgalya (मौद्गल्य) Gotra; often mistakenly categorized as Mandabya in informal lists."
    elif s_key == "belbase":
        matched_gotra_key = "maudgalya"
        gotra_text = "Maudgalya"
        gotra_deva = "मौद्गल्य"
        subcaste_text = "Maudgalya (Khas-Bahun)"
    elif s_key in ["pyakurel/pyakuryal", "pyakurel"]:
        matched_gotra_key = "kaudinya"
        gotra_text = "Kaudinya"
        gotra_deva = "कौडिन्य"
        subcaste_text = "Kaudinya (Purbiya / Khas-Bahun)"
    elif s_key == "sapkota":
        matched_gotra_key = "kaushik"
        gotra_text = "Kaushik"
        gotra_deva = "कौशिक"
        subcaste_text = "Kaushik (Purbiya)"
    elif s_key in ["neupane/nyaupane", "neupane", "nyaupane"]:
        matched_gotra_key = "upamanyu"
        gotra_text = "Upamanyu"
        gotra_deva = "उपमन्यु"
    elif s_key in ["oli", "woli"]:
        matched_gotra_key = "shandilya"
        gotra_text = "Shandilya"
        gotra_deva = "शाण्डिल्य"
    elif s_key in ["kaphle/kafle", "kafle", "kaphle"]:
        matched_gotra_key = "sharadwata"
        gotra_text = "Sharadwata"
        gotra_deva = "शरद्वत"
    elif s_key == "silwal":
        matched_gotra_key = "bharadwaj"
        gotra_text = "Bharadwaj"
        gotra_deva = "भारद्वाज"
    elif "batsa" in clan_words or "batsa" in clan_raw.lower() or "vatsa" in clan_words or "vatsa" in clan_raw.lower():
        matched_gotra_key = "vatsa"
        gotra_text = "Vatsa"
        gotra_deva = "वत्स"
    elif "dhananjay" in clan_raw.lower():
        matched_gotra_key = "dhananjaya"
        gotra_text = "Dhananjaya"
        gotra_deva = "धनञ्जय"
    else:
        for gk in GOTRA_DATA.keys():
            if gk in clan_words or gk in clan_raw.lower():
                matched_gotra_key = gk
                break

    if not matched_gotra_key and s_key in FALLBACK_GOTRA:
        fb_gotra, fb_deva = FALLBACK_GOTRA[s_key]
        gotra_text = fb_gotra
        gotra_deva = fb_deva
        for gk in GOTRA_DATA.keys():
            if gk in fb_gotra.lower():
                matched_gotra_key = gk
                break

    if matched_gotra_key in ["batsa", "vatsa"]:
        matched_gotra_key = "vatsa"
        gotra_text = "Vatsa"
        gotra_deva = "वत्स"

    if matched_gotra_key:
        ginfo = GOTRA_DATA[matched_gotra_key]
        if not gotra_text:
            gotra_text = matched_gotra_key.capitalize()
            gotra_deva = ginfo["devanagari"]
        pravara_text = ginfo["pravara"]
        kuldevata_text = ginfo["kuldevata"]
        region_text = ginfo["region"]
        notes_text = ginfo["description"]
    elif gotra_text and not gotra_deva:
        for gk, ginfo in GOTRA_DATA.items():
            if gk in gotra_text.lower():
                gotra_deva = ginfo["devanagari"]
                pravara_text = ginfo["pravara"]
                kuldevata_text = ginfo["kuldevata"]
                region_text = ginfo["region"]
                notes_text = ginfo["description"]
                break

    # Resolve authentic historic origin
    origin_text, origin_deva = resolve_historic_origin(s_key, comm_norm, category, clan_words)

    # Match census data
    census_caste, census_pop, census_rank, census_pct = match_census_data(comm_norm, category, s_key, clan_words)

    # Specific ethnic enrichments if not Vedic gotra
    if category == "Newar":
        if s_key == "rajopadhyaya":
            gotra_text = "Garga / Bharadwaj / Kaushik"
            gotra_deva = "गर्ग / भारद्वाज / कौशिक"
            pravara_text = "Tryarshi (Garga, Angirasa, Barhaspatya)"
            kuldevata_text = "Taleju Bhawani / Digu Dya / Pashupatinath"
            notes_text = "Devabhaju / Rajopadhyaya Vedic Brahmins of Kathmandu Valley, royal preceptors and temple priests of Taleju and Pashupatinath since the Malla era."
        elif not gotra_text:
            gotra_text = "Guthi / Clan Lineage"
            gotra_deva = "गुठी / वंश"
        if not kuldevata_text:
            kuldevata_text = "Digu Dya (दिगु द्यः / Clan Deity), Taleju Bhawani, Karunamaya"
        if not region_text:
            region_text = "Kathmandu Valley (Kathmandu, Lalitpur, Bhaktapur, Thimi, Kirtipur)"
        if "shrestha" in clan_raw.lower() or "kshatriya" in comm_norm.lower():
            notes_text = "High-ranking Newar nobility, administrators, and historic courtiers of the Malla and Shah eras."
        elif "jyapu" in clan_raw.lower() or "maharjan" in s_key or "dangol" in s_key:
            notes_text = "Custodians of Kathmandu Valley's indigenous agricultural science, traditional festivals, Guthi institutions, and sacred musical ensembles."
        elif "uray" in clan_raw.lower() or "tuladhar" in s_key or "kamsakar" in s_key:
            notes_text = "Historic Buddhist merchant and artisanal guilds of Kathmandu, famous for trans-Himalayan trade between Nepal and Tibet (Lhasa)."
        elif "brahman" in comm_norm.lower() or "rajopadhyaya" in clan_raw.lower():
            notes_text = "Devabhaju / Rajopadhyaya Vedic Brahmins, serving as primary royal preceptors and temple priests of Taleju and Pashupatinath."
        elif "vajracharya" in s_key or "shakya" in s_key or "bare" in clan_raw.lower():
            notes_text = "Hereditary Buddhist masters (Gubhaju) and monks/philosophers (Bare), preservers of Sanskrit Vajrayana Buddhism."
        elif not notes_text:
            notes_text = "Integral guild community in the centuries-old cultural, religious, and economic fabric of the Newar civilization."

    elif category == "Indigenous Janajati":
        if s_key == "praja":
            gotra_text = "Chepang Clan / Thar"
            gotra_deva = "चेपाङ कुल / थर"
            kuldevata_text = "Namrung (Forest & Hunting Deity), Ancestral Spirits"
            region_text = "Chitwan, Makwanpur, Dhading, Gorkha (Mahabharat range)"
            notes_text = "Indigenous semi-nomadic community of the central Mahabharat hills with profound knowledge of forest ecology and traditional shamanic rites."
        elif s_key == "rajbanshi":
            gotra_text = "Koch / Rajbanshi Lineage"
            gotra_deva = "कोच / राजवंशी कुल"
            kuldevata_text = "Thakurani / Gram Devata / Kali"
            region_text = "Jhapa & Morang (Eastern Terai)"
            notes_text = "Indigenous Koch-Rajbanshi community of Eastern Nepal with ancient historical roots in the Koch kingdom and rich agrarian festivals."
        elif "limbu" in cn_words:
            gotra_text = "Kirat Mundhum (Samet / Phaid)"
            gotra_deva = "मुन्धुम (सामेत / फैद)"
            if not kuldevata_text:
                kuldevata_text = "Yuma Sammang, Theba Sammang (Mundhum tradition)"
            if not region_text:
                region_text = "Koshi Province (Limbuwan: Taplejung, Panchthar, Ilam, Sankhuwasabha, Tehrathum)"
            notes_text = "Indigenous Yakthungba people of Eastern Nepal. Social organization governed by ancient Mundhum scriptures and clan (Samet/Phaid) exogamy."
        elif "rai" in cn_words:
            gotra_text = "Kirat Mundhum (Phaid / Pachha)"
            gotra_deva = "मुन्धुम (फैद / पाछा)"
            if not kuldevata_text:
                kuldevata_text = "Sumnima-Paruhang, Suptulung (Three sacred hearth stones)"
            if not region_text:
                region_text = "Koshi Province (Majh Kirat: Bhojpur, Khotang, Solukhumbu, Okhaldhunga, Udayapur)"
            notes_text = "Indigenous Kirat Khambu nation with 28+ distinct linguistic lineages, celebrating nature and harvest during Sakela (Ubhauli & Udhauli)."
        elif "magar" in cn_words:
            gotra_text = "Magarat Thar (7 Major Divisions)"
            gotra_deva = "मगरात थर"
            if not kuldevata_text:
                kuldevata_text = "Bhume / Baraha / Mandali"
            if not region_text:
                region_text = "Gandaki & Lumbini (Palpa, Tanahun, Gulmi, Syangja, Rolpa, Baglung, Myagdi)"
            notes_text = "One of Nepal's largest indigenous nationalities with distinct Thar divisions (Thapa, Rana, Pun, Ale, Gharti, Buda, Roka). Renowned martial and agrarian traditions."
        elif "tamang" in cn_words:
            gotra_text = "Rhu / Thar (Clan Lineage)"
            gotra_deva = "रु / थर"
            if not kuldevata_text:
                kuldevata_text = "Bon deities, Buddhist deities, Tamba ancestral spirits"
            if not region_text:
                region_text = "Bagmati Province (Kavre, Sindhupalchok, Makwanpur, Nuwakot, Dhading, Rasuwa)"
            notes_text = "Indigenous Tibetan-Burman ethnic group with 18+ major clans (Rhu), preserving rich oral Tamba poetry, Buddhist Lamas, and Bon shamans."
        elif "gurung" in cn_words:
            gotra_text = "Tamu Clan (Char Jaat / Sora Jaat)"
            gotra_deva = "तमु कुल (चार जात / सोर जात)"
            if not kuldevata_text:
                kuldevata_text = "Pju & Khepre ancestor spirits, Buddha"
            if not region_text:
                region_text = "Gandaki Province (Kaski, Lamjung, Gorkha, Tanahun, Manang, Syangja)"
            notes_text = "Tamu ethnic group originating in the high slopes of Annapurna, historically divided into Char Jaat (Ghale, Ghodane, Lama, Lamichhane) and Sora Jaat clans."
        elif "tharu" in cn_words:
            gotra_text = "Tharu Clan / Thar"
            gotra_deva = "थारु थर"
            if not kuldevata_text:
                kuldevata_text = "Bhewa, Barham, Gorraiya (Tharu folk deities)"
            if not region_text:
                region_text = "Terai Inner Plains (Dang, Chitwan, Kailali, Kanchanpur, Bardiya, Nawalparasi, Morang)"
            notes_text = "Original indigenous settlers of the malaria-endemic Terai forests, boasting profound ecological knowledge, unique wall murals, and Maghi celebrations."
        elif "sunuwar" in cn_words:
            gotra_text = "Koinch Clan"
            gotra_deva = "कोइँच कुल"
            if not kuldevata_text:
                kuldevata_text = "Shyandar Pidar (Sunuwar ancestor and nature spirits)"
            if not region_text:
                region_text = "Bagmati & Koshi (Ramechhap, Okhaldhunga, Dolakha)"
            notes_text = "Indigenous Kirat-related Koinch nation living along the Likhu and Khimti rivers, holding deep reverence for ancestral nature spirits."

    elif category == "Madhesi / Terai":
        if not region_text:
            region_text = "Terai Plains (Mithila, Bhojpur, Awadh regions)"
        if s_key in ["jha", "mishra", "tripathi", "tiwari", "chaturvedi"]:
            if not gotra_text:
                gotra_text = "Kashyap / Shandilya / Vatsa"
                gotra_deva = "कश्यप / शाण्डिल्य / वत्स"
            if not kuldevata_text:
                kuldevata_text = "Lord Shiva / Bhagwati"
            notes_text = "Maithil Vedic Brahmins of ancient Mithila, custodians of Sanskrit literature, Nyaya philosophy, and sacred Vedic traditions."
        elif "yadav" in s_key or "gwala" in s_key:
            gotra_text = "Yaduvanshi / Kashyap"
            gotra_deva = "यदुवंशी / कश्यप"
            if not kuldevata_text:
                kuldevata_text = "Lord Krishna / Goraiya"
            notes_text = "Prominent Yaduvanshi agricultural and dairy community of the Terai, with influential social and cultural leadership."
        elif not notes_text:
            notes_text = "Integral community of the fertile Terai plains, celebrating Chhath, Sama Chakeva, and Holi with deep cultural fervor."

    elif category == "Dalit":
        if not region_text:
            region_text = "Nationwide across Hill and Terai districts"
        if not gotra_text:
            gotra_text = "Kashyap / Shiva Gotra"
            gotra_deva = "कश्यप / शिव गोत्र"
        if any(w in cn_words or w in clan_words for w in ["bishwokarma", "kami", "lohar", "sunar", "tamata", "od", "parki"]):
            if not kuldevata_text:
                kuldevata_text = "Vishwakarma (Divine Architect/Artisan), Masto, Shiva"
            notes_text = "Master craftsmen, blacksmiths, goldsmiths, and copper artisans. Builders of Nepal's traditional metal heritage and architecture."
        elif any(w in cn_words or w in clan_words for w in ["pariyar", "damai", "darji", "suchikar", "dholi", "nagarchi"]):
            if not kuldevata_text:
                kuldevata_text = "Shiva / Kalika / Masto"
            notes_text = "Custodians of Nepal's auspicious musical heritage (Panche Baja, Naumati Baja) and master tailors/couturiers."
        elif any(w in cn_words or w in clan_words for w in ["mijar", "sarki", "charmakar", "bhul"]):
            if not kuldevata_text:
                kuldevata_text = "Masto / Shiva"
            notes_text = "Master leather artisans and agrarian farmers, historically maintaining essential leathercrafts and rural infrastructure."
        elif any(w in cn_words or w in clan_words for w in ["gandharba", "gaine"]):
            if not kuldevata_text:
                kuldevata_text = "Saraswati / Masto"
            notes_text = "Folk minstrels, traveling bards, and Sarangi virtuosos. Keepers of Nepal's oral history, historic epics (Karkha), and ballads."
        elif "badi" in s_key or "badi" in clan_words:
            if not kuldevata_text:
                kuldevata_text = "Mahadev / Badi ancestors"
            notes_text = "Traditional folk singers, dancers, musical instrument makers, and riverine fishers along the Karnali and Bheri basins."
        elif "tarai-dalit" in comm_norm.lower() or "chamar" in clan_words or "paswan" in s_key or "musahar" in s_key or "dom" in s_key:
            if not kuldevata_text:
                kuldevata_text = "Dinanbhadri / Rahu / Salhesh / Kabir"
            notes_text = "Terai Dalit communities with rich oral traditions, revered folk heroes (Raja Salhesh, Dinanbhadri), and foundational agricultural contributions."

    elif category == "Muslim":
        gotra_text = "Islamic Lineage (Khandaan)"
        gotra_deva = "खानदान / वंश"
        if not region_text:
            region_text = "Terai border districts, Kathmandu Valley, and Western hills (Churaute)"
        if not kuldevata_text:
            kuldevata_text = "Allah / Islamic monotheistic tradition"
        notes_text = "Nepali Muslims comprising Terai Muslims (Ansari, Sheikh, Pathan), historic Kashmiri Muslim merchants of Kathmandu (dating to Malla era), and Western hill Churaute."

    elif category == "Khas-Arya" and not notes_text:
        if "thakuri" in cn_words:
            if not gotra_text:
                gotra_text = "Suryavanshi / Chandravanshi"
                gotra_deva = "सूर्यवंशी / चन्द्रवंशी"
            if not kuldevata_text:
                kuldevata_text = "Kalika / Masto / Baraha"
            if not region_text:
                region_text = "Karnali, Sudurpashchim, Gandaki, Bagmati"
            notes_text = "Aristocratic and royal lineage of the Khas-Malla Empire and medieval Baise/Chaubisi principalities."
        elif "bahun" in cn_words:
            if not kuldevata_text:
                kuldevata_text = "Baraha / Mahadev / Kalika"
            if not region_text:
                region_text = "Gandaki, Bagmati, Koshi, Karnali"
            notes_text = "Priestly and scholarly community of the Khas people, historically responsible for education, rituals, and astrology."
        elif "chhetri" in cn_words:
            if not kuldevata_text:
                kuldevata_text = "Masto / Kalika / Bhairav"
            if not region_text:
                region_text = "Karnali, Sudurpashchim, Gandaki, Bagmati, Koshi"
            notes_text = "Warrior and administrative pillar of the Khas kingdom, famed for courage and service in national unification and defense."
        elif "dashnami" in cn_words or "sanyasi" in cn_words or "giri" in s_key:
            if not gotra_text:
                gotra_text = "Kapil / Dattatreya"
                gotra_deva = "कपिल / दत्तात्रेय"
            if not kuldevata_text:
                kuldevata_text = "Lord Shiva / Gorakhnath / Dattatreya"
            if not region_text:
                region_text = "Gandaki, Bagmati, Koshi"
            notes_text = "Descendants of the 10 monastic orders of Adi Shankaracharya who transitioned into householder sages (Giri, Puri, Bharati, etc.)."

    entry = {
        "id": id_counter,
        "surname": surname_raw,
        "devanagari": devanagari if devanagari else surname_raw,
        "category": category,
        "community": display_community,
        "subcaste_or_clan": subcaste_text,
        "gotra": gotra_text if gotra_text else "Clan Lineage / Thar",
        "gotra_devanagari": gotra_deva if gotra_deva else "",
        "pravara": pravara_text,
        "kuldevata": kuldevata_text if kuldevata_text else "Local Ancestral / Kula Deity",
        "origin": origin_text,
        "origin_devanagari": origin_deva,
        "region": region_text if region_text else "Nepal (Widespread)",
        "census_caste": census_caste,
        "census_pop": census_pop,
        "census_rank": census_rank,
        "census_pct": census_pct,
        "notes": notes_text if notes_text else "Historic Nepali family lineage with deep cultural and regional roots."
    }

    records.append(entry)
    id_counter += 1

print(f"Enriched total records: {len(records)}")

# Write to JSON
with open('data/surnames.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

# Write to JS
with open('js/casteData.js', 'w', encoding='utf-8') as f:
    f.write('/**\n * Master verified and enriched dataset of Nepali Surnames, Castes, Gotras, and Clans.\n * Fact-checked and structured for interactive search and exploration.\n */\n')
    f.write('var CASTE_DATABASE = window.CASTE_DATABASE = ')
    json.dump(records, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print("Successfully regenerated data/surnames.json and js/casteData.js")


# Enrich census 2021 with subcastes, gotras, languages, and matching surnames
caste_surnames = {}
for s in records:
    cc = s.get('census_caste')
    if cc:
        caste_surnames.setdefault(cc, []).append(s['surname'])

ETHNO_METADATA = {
    "Brahman - Hill": {
        "subcastes": "उपाध्याय (Upadhyaya), जैसी (Jaisi), कुमाईं (Kumai), पूर्वीया (Purbiya)",
        "major_gotras": "कौडिन्य, भारद्वाज, कश्यप, आत्रेय, वशिष्ठ, मौद्गल्य, उपमन्यु, शाण्डिल्य, कौशिक, गर्ग, धनञ्जय, पराशर, वत्स, शरद्वत",
        "primary_language": "Nepali (नेपाली - ४४.८६%)",
        "ancestor_language": "Nepali (नेपाली), Khas (खस), Sanskrit (संस्कृत)",
        "amended_from_2011": "Unchanged (कायम रहेको)"
    },
    "Kshetri": {
        "subcastes": "खस क्षेत्री (Khas Chhetri), राउत (Raut), कुँवर (Kunwar), खड्का (Khadka), बिष्ट (Bista), कार्की (Karki), थापा (Thapa)",
        "major_gotras": "कश्यप, भारद्वाज, कौशिक, वत्स, आत्रेय, धनञ्जय, माण्डव्य, मौद्गल्य, शाण्डिल्य, उपमन्यु",
        "primary_language": "Nepali (नेपाली), Doteli (डोटेली), Achhami (अछामी), Bajhangi (बझाङ्गी)",
        "ancestor_language": "Khash (खस), Nepali (नेपाली)",
        "amended_from_2011": "Spelling updated from Chhetree to Kshetri"
    },
    "Thakuri": {
        "subcastes": "शाह (Shah), चन्द (Chand), सिंह (Singh), मल्ल (Malla), सेन (Sen), बंशी (Banshi), हमाल (Hamal)",
        "major_gotras": "कश्यप, भारद्वाज, सूर्यवंशी/मानव",
        "primary_language": "Nepali (नेपाली), Doteli (डोटेली)",
        "ancestor_language": "Khash (खस / जुम्ली)",
        "amended_from_2011": "Unchanged"
    },
    "Sanyasi/Dasnami": {
        "subcastes": "गिरी (Giri), पुरी (Puri), भारती (Bharati), वन (Ban), तीर्थ (Tirtha), आश्रम (Ashram), सरस्वती (Saraswati)",
        "major_gotras": "कपिल / दत्तात्रेय (Kapil / Dattatreya)",
        "primary_language": "Nepali (नेपाली)",
        "ancestor_language": "Nepali / Sanskrit",
        "amended_from_2011": "Unchanged"
    },
    "Bishwokarma": {
        "subcastes": "कामी (Kami), सुनार (Sunar), लोहार (Lohar), टमटा/ताम्राकार (Tamta), चुनारा (Chunara), पार्की (Parki), कडरा (Kadara)",
        "major_gotras": "कश्यप, भारद्वाज, विश्वामित्र, वशिष्ठ, धनञ्जय, शिवगोत्र",
        "primary_language": "Nepali (नेपाली)",
        "ancestor_language": "Khash / Nepali",
        "amended_from_2011": "Renamed from 'Kami' (कामी) to 'Bishwokarma' (विश्वकर्मा) in 2021"
    },
    "Pariyar": {
        "subcastes": "दमाई (Damai), ढोली (Dholi), दर्जी (Darji), सूचिकार (Suchikar), नगर्ची (Nagarchi)",
        "major_gotras": "कश्यप, भारद्वाज, धनञ्जय, शिवगोत्र",
        "primary_language": "Nepali (नेपाली)",
        "ancestor_language": "Khash / Nepali",
        "amended_from_2011": "Renamed from 'Damai/Dholi' to 'Pariyar' (परियार) in 2021"
    },
    "Mijar": {
        "subcastes": "सार्की (Sarki), भूल (Bhul), रोक्का (Rokka), चर्मकार (Charmakar)",
        "major_gotras": "कश्यप, भारद्वाज, वशिष्ठ, शिवगोत्र",
        "primary_language": "Nepali (नेपाली)",
        "ancestor_language": "Khash / Nepali",
        "amended_from_2011": "Renamed from 'Sarki' to 'Mijar' (मिजार) in 2021"
    },
    "Newa: (Newar)": {
        "subcastes": "राजोपाध्याय (Devabhaju), शाक्य (Shakya), बज्राचार्य (Bajracharya), श्रेष्ठ (Shrestha), ज्यापु (Jyapu), उदास/उराय (Uray), मानन्धर (Sayami), प्रजापति (Kumah), खड्गी (Shahi/Nai), कपाली (Kusle), बलामी (Balami)",
        "major_gotras": "गुठी/वंश (Guthi/Clan), कश्यप, मानव; राजोपाध्याय: गर्ग, भारद्वाज, कौशिक",
        "primary_language": "Nepalbhasha / Newari (नेपालभाषा - २.९६%)",
        "ancestor_language": "Nepalbhasha (नेपालभाषा - ४.०५%)",
        "amended_from_2011": "Renamed from 'Newar' to 'Newa: (Newar)' (नेवा:) in 2021"
    },
    "Magar": {
        "subcastes": "थापा (Thapa), राना (Rana), आले (Ale), पुन (Pun), बुढा/बुढामगर (Budha), रोका (Roka), घर्ती (Gharti)",
        "major_gotras": "सात थरी कुल परम्परा (Seven Clan Lineages)",
        "primary_language": "Magar Dhut (मगर ढुट - २.७८%), Magar Kham (मगर खाम), Magar Kaike (मगर काइके)",
        "ancestor_language": "Magar Dhut (मगर ढुट - ४.२८%)",
        "amended_from_2011": "Unchanged (Pun recognized as distinct caste in 2021)"
    },
    "Tharu": {
        "subcastes": "डंगौरा (Dangaura), राना (Rana), कठरिया (Kathariya), कोचिला (Kochila), रौतार (Rautar), लामपुछ्वा (Lampuchhwa)",
        "major_gotras": "थारु कुल परम्परा तथा गोत्र (Tharu Clan Lineages)",
        "primary_language": "Tharu (थारु - ५.८८%)",
        "ancestor_language": "Tharu (थारु - ६.०५%)",
        "amended_from_2011": "Ranatharu categorized as separate caste in 2021"
    },
    "Tamang": {
        "subcastes": "मोक्तान (Moktan), योन्जन (Yonjan), थिङ (Thing), बम्जन (Bomjan), पाख्रिन (Pakhrin), वाइबा (Waiba), घिसिङ (Ghising), स्याङ्तान (Syangtang), लोप्चन (Lopchan), गोङ्बा (Gongba)",
        "major_gotras": "रु / थर (Rhu - १८+ मूल थरहरू)",
        "primary_language": "Tamang (तामाङ - ४.८८%)",
        "ancestor_language": "Tamang (तामाङ - ५.५०%)",
        "amended_from_2011": "Unchanged"
    },
    "Rai": {
        "subcastes": "बान्तावा (Bantawa), चाम्लिङ (Chamling), कुलुङ (Kulung), थुलुङ (Thulung), साम्पाङ (Sampang), खालिङ (Khaling), लोहोरुङ (Lohorung), दुमी (Dumi), नाछिरिङ (Nachhiring), बाहिङ (Bahing), मेवाहाङ (Mewahang), पुमा (Puma)",
        "major_gotras": "माझ किराँत पाछा/सामेत (Pachha / Samet)",
        "primary_language": "Bantawa (बान्तावा), Chamling (चाम्लिङ), Rai (राई), Thulung, Khaling",
        "ancestor_language": "Rai Languages (किराँती भाषाहरू)",
        "amended_from_2011": "Several Rai linguistic communities separately reported"
    },
    "Yakthung/Limbu": {
        "subcastes": "फेदापे (Phedape), पान्थरे (Panthare), तम्बरखोले (Tambarkhole), छथरे (Chhathare), मेवाखोले (Mewakhole) — १० लिम्बू उपथर",
        "major_gotras": "याक्थुङ हाङ / सामेत (Yakthung Hang / Samet)",
        "primary_language": "Yakthung/Limbu (याक्थुङ/लिम्बू - १.२०%)",
        "ancestor_language": "Yakthung/Limbu (१.४०%)",
        "amended_from_2011": "Renamed from 'Limbu' to 'Yakthung/Limbu' in 2021"
    },
    "Gurung": {
        "subcastes": "चार जात (Char Jat: घोदाने, घले, लामा, लामिछाने) र सोह्र जात (Sohra Jat)",
        "major_gotras": "तमू प्ये / कुल परम्परा (Tamu Pye Lineages)",
        "primary_language": "Gurung (गुरुङ - १.१२%)",
        "ancestor_language": "Gurung (१.६०%)",
        "amended_from_2011": "Unchanged"
    },
    "Yadav": {
        "subcastes": "आहिर (Ahir), गोप (Gope), मण्डल (Mandal), कृष्णौत (Krishnaut), मझरौत (Majhrot), कनौडिया (Kanaudiya)",
        "major_gotras": "कश्यप (Kashyap), अत्रि, यदुवंशी परम्परा",
        "primary_language": "Maithili (मैथिली), Bhojpuri (भोजपुरी), Bajjika (बज्जिका)",
        "ancestor_language": "Maithili, Bhojpuri, Bajjika",
        "amended_from_2011": "Unchanged"
    },
    "Musalman": {
        "subcastes": "अन्सारी (Ansari), शेष/शेख (Sheikh), पठान (Pathan), सैयद (Sayyid), मन्सूरी (Mansoori), कुरैशी (Qureshi), धोबी (Dhobi)",
        "major_gotras": "इस्लामिक खान्दान तथा शजरा (Islamic Shajara / Lineages)",
        "primary_language": "Urdu (उर्दू - १.४२%), Maithili, Bhojpuri, Nepali",
        "ancestor_language": "Urdu (१.९५%), Maithili, Bhojpuri",
        "amended_from_2011": "Unchanged"
    },
    "Rajput": {
        "subcastes": "सूर्यवंशी (Suryavanshi), चन्द्रवंशी (Chandravanshi), चौहान (Chauhan), राठौर (Rathore), सिँह (Singh), गहरवार (Gaharwar)",
        "major_gotras": "कश्यप, वत्स, मानव, कौशिक, भारद्वाज",
        "primary_language": "Maithili, Bhojpuri, Avadhi, Nepali",
        "ancestor_language": "Maithili, Bhojpuri, Avadhi",
        "amended_from_2011": "Unchanged"
    },
    "Kayastha": {
        "subcastes": "कर्ण (Karna), श्रीवास्तव (Shrivastava), अम्बष्ठ (Ambastha), माथुर (Mathur), सक्सेना (Saxena), भटनागर (Bhatnagar)",
        "major_gotras": "कश्यप (Kashyap), आत्रेय (Atreya)",
        "primary_language": "Maithili (मैथिली), Bhojpuri (भोजपुरी)",
        "ancestor_language": "Maithili, Bhojpuri",
        "amended_from_2011": "Unchanged"
    },
    "Brahman - Tarai": {
        "subcastes": "मैथिल ब्राह्मण (Maithil Brahmin), तिरहुते (Tirhute), भूमिहार (Bhumihar), शाकद्वीपीय (Shakdwipi)",
        "major_gotras": "शाण्डिल्य, कश्यप, भारद्वाज, वत्स, पराशर, गौतम",
        "primary_language": "Maithili (मैथिली), Bhojpuri (भोजपुरी)",
        "ancestor_language": "Maithili, Bhojpuri, Sanskrit",
        "amended_from_2011": "Unchanged (Bhumihar separately categorized in 2021)"
    },
    "Teli": {
        "subcastes": "साह (Sah), साहु (Sahu), तेली (Teli), रौनियार (Rauniyar)",
        "major_gotras": "कश्यप (Kashyap)",
        "primary_language": "Maithili, Bhojpuri, Bajjika",
        "ancestor_language": "Maithili, Bhojpuri",
        "amended_from_2011": "Unchanged"
    },
    "Koiri/Kushwaha": {
        "subcastes": "कुशवाहा (Kushwaha), कोइरी (Koiri), महतो (Mahato), भगत (Bhagat)",
        "major_gotras": "कश्यप (Kashyap)",
        "primary_language": "Bhojpuri, Maithili, Bajjika",
        "ancestor_language": "Bhojpuri, Maithili",
        "amended_from_2011": "Spelling updated to Koiri/Kushwaha in 2021"
    },
    "Kurmi": {
        "subcastes": "पटेल (Patel), चौधरी (Chaudhary), वर्मा (Verma), महतो (Mahato)",
        "major_gotras": "कश्यप (Kashyap)",
        "primary_language": "Avadhi, Bhojpuri, Maithili",
        "ancestor_language": "Avadhi, Bhojpuri",
        "amended_from_2011": "Unchanged"
    },
    "Chamar/Harijan/Ram": {
        "subcastes": "चमार (Chamar), राम (Ram), हरिजन (Harijan), मोची (Mochi), रविदास (Ravidass)",
        "major_gotras": "रविदास परम्परा / कश्यप",
        "primary_language": "Bhojpuri, Maithili, Bajjika",
        "ancestor_language": "Bhojpuri, Maithili",
        "amended_from_2011": "Unchanged"
    },
    "Dusadh/Pasawan/Pasi": {
        "subcastes": "दुसाध (Dusadh), पासवान (Paswan), पासी (Pasi), हजरा (Hajara)",
        "major_gotras": "गहलोत / सलहेस परम्परा / कश्यप",
        "primary_language": "Maithili, Bhojpuri, Bajjika",
        "ancestor_language": "Maithili, Bhojpuri",
        "amended_from_2011": "Unchanged"
    },
    "Musahar": {
        "subcastes": "मुसहर (Musahar), सादा (Sada), माझी (Majhi), ऋषिदेव (Rishidev)",
        "major_gotras": "दीना-भद्री परम्परा / प्रकृति",
        "primary_language": "Maithili, Bhojpuri, Bajjika",
        "ancestor_language": "Maithili, Bhojpuri",
        "amended_from_2011": "Unchanged"
    },
    "Sherpa": {
        "subcastes": "लामा (Lama), साल्खा (Salakha), गोपेर्मा (Goperma), पिनासा (Pinasa)",
        "major_gotras": "शेर्पा रु / कुल (Sherpa Rhu Lineages)",
        "primary_language": "Sherpa (शेर्पा - ०.४०%)",
        "ancestor_language": "Sherpa (शेर्पा - ०.४४%)",
        "amended_from_2011": "Unchanged"
    },
    "Sunuwar": {
        "subcastes": "मुखिया (Mukhiya), बामनायात (Bamanayata), ब्राचे (Brachey), दुर्बिचा (Durbicha)",
        "major_gotras": "कोइँच कुल परम्परा (Koinch Clan Lineage)",
        "primary_language": "Sunuwar (सुनुवार)",
        "ancestor_language": "Sunuwar (सुनुवार)",
        "amended_from_2011": "Unchanged"
    }
}

for c in CENSUS_LIST:
    c_name = c['caste']
    meta = ETHNO_METADATA.get(c_name, {})
    c['subcastes'] = meta.get('subcastes', 'स्थानीय थर तथा पारिवारिक शाखाहरू')
    c['major_gotras'] = meta.get('major_gotras', 'कुल परम्परा तथा वंश परम्परा')
    c['primary_language'] = meta.get('primary_language', 'नेपाली / सम्बन्धित मातृभाषा')
    c['ancestor_language'] = meta.get('ancestor_language', 'पुर्खाको भाषा (Census 2021 Annex 4)')
    c['amended_from_2011'] = meta.get('amended_from_2011', 'Census 2011 देखि यथावत' if c['rank'] <= 125 else '२०७८ जनगणनामा नयाँ सूचीकृत')
    matched_surnames = caste_surnames.get(c_name, [])
    c['surnames_count'] = len(matched_surnames)
    c['sample_surnames'] = matched_surnames[:12]

with open('data/census_2021.json', 'w', encoding='utf-8') as f:
    json.dump(CENSUS_LIST, f, ensure_ascii=False, indent=2)

with open('js/censusData.js', 'w', encoding='utf-8') as f:
    f.write('/**\n * Official National Population and Housing Census 2021 (NPHC 2021)\n * Published by National Statistics Office (NSO), Government of Nepal.\n * Enriched with subcastes, major gotras, languages, and matching verified surnames.\n */\n')
    f.write('var CENSUS_2021_DATA = window.CENSUS_2021_DATA = ')
    json.dump(CENSUS_LIST, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print("Successfully regenerated data/census_2021.json and js/censusData.js")

# Regenerate sitemap.xml
import urllib.parse
import datetime

BASE_URL = 'https://www.rishavdahal.com.np/cast-in-nepal/'
TODAY = datetime.date.today().isoformat()
urls = []
urls.append((BASE_URL, '1.0', 'daily'))
for v in ['grid', 'table', 'sagotra', 'checker', 'insights']:
    urls.append((f'{BASE_URL}?view={v}', '0.9', 'weekly'))
for cat in ['khas-arya', 'newar', 'janajati', 'madhesi', 'dalit', 'muslim']:
    urls.append((f'{BASE_URL}?category={cat}', '0.85', 'weekly'))

gotras_set = set()
for s in records:
    g = (s.get('gotra') or '').strip()
    if g and g not in ['—', '-', 'None', 'Unknown', 'Various', 'N/A', '']:
        gotras_set.add(g)
for g in sorted(gotras_set):
    urls.append((f'{BASE_URL}?gotra={urllib.parse.quote(g)}', '0.80', 'monthly'))

for c in CENSUS_LIST:
    caste_name = c.get('caste', '').strip()
    if caste_name:
        urls.append((f'{BASE_URL}?caste={urllib.parse.quote(caste_name)}', '0.75', 'monthly'))

surnames_set = set()
for s in records:
    name = (s.get('surname') or '').strip()
    if name:
        for part in name.split('/'):
            clean_part = part.strip()
            if clean_part:
                surnames_set.add(clean_part)
for sn in sorted(surnames_set):
    urls.append((f'{BASE_URL}?search={urllib.parse.quote(sn)}', '0.70', 'monthly'))

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
    '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
    '        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">'
]
for loc, priority, changefreq in urls:
    clean_loc = loc.replace('&', '&amp;')
    xml_lines.append('  <url>')
    xml_lines.append(f'    <loc>{clean_loc}</loc>')
    xml_lines.append(f'    <lastmod>{TODAY}</lastmod>')
    xml_lines.append(f'    <changefreq>{changefreq}</changefreq>')
    xml_lines.append(f'    <priority>{priority}</priority>')
    xml_lines.append('  </url>')
xml_lines.append('</urlset>\n')

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_lines))

print(f"Successfully generated sitemap.xml with {len(urls)} URLs!")

