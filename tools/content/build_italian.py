"""Build courses/it/curriculum.json (the Italian course) from the readable lists below.

Run: python tools/content/build_italian.py
Each word: (italian, english, [other accepted English answers], emoji, {extra fields})
Standard Italian as spoken in Italy, same levels, units, lessons and word counts as the
French course, with the grammar units swapped for Italian ones (Il & La, Essere & Avere,
Tu & Lei). Italian is the same slot-for-slot: if French has 6 words in a lesson, so does this.
Word ids: it-<lesson>-<n>. Italian puts no space before ? or !, so no special spacing is needed.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "courses" / "it" / "curriculum.json"


def W(text, en, accept=None, emoji=None, **extra):
    return (text, en, accept or [], emoji, extra)


COURSE = [
  ("Beginner", [
    ("it-basics1", "Greetings", "The words you'll use every single day.", [
      ("it-b1-l1", "Hello & thanks", [
        W("Buongiorno", "Hello", ["hi", "hiya", "good morning", "good day"], "👋", note="Use buongiorno until the afternoon, then buonasera. With friends and family, ciao is hello and goodbye in one word!"),
        W("Grazie", "Thank you", ["thanks", "thank you very much"], "🙏", note="Said 'GRAH-tsyeh'. The z sounds like 'ts'."),
        W("Sì", "Yes", ["yeah"], "✅", note="The accent on sì means yes. Without it, si means 'if' or 'himself'."),
        W("No", "No", [], "❌", note="The same as English! Italian o is short and clean: noh."),
        W("Scusa", "Sorry", ["excuse me", "pardon", "pardon me"], "😔", note="To friends and family say scusa. To someone you don't know say mi scusi."),
        W("Prego", "You're welcome", ["no problem", "not at all", "you are welcome", "please"], "😌", note="Prego does lots of jobs: you're welcome, please go ahead, after you."),
      ]),
      ("it-b1-l2", "How are you?", [
        W("Come stai?", "How are you?", ["how's it going", "how are things", "how are you doing"], "🙂", note="Ask it with come stai? and answer it with sto bene (I'm well). To a grown-up you don't know, say come sta?"),
        W("Bene", "Good", ["well", "fine", "ok"], "👍"),
        W("Molto bene", "Very good", ["very well", "really good"], "😄"),
        W("E tu?", "And you?", ["what about you", "and yourself"], "🫵"),
        W("Arrivederci", "Goodbye", ["bye", "bye bye"], "👋", note="With friends, just say ciao again. Arrivederci is the polite goodbye."),
        W("A dopo", "See you later", ["see you", "bye for now", "later"], "🙋"),
      ]),
    ]),
    ("it-numbers1", "Numbers 1–10", "Count on your fingers together.", [
      ("it-n1-l1", "One to five", [
        W("uno", "One", ["1"], "1️⃣"), W("due", "Two", ["2"], "2️⃣"), W("tre", "Three", ["3"], "3️⃣", note="Roll the r a tiny bit: treh."),
        W("quattro", "Four", ["4"], "4️⃣", note="The double t is held a little longer: KWAT-tro."), W("cinque", "Five", ["5"], "5️⃣", note="Said 'CHEEN-kweh'."),
      ]),
      ("it-n1-l2", "Six to ten", [
        W("sei", "Six", ["6"], "6️⃣", note="Said 'say'."), W("sette", "Seven", ["7"], "7️⃣", note="Hold the double t: SET-teh."),
        W("otto", "Eight", ["8"], "8️⃣", note="Hold the double t: OT-toh."), W("nove", "Nine", ["9"], "9️⃣"), W("dieci", "Ten", ["10"], "🔟", note="Said 'dee-AY-chee'."),
      ]),
    ]),
    ("it-numbers2", "Bigger Numbers", "Eleven, twenty, and counting by tens.", [
      ("it-n2-l1", "Eleven to fifteen", [
        W("undici", "Eleven", ["11"]), W("dodici", "Twelve", ["12"]), W("tredici", "Thirteen", ["13"]),
        W("quattordici", "Fourteen", ["14"]), W("quindici", "Fifteen", ["15"], note="Said 'kwin-DEE-chee'."),
      ]),
      ("it-n2-l2", "Counting by tens", [
        W("venti", "Twenty", ["20"]), W("trenta", "Thirty", ["30"]), W("quaranta", "Forty", ["40"]),
        W("cinquanta", "Fifty", ["50"]), W("cento", "One hundred", ["100", "a hundred", "hundred"], "💯", note="Said 'CHEN-toh': c before e sounds like ch."),
      ]),
    ]),
    ("it-family", "Family", "Mamma, papà and everyone in between. Il = he word, la = she word.", [
      ("it-fam-l1", "Close family", [
        W("la madre", "Mother", ["mum", "mom", "mummy", "the mother"], "👩", note="Mamma is 'mum'."),
        W("il padre", "Father", ["dad", "daddy", "the father"], "👨", note="Papà is 'dad'. The accent shows you stress the last a."),
        W("il fratello", "Brother", ["the brother"], "👦"),
        W("la sorella", "Sister", ["the sister"], "👧"),
        W("il figlio", "Son", ["the son"], "🧒", note="The gli sounds like the 'lli' in million: FEE-lyo."),
        W("la figlia", "Daughter", ["the daughter"], "👩‍👧", note="Same gli sound as in son: FEE-lya."),
      ]),
      ("it-fam-l2", "Grandparents & more", [
        W("il nonno", "Grandfather", ["grandad", "grandpa", "granddad"], "👴", note="Hold the double n: NON-no."),
        W("la nonna", "Grandmother", ["grandma", "granny", "nan", "nana"], "👵"),
        W("lo zio", "Uncle", ["the uncle"], "🧔", note="It's lo, not il, because zio starts with z."),
        W("la zia", "Aunt", ["auntie", "aunty"], "👩‍🦰"),
        W("il cugino", "Cousin", ["the cousin"], "🧑", note="A girl cousin is la cugina."),
        W("la famiglia", "Family", ["the family"], "👨‍👩‍👧‍👦", note="The gli sound again: fa-MEE-lya."),
      ]),
    ]),
    ("it-colors", "Colours & Shapes", "The colour usually comes after the thing: una macchina rossa, a red car.", [
      ("it-col-l1", "Colours", [
        W("rosso", "Red", [], "🔴", swatch="#c0392b", note="Hold the double s: ROS-so."),
        W("blu", "Blue", [], "🔵", swatch="#1f5fa8", note="Blu never changes, whatever it describes."),
        W("verde", "Green", [], "🟢", swatch="#2e8b57"),
        W("giallo", "Yellow", [], "🟡", swatch="#f1c40f", note="Said 'JAL-lo': gi sounds like j."),
        W("nero", "Black", [], "⚫", swatch="#222222"),
        W("bianco", "White", [], "⚪", swatch="#f8f8f8"),
      ]),
      ("it-col-l2", "Shapes", [
        W("il cerchio", "Circle", ["a circle"], "⭕", note="Said 'CHER-kyo': the first c is 'ch', the ch is a hard 'k'."),
        W("il quadrato", "Square", ["a square"], "🟥"),
        W("il triangolo", "Triangle", ["a triangle"], "🔺"),
        W("la stella", "Star", ["a star"], "⭐", note="Hold the double l: STEL-la."),
        W("il cuore", "Heart", ["a heart"], "❤️"),
      ]),
    ]),
    ("it-food", "Food & Drink", "Pizza, pasta and everything in between.", [
      ("it-food-l1", "Foods", [
        W("il pane", "Bread", [], "🍞"),
        W("il formaggio", "Cheese", [], "🧀", note="The gg sounds like j: for-MAJ-jo."),
        W("il riso", "Rice", [], "🍚"),
        W("la mela", "Apple", ["an apple"], "🍎"),
        W("il pollo", "Chicken", [], "🍗"),
        W("l'uovo", "Egg", ["an egg"], "🥚", note="One egg is l'uovo, but two eggs are le uova."),
      ]),
      ("it-food-l2", "Drinks & taste", [
        W("l'acqua", "Water", [], "💧", note="Said 'AK-kwa'."),
        W("il latte", "Milk", [], "🥛", note="In Italy, latte means plain milk, not coffee!"),
        W("il succo", "Juice", [], "🧃"),
        W("il caffè", "Coffee", [], "☕", note="Ask for un caffè and you get a tiny, strong espresso."),
        W("buono", "Tasty", ["delicious", "yummy", "good"], "😋", note="Buono is 'good' and 'tasty'. With a she word it becomes buona: una pizza buona."),
        W("piccante", "Spicy", ["hot"], "🌶️", note="Said 'pik-KAN-teh'."),
      ]),
    ]),
    ("it-phrases", "Everyday Phrases", "Small words that unlock real conversations.", [
      ("it-phr-l1", "Asking for things", [
        W("per favore", "Please", [], "🥺", note="You can also say per piacere. Both are polite."),
        W("vorrei", "I would like", ["i'd like"], "🙋", note="Vorrei is the polite way to ask: vorrei un gelato!"),
        W("ho bisogno di", "I need", [], "🙌", note="The h is silent: ho sounds like 'oh'."),
        W("Dov'è il bagno?", "Where is the toilet?", ["where are the toilets", "where's the toilet", "where is the bathroom", "where's the bathroom"], "🚻"),
        W("Non capisco", "I don't understand", ["i do not understand"], "🤷"),
        W("Più lentamente, per favore", "Slower, please", ["more slowly please", "slowly please"], "🐢"),
      ]),
      ("it-phr-l2", "Question words", [
        W("Cosa?", "What?", [], "❓", note="You'll also hear che cosa? or just che?"),
        W("Chi?", "Who?", [], "🧑", note="Chi is said 'kee', with a hard k sound."),
        W("Dove?", "Where?", [], "📍"),
        W("Quando?", "When?", [], "🕐"),
        W("Perché?", "Why?", [], "🤔", note="Perché means both 'why?' and 'because'. The accent goes on the last é."),
        W("Quanto?", "How much?", ["how many"], "💰"),
      ]),
    ]),
    ("it-time", "Time & Days", "Days of the week — and no capital letters in Italian!", [
      ("it-time-l1", "Weekdays", [
        W("lunedì", "Monday", note="The accent shows you stress the last syllable: loo-neh-DEE."), W("martedì", "Tuesday"), W("mercoledì", "Wednesday"),
        W("giovedì", "Thursday"), W("venerdì", "Friday"),
      ]),
      ("it-time-l2", "Weekend & today", [
        W("sabato", "Saturday"), W("domenica", "Sunday"),
        W("oggi", "Today", [], "📅", note="The gg sounds like j: OJ-jee."),
        W("domani", "Tomorrow", [], "🌅"),
        W("ieri", "Yesterday", [], "⏪"),
      ]),
    ]),
    ("it-places", "Places & Directions", "Getting around town.", [
      ("it-pl-l1", "Places", [
        W("la casa", "House", ["home", "the house"], "🏠"),
        W("la scuola", "School", ["the school"], "🏫", note="Sc before u sounds like 'sk': SKWO-la."),
        W("la spiaggia", "Beach", ["the beach"], "🏖️", note="Said 'SPYAJ-ja'."),
        W("il parco", "Park", ["the park"], "🌳"),
        W("il negozio", "Shop", ["store", "the shop"], "🏪"),
        W("l'ospedale", "Hospital", ["the hospital"], "🏥", note="Said 'os-peh-DAH-leh'. English has an h at the start, but Italian has none."),
      ]),
      ("it-pl-l2", "Directions", [
        W("a sinistra", "On the left", ["left", "to the left"], "⬅️"),
        W("a destra", "On the right", ["right", "to the right"], "➡️"),
        W("sempre dritto", "Straight on", ["straight ahead", "straight"], "⬆️"),
        W("qui", "Here", [], "📌", note="Qui is said 'kwee'. You'll also hear qua."),
        W("lì", "There", ["over there"], "👉", note="With the accent, lì means 'there'. Without it, li is 'them'."),
        W("vicino", "Near", ["close", "nearby"], "🤏"),
      ]),
    ]),
    ("it-shopping", "Shopping & Money", "Prices, paying and 'just looking'.", [
      ("it-shop-l1", "At the shop", [
        W("Quanto costa?", "How much is it?", ["how much does it cost", "how much"], "🏷️"),
        W("caro", "Expensive", ["dear"], "💸", note="Caro also means 'dear', as in a friend: caro amico."),
        W("economico", "Cheap", ["inexpensive", "not expensive"], "🪙"),
        W("Sto solo guardando", "I'm just looking", ["just looking", "i am just looking"], "👀"),
        W("la taglia", "Size", ["clothes size"], "👕", note="Taglia is for clothes. A shoe size is il numero."),
        W("Lo prendo", "I'll take it", ["i will take it"], "🛍️"),
      ]),
      ("it-shop-l2", "Paying up", [
        W("i soldi", "Money", [], "💶", note="Soldi is always plural: i soldi."),
        W("la carta", "Card", ["bank card", "credit card", "debit card"], "💳", note="Carta also means 'paper'."),
        W("in contanti", "In cash", ["cash"], "💵"),
        W("il conto", "The bill", ["bill", "check", "the check"], "🧾"),
        W("il resto", "Change", ["the change"], "🪙"),
        W("il negozio di souvenir", "Gift shop", ["souvenir shop", "the gift shop"], "🎁", note="Souvenir stays the same in the plural."),
      ]),
    ]),
    ("it-travel", "Travel & Transport", "How you'll get to Italy — and around it.", [
      ("it-trv-l1", "Getting around", [
        W("la macchina", "Car", ["the car"], "🚗", note="Said 'MAK-ki-na'. You might also hear l'auto."),
        W("l'autobus", "Bus", ["the bus"], "🚌"),
        W("il treno", "Train", ["the train"], "🚆"),
        W("l'aereo", "Plane", ["aeroplane", "airplane", "the plane"], "✈️"),
        W("la bici", "Bike", ["bicycle", "the bike"], "🚲", note="Short for la bicicletta."),
        W("a piedi", "On foot", ["walking"], "🚶"),
      ]),
      ("it-trv-l2", "At the airport", [
        W("l'aeroporto", "Airport", ["the airport"], "🛫"),
        W("il passaporto", "Passport", ["the passport"], "🛂"),
        W("la valigia", "Suitcase", ["the suitcase"], "🧳", note="Said 'va-LEE-ja'."),
        W("il biglietto", "Ticket", ["the ticket"], "🎫", note="The gli sounds like 'lli' in million: beel-YET-to."),
        W("l'uscita d'imbarco", "Boarding gate", ["gate", "the gate"], "🚪", note="L'uscita on its own means 'the exit'. At airports you'll often see the English word gate."),
        W("il volo", "Flight", ["the flight"], "🛬"),
      ]),
    ]),
    ("it-weather", "Weather & Seasons", "Small talk that works anywhere — Italians love to talk about the weather too!", [
      ("it-wx-l1", "What's it like out?", [
        W("Fa caldo", "It's hot", ["it is hot"], "🥵", note="Word for word: it makes hot."),
        W("Fa freddo", "It's cold", ["it is cold"], "🥶"),
        W("C'è il sole", "It's sunny", ["it is sunny"], "☀️", note="Word for word: there is the sun."),
        W("Piove", "It's raining", ["it is raining", "it rains"], "🌧️"),
        W("Tira vento", "It's windy", ["it is windy"], "💨", note="Word for word: it pulls wind."),
        W("È nuvoloso", "It's cloudy", ["it is cloudy"], "☁️"),
      ]),
      ("it-wx-l2", "Seasons", [
        W("la primavera", "Spring", [], "🌸"),
        W("l'estate", "Summer", [], "🌞", note="L'estate is a she word: la bella estate."),
        W("l'autunno", "Autumn", ["fall"], "🍂", note="Hold the double n: ow-TOON-no."),
        W("l'inverno", "Winter", [], "❄️"),
        W("il tempo", "The weather", ["weather"], "🌦️", note="Tempo also means 'time'."),
      ]),
    ]),
    ("it-feelings", "Feelings & Health", "Saying how you actually feel.", [
      ("it-feel-l1", "Feelings", [
        W("contento", "Happy", ["glad", "pleased"], "😊", note="A girl says contenta."),
        W("triste", "Sad", [], "😢"),
        W("stanco", "Tired", [], "😴", note="A girl says stanca."),
        W("arrabbiato", "Angry", ["cross", "annoyed"], "😠", note="A girl says arrabbiata. Hold the double r and b."),
        W("nervoso", "Nervous", [], "😬", note="A girl says nervosa."),
        W("Mi annoio", "I'm bored", ["i am bored", "bored"], "🥱"),
      ]),
      ("it-feel-l2", "Feeling unwell", [
        W("Ho mal di testa", "I have a headache", ["my head hurts"], "🤕", note="Word for word: I have pain of head."),
        W("Ho mal di pancia", "I have a tummy ache", ["my tummy hurts", "stomach ache", "my stomach hurts"], "🤢"),
        W("Sono malato", "I'm ill", ["i am ill", "i'm sick", "i am sick"], "🤒", note="A girl says sono malata."),
        W("il medico", "Doctor", ["the doctor"], "🩺"),
        W("la farmacia", "Pharmacy", ["chemist", "the chemist"], "💊"),
        W("Ho la febbre", "I have a temperature", ["i have a fever"], "🌡️"),
      ]),
    ]),
    ("it-sentences", "Putting It Together", "Whole sentences, built from everything so far.", [
      ("it-sen-l1", "Talking about yourself", [
        W("Mi chiamo Anna", "My name is Anna", ["i'm called anna", "i am called anna"], "🙋", note="Ch is a hard k sound: mee KYAH-mo."),
        W("Ho dieci anni", "I'm ten years old", ["i am ten", "i'm ten", "i am ten years old"], "🎂", note="In Italian you 'have' years: ho = I have."),
        W("Vengo dall'Inghilterra", "I'm from England", ["i am from england", "i come from england"], "🌍"),
        W("Abito a Londra", "I live in London", [], "🏙️"),
        W("Parlo un po' di italiano", "I speak a little Italian", ["i speak a bit of italian"], "💬"),
        W("Mi piace il cioccolato", "I like chocolate", [], "🍫", note="Word for word: chocolate pleases me."),
      ]),
      ("it-sen-l2", "A day in words", [
        W("Mi alzo", "I get up", [], "⏰"),
        W("Faccio colazione", "I have breakfast", ["i eat breakfast", "i have my breakfast"], "🥣", note="Word for word: I make breakfast."),
        W("Vado a scuola", "I go to school", [], "🎒"),
        W("Mangio con la mia famiglia", "I eat with my family", ["i have a meal with my family"], "🍽️"),
        W("Gioco al parco", "I play in the park", [], "⚽", note="Said 'JO-ko'."),
        W("Vado a letto", "I go to bed", [], "🛏️"),
      ]),
    ]),
  ]),
  ("Elementary", [
    ("it-gender", "Il & La", "Every Italian noun is a 'he' or a 'she' word — learn the little word in front.", [
      ("it-gen-l1", "The: il or la?", [
        W("il cane", "The dog", ["dog"], "🐶", note="Before a vowel il and la become l': l'amico. Before z or s+consonant, il becomes lo: lo zaino."),
        W("il gatto", "The cat", ["cat"], "🐱", note="Hold the double t: GAT-to."),
        W("la tavola", "The table", ["table"], "🍽️", note="La tavola is the table you eat at. A work table is il tavolo."),
        W("il libro", "The book", ["book"], "📖"),
        W("la finestra", "The window", ["window"], "🪟"),
      ]),
      ("it-gen-l2", "A or an: un or una?", [
        W("una banana", "A banana", ["banana"], "🍌"),
        W("un'arancia", "An orange", ["orange"], "🍊", note="Before a she word that starts with a vowel, una becomes un' (with an apostrophe). For a he word it's just un: un amico."),
        W("un pallone", "A ball", ["ball", "a football"], "⚽", note="Un has no apostrophe with a he word."),
        W("una sedia", "A chair", ["chair"], "🪑"),
        W("delle scarpe", "Some shoes", ["shoes"], "👟", note="Delle means 'some' for more than one she word."),
      ]),
    ]),
    ("it-routine", "Daily Routine", "The verbs and time words behind an ordinary day.", [
      ("it-rtn-l1", "Morning to night", [
        W("Mi faccio la doccia", "I have a shower", ["i shower", "i take a shower"], "🚿"),
        W("Mi lavo i denti", "I brush my teeth", [], "🪥", note="Word for word: I wash my teeth."),
        W("Mi vesto", "I get dressed", [], "👕"),
        W("Mangio", "I eat", [], "🍴"),
        W("Lavoro", "I work", [], "💼"),
        W("Dormo", "I sleep", [], "😴"),
      ]),
      ("it-rtn-l2", "What time is it?", [
        W("Che ore sono?", "What time is it?", ["what's the time"], "⏰", note="You'll also hear che ora è? Both are fine."),
        W("È l'una", "It's one o'clock", ["it is one o'clock", "it's one"], "🕐", note="One o'clock is singular (è l'una). Every other hour is plural (sono le due)."),
        W("Sono le due", "It's two o'clock", ["it is two o'clock", "it's two"], "🕑"),
        W("e mezza", "Half past", ["and a half"], "🕧", note="Sono le due e mezza: it's half past two."),
        W("la mattina", "In the morning", ["the morning", "morning"], "🌄"),
        W("la sera", "In the evening", ["the evening", "evening"], "🌙"),
      ]),
    ]),
    ("it-essereavere", "Essere & Avere", "The two most important verbs: essere (to be) and avere (to have).", [
      ("it-ea-l1", "Essere: to be", [
        W("Sono alto", "I'm tall", ["i am tall"], "📏", note="A girl says alta."),
        W("Sono inglese", "I'm English", ["i am english"], "🇬🇧", note="Inglese ends in -e, so it's the same for boys and girls."),
        W("È mia sorella", "She's my sister", ["she is my sister", "this is my sister", "it's my sister"], "👧", note="With one family member you drop the little word: mia sorella, not la mia sorella."),
        W("È molto gentile", "He's very nice", ["he is very nice", "he's very kind", "she's very nice", "she is very nice", "she's very kind"], "😊", note="È means 'he is', 'she is' and 'it is'. Context tells you which."),
        W("Siamo una famiglia", "We are a family", ["we're a family"], "👨‍👩‍👧"),
      ]),
      ("it-ea-l2", "Avere: to have", [
        W("Ho un cane", "I have a dog", ["i've got a dog"], "🐕", note="The h is silent: ho sounds like 'oh'."),
        W("Hai fame?", "Are you hungry?", [], "🍽️", note="In Italian you 'have hunger': avere fame."),
        W("Ho sete", "I'm thirsty", ["i am thirsty"], "🥤", note="You 'have thirst': avere sete."),
        W("Ha freddo", "He's cold", ["he is cold", "she's cold", "she is cold"], "🥶", note="You 'have cold': avere freddo."),
        W("Abbiamo una macchina", "We have a car", ["we've got a car"], "🚙", note="Hold the double b and double m."),
      ]),
    ]),
    ("it-compare", "Comparisons", "More than, less than, and the best.", [
      ("it-cmp-l1", "More, less, most", [
        W("più grande", "Bigger", ["larger", "bigger than"], "🐘", note="Più means 'more'. Add it before nearly any describing word."),
        W("più piccolo", "Smaller", [], "🐭"),
        W("migliore", "Better", [], "👍", note="Said 'meel-YO-reh'. Migliore describes things; meglio is used with verbs."),
        W("peggiore", "Worse", [], "👎", note="Said 'ped-JO-reh'."),
        W("il più veloce", "The fastest", ["fastest"], "🏃"),
        W("alto come", "As tall as", [], "📐"),
      ]),
    ]),
    ("it-restaurant", "At the Restaurant", "Order a pizza, ask for the menu and pay the bill.", [
      ("it-res-l1", "Ordering food", [
        W("il menù", "The menu", ["menu"], "📜", note="Il menù fisso in Italy is a set meal at a fixed price."),
        W("Per me, una pizza", "A pizza for me", ["i'll have a pizza", "for me a pizza", "a pizza for me please"], "🍕", note="Pizza is said 'PEET-tsa': the double z is a strong 'ts' sound."),
        W("Cosa vuoi da bere?", "What would you like to drink?", ["what do you want to drink"], "🥤"),
        W("senza cipolla", "Without onion", ["no onion"], "🧅", note="Said 'cheep-OL-la'."),
        W("È buonissimo!", "It's delicious!", ["it is delicious", "it's really good"], "😋", note="Add -issimo to make 'very very': buono, buonissimo."),
        W("Il conto, per favore", "The bill, please", ["the check please", "bill please"], "🧾"),
      ]),
    ]),
    ("it-plans", "Making Plans", "Arranging to meet up — the most useful conversation of all.", [
      ("it-pln-l1", "Are you free?", [
        W("Sei libero sabato?", "Are you free on Saturday?", ["are you free saturday"], "📅", note="To a girl say sei libera."),
        W("Ci vediamo?", "Shall we meet up?", ["shall we meet", "do you want to meet"], "🤝", note="Word for word: do we see each other?"),
        W("A che ora?", "What time?", ["at what time"], "⏰"),
        W("Va bene", "OK", ["okay", "alright", "all right", "agreed"], "👌", note="You'll hear va bene all day long in Italy."),
        W("Mi dispiace, non posso", "Sorry, I can't", ["sorry i cannot"], "🙅"),
        W("A presto!", "See you soon!", ["see you", "see you then"], "👋"),
      ]),
    ]),
  ]),
  ("Intermediate", [
    ("it-connectors", "Connectors", "And, but, because, if — the words that join ideas together.", [
      ("it-con-l1", "Joining ideas", [
        W("e", "And", [], "➕", note="No accent: e = and. With an accent: è = is."),
        W("ma", "But", [], "↔️"),
        W("perché", "Because", [], "💡", note="Perché is both 'why?' and 'because'. Ask it, then answer it with the same word!"),
        W("se", "If", [], "❔"),
        W("o", "Or", [], "🔀", note="Short and clean: oh. Don't mix it up with ho (I have), which sounds exactly the same!"),
        W("anche", "Also", ["too", "as well"], "🔁", note="Said 'AN-keh'."),
      ]),
    ]),
    ("it-directions2", "Giving Directions", "Full sentences for getting someone from A to B.", [
      ("it-dir2-l1", "Turn here", [
        W("Gira a sinistra", "Turn left", ["turn to the left"], "⬅️"),
        W("Vai sempre dritto", "Go straight on", ["keep going straight", "go straight ahead"], "⬆️"),
        W("Attraversa la strada", "Cross the street", ["cross the road"], "🚸"),
        W("È accanto alla banca", "It's next to the bank", ["it is next to the bank"], "🏦"),
        W("la seconda strada", "The second street", ["the second road", "second street"], "2️⃣"),
        W("È a cinque minuti", "It's five minutes away", ["it is five minutes away"], "⏱️"),
      ]),
    ]),
    ("it-people-desc", "Describing People", "Height, hair and character — words change for boys and girls.", [
      ("it-pd-l1", "Appearance", [
        W("alto", "Tall", [], "🦒", note="A girl is alta."),
        W("basso", "Short", [], "🐁", note="A girl is bassa."),
        W("magro", "Thin", ["slim"], "🧍"),
        W("i capelli biondi", "Blond hair", ["fair hair", "blonde hair"], "👱", note="Capelli is normally plural, like 'trousers' in English."),
        W("gli occhi azzurri", "Blue eyes", [], "👀", note="Gli is said like the 'lli' in million: lyee."),
        W("la barba", "Beard", ["a beard"], "🧔"),
      ]),
      ("it-pd-l2", "Character", [
        W("simpatico", "Nice", ["friendly", "kind"], "😊", note="Simpatico means nice or friendly, not 'sympathetic'. A girl is simpatica."),
        W("timido", "Shy", [], "🙈", note="A girl is timida."),
        W("divertente", "Funny", ["fun"], "😂", note="Divertente is the same for boys and girls."),
        W("laborioso", "Hard-working", ["hardworking", "hard working"], "💪", note="A girl is laboriosa."),
        W("pigro", "Lazy", [], "🦥", note="A girl is pigra."),
        W("generoso", "Generous", [], "🎁", note="A girl is generosa."),
      ]),
    ]),
    ("it-work", "Work & Occupations", "What do you do? — jobs and talking about work.", [
      ("it-work-l1", "Occupations", [
        W("l'insegnante", "Teacher", ["the teacher"], "👨‍🏫", note="Insegnante is the same for a man or a woman."),
        W("l'infermiera", "Nurse", ["the nurse"], "👩‍⚕️", note="A male nurse is l'infermiere."),
        W("il poliziotto", "Police officer", ["policeman", "the police officer"], "👮", note="A woman is la poliziotta."),
        W("il cuoco", "Cook", ["chef", "the cook"], "👨‍🍳", note="A woman is la cuoca."),
        W("il pompiere", "Firefighter", ["fireman", "the firefighter"], "👨‍🚒"),
        W("l'agricoltore", "Farmer", ["the farmer"], "👨‍🌾"),
      ]),
      ("it-work-l2", "The world of work", [
        W("Che lavoro fai?", "What do you do?", ["what is your job", "what's your job"], "💼", note="Word for word: what work do you do?"),
        W("l'ufficio", "Office", ["the office"], "🏢"),
        W("il capo", "Boss", ["the boss"], "👔", note="Capo also means 'head'."),
        W("la riunione", "Meeting", ["the meeting"], "🗓️"),
        W("lo stipendio", "Salary", ["wages", "pay"], "💶", note="It's lo, not il, because stipendio starts with s+consonant."),
        W("le vacanze", "Holidays", ["holiday", "vacation"], "🏝️", note="Vacanze is always plural."),
      ]),
    ]),
    ("it-dialogues", "Short Conversations", "Real back-and-forth exchanges, not just single words.", [
      ("it-dlg-l1", "At a café", [
        W("Cosa prende?", "What can I get you?", ["what would you like", "what will you have"], "☕", note="The waiter is polite, so he says prende (you take)."),
        W("Un cappuccino, per favore", "A cappuccino, please", ["a coffee with milk please"], "🥛", note="Italians drink cappuccino only at breakfast, never after a meal!"),
        W("Altro?", "Anything else?", [], "➕"),
        W("Basta così, grazie", "That's all, thanks", ["nothing else thanks", "that's all thank you"], "🙏", note="Word for word: it's enough like this."),
      ]),
      ("it-dlg-l2", "Asking for help", [
        W("Può aiutarmi?", "Can you help me?", ["could you help me"], "🆘", note="Può is the polite 'you can'. See Tu & Lei."),
        W("Certo", "Of course", ["sure", "certainly"], "👍"),
        W("Mi sono perso", "I'm lost", ["i am lost"], "🗺️", note="A girl says mi sono persa."),
        W("Parla inglese?", "Do you speak English?", [], "🇬🇧"),
      ]),
    ]),
    ("it-emergency", "Health & Emergencies", "The phrases you hope you'll never need — but should know anyway.", [
      ("it-emg-l1", "Getting help fast", [
        W("Aiuto!", "Help!", [], "🆘", note="Said 'eye-OO-toh'."),
        W("Chiami un'ambulanza", "Call an ambulance", [], "🚑", note="That's the polite way. To a friend say chiama un'ambulanza."),
        W("È un'emergenza", "It's an emergency", ["it is an emergency"], "🚨"),
        W("Ho perso il passaporto", "I've lost my passport", ["i have lost my passport", "i lost my passport"], "🛂"),
        W("Sono allergico alla frutta a guscio", "I'm allergic to nuts", ["i am allergic to nuts"], "🌰", note="Frutta a guscio means tree nuts, like almonds and walnuts. Peanuts are arachidi. A girl says allergica."),
        W("Dov'è l'ospedale?", "Where is the hospital?", ["where's the hospital"], "🏥"),
      ]),
    ]),
  ]),
  ("Upper-Intermediate", [
    ("it-opinions", "Opinions & Agreement", "Saying what you think, and whether you agree.", [
      ("it-opn-l1", "What do you think?", [
        W("Penso di sì", "I think so", [], "👍"),
        W("Penso di no", "I don't think so", ["i do not think so"], "👎"),
        W("Sono d'accordo", "I agree", [], "🤝"),
        W("Non sono d'accordo", "I disagree", ["i don't agree", "i do not agree"], "🙅"),
        W("Secondo me", "In my opinion", [], "💭", note="Word for word: according to me."),
        W("Dipende", "It depends", ["that depends"], "⚖️"),
      ]),
    ]),
    ("it-past", "Talking About the Past", "The past tense for things that happened and finished: sono andato, ho mangiato, ho parlato.", [
      ("it-pst-l1", "What did you do?", [
        W("Ieri sono andato in spiaggia", "Yesterday I went to the beach", ["i went to the beach yesterday"], "🏖️", note="A girl says andata. Verbs of going use sono, most others use ho."),
        W("Ho mangiato la pasta", "I ate pasta", ["i had pasta", "i have eaten pasta"], "🍝"),
        W("Ho parlato con mia nonna", "I talked to my grandma", ["i spoke to my grandmother", "i talked to my grandmother"], "📞"),
        W("Abbiamo guardato un film", "We watched a film", ["we saw a film", "we watched a movie"], "🎬"),
        W("Che cosa hai fatto?", "What did you do?", [], "❓"),
        W("Era molto divertente", "It was really fun", ["it was a lot of fun", "it was very fun"], "🎉", note="Era is a second past tense, for saying how things were."),
      ]),
    ]),
    ("it-storytelling", "Telling a Story", "The linking words that turn events into a story.", [
      ("it-str-l1", "Once upon a time", [
        W("C'era una volta", "Once upon a time", [], "📖", note="Every Italian fairy tale (fiaba) starts like this."),
        W("Prima", "First", ["first of all", "firstly"], "1️⃣"),
        W("Poi", "Then", ["next", "after that"], "➡️"),
        W("All'improvviso", "Suddenly", ["all of a sudden"], "⚡"),
        W("Alla fine", "In the end", ["finally", "at the end"], "🏁"),
        W("E vissero felici e contenti", "And they lived happily ever after", ["they lived happily ever after"], "🏰"),
      ]),
    ]),
    ("it-register", "Tu & Lei", "Friendly tu for family and friends, polite Lei for strangers and older people.", [
      ("it-reg-l1", "Polite or friendly?", [
        W("signore", "Mr", ["sir", "mister"], "🎩", note="Before a name it loses the e: signor Rossi."),
        W("signora", "Mrs", ["madam", "ma'am"], "👒"),
        W("Lei", "You (polite)", ["you formal", "you"], "🤵", note="Lei is often written with a capital L when it means a polite 'you'. For more than one person, say voi."),
        W("tu", "You (friendly)", ["you informal", "you"], "🙂"),
        W("Come sta?", "How are you? (polite)", ["how are you formal", "how are you"], "🧑‍💼"),
        W("Piacere", "Pleased to meet you", ["nice to meet you"], "🤝", note="Piacere literally means 'pleasure'. It's the quick, everyday way to say it."),
      ]),
    ]),
    ("it-phone", "Phone Conversations", "Talking on the phone has its own set phrases.", [
      ("it-phn-l1", "On the line", [
        W("Pronto?", "Hello? (on the phone)", ["hello on the phone", "hello"], "📞", note="Pronto means 'ready'. Italians only say it when they pick up the phone."),
        W("Chi parla?", "Who's calling?", ["who is calling", "who's speaking"], "☎️"),
        W("Un attimo, per favore", "One moment, please", ["just a moment please", "hold on please"], "⏳"),
        W("Ti richiamo più tardi", "I'll call you later", ["i will call you later", "i'll call you back later"], "📱"),
        W("È caduta la linea", "We got cut off", ["the line went dead", "it cut off"], "📵", note="Word for word: the line has fallen."),
        W("Mi senti?", "Can you hear me?", [], "👂"),
      ]),
    ]),
    ("it-idioms", "Idioms & Expressions", "Phrases that don't translate word for word, but everyone in Italy knows.", [
      ("it-idm-l1", "How Italians really talk", [
        W("In bocca al lupo!", "Good luck!", ["break a leg"], "🐺", note="Word for word: into the wolf's mouth! You answer: crepi! (may it die)."),
        W("Costare un occhio della testa", "To cost an arm and a leg", ["to be very expensive"], "💸", note="Word for word: to cost an eye of the head."),
        W("Essere al settimo cielo", "To be over the moon", ["to be very happy"], "🌤️", note="Word for word: to be in seventh heaven."),
        W("È facile come bere un bicchier d'acqua", "It's a piece of cake", ["it's easy", "easy peasy"], "🥛", note="Word for word: it's as easy as drinking a glass of water."),
        W("Prendere due piccioni con una fava", "To kill two birds with one stone", ["two birds with one stone"], "🐦", note="Word for word: to catch two pigeons with one bean."),
      ]),
    ]),
  ]),
  ("Advanced", [
    ("it-business", "Business Italian", "Vocabulary for the office and the meeting room.", [
      ("it-biz-l1", "At the office", [
        W("l'azienda", "Company", ["business", "firm", "the company"], "🏭"),
        W("il cliente", "Client", ["customer", "the client"], "🤝"),
        W("il contratto", "Contract", ["the contract"], "📝"),
        W("il budget", "Budget", ["the budget"], "📊", note="Italians use the English word budget."),
        W("la fattura", "Invoice", ["bill", "the invoice"], "🧾"),
        W("le vendite", "Sales", ["the sales"], "📈"),
      ]),
    ]),
    ("it-news", "News & Society", "The words behind newspapers and the evening news.", [
      ("it-news-l1", "Reading the news", [
        W("le notizie", "The news", ["news"], "📰", note="One piece of news is una notizia. The TV news is il telegiornale."),
        W("il governo", "Government", ["the government"], "🏛️"),
        W("le elezioni", "Elections", ["the elections"], "🗳️"),
        W("l'economia", "Economy", ["the economy"], "💹"),
        W("l'ambiente", "Environment", ["the environment"], "🌍"),
        W("la società", "Society", [], "👥"),
      ]),
    ]),
    ("it-future", "Future & 'Would'", "Will, would and 'if I were…' — where Italian verbs get interesting.", [
      ("it-fut-l1", "What will happen?", [
        W("Domani andrò al cinema", "Tomorrow I'll go to the cinema", ["i will go to the cinema tomorrow", "tomorrow i will go to the cinema"], "🍿", note="Italians often use the present for the future too: domani vado al cinema."),
        W("Pioverà", "It will rain", ["it'll rain"], "☔"),
        W("Sarà facile", "It will be easy", ["it'll be easy"], "✅"),
        W("Mi piacerebbe viaggiare", "I would like to travel", ["i'd like to travel"], "🧭"),
        W("Potrebbe aiutarmi?", "Could you help me?", [], "🙏"),
        W("Se fossi ricco, comprerei una barca", "If I were rich, I would buy a boat", ["if i was rich i would buy a boat", "if i were rich i'd buy a boat"], "⛵"),
      ]),
    ]),
    ("it-proverbs", "Proverbs & Sayings", "Proverbi — sayings every Italian child grows up with.", [
      ("it-prv-l1", "Common sayings", [
        W("Meglio tardi che mai", "Better late than never", [], "⏰"),
        W("Chi dorme non piglia pesci", "You snooze, you lose", ["you snooze you lose", "the early bird catches the worm", "early bird gets the worm"], "🌅", note="Word for word: who sleeps catches no fish."),
        W("Chi va piano va sano e va lontano", "Slow and steady wins the race", ["slowly but surely", "slow and steady"], "🐢", note="Word for word: who goes slowly goes safely and goes far."),
        W("Tra il dire e il fare c'è di mezzo il mare", "Easier said than done", ["it is easier said than done"], "🌊", note="Word for word: between saying and doing there is the sea."),
        W("L'unione fa la forza", "Strength in unity", ["there is strength in numbers", "united we stand"], "🤝", note="Word for word: union makes strength."),
      ]),
    ]),
    ("it-debate", "Discussion & Debate", "Weighing up pros and cons like a native speaker.", [
      ("it-dbt-l1", "Weighing it up", [
        W("Da un lato", "On the one hand", [], "☝️"),
        W("Dall'altro lato", "On the other hand", [], "✋"),
        W("Tuttavia", "However", ["nevertheless"], "🔄"),
        W("Inoltre", "Moreover", ["furthermore", "what's more", "besides"], "➕"),
        W("i vantaggi", "The advantages", ["advantages", "pros"], "✅"),
        W("gli svantaggi", "The disadvantages", ["disadvantages", "cons", "drawbacks"], "❌", note="Gli is used before s+consonant: gli svantaggi."),
      ]),
    ]),
  ]),
  ("Fluency & Mastery", [
    ("it-slang", "Slang & Casual Speech", "The words you won't find in a textbook, but hear everywhere in Italy.", [
      ("it-slg-l1", "Sounding natural", [
        W("Che forte!", "That's so cool!", ["how cool", "cool", "that's cool"], "😎", note="Word for word: how strong! Everyone says it."),
        W("Raga", "Guys", ["mates", "everyone", "you lot"], "🤙", note="Short for ragazzi (boys, kids). Friends say 'Ciao, raga!'"),
        W("Spacca!", "It's brilliant!", ["it rocks", "it's great", "it's amazing"], "🤘", note="Word for word: it smashes!"),
        W("Uffa!", "What a pain!", ["what a drag", "how annoying", "ugh"], "🙄", note="Kids say uffa! when they are bored or annoyed."),
        W("Non ci credo!", "I can't believe it!", ["i'm amazed", "i am amazed", "i'm shocked"], "🤯"),
        W("Non mi importa", "I don't care", ["i couldn't care less", "whatever"], "🤷"),
      ]),
    ]),
    ("it-reactions", "Humour & Reactions", "The little exclamations real conversations run on.", [
      ("it-rxn-l1", "Reacting naturally", [
        W("Dai!", "Come on!", ["come on", "go on"], "💪", note="Dai is used all the time: come on, go on, please!"),
        W("Speriamo!", "I hope so!", ["hopefully", "i hope so", "fingers crossed"], "🤞"),
        W("Peccato!", "What a shame!", ["what a pity", "too bad"], "😞"),
        W("Ma dai!", "No way!", ["you're joking", "that's not true"], "😮", note="Said with a rising voice, it means 'you're kidding!'"),
        W("Mamma mia!", "Oh my goodness!", ["oh my god", "wow", "goodness me", "oh dear"], "😱", note="Yes, Italians really say it, and they say it a lot!"),
      ]),
    ]),
    ("it-reading", "Reading a Short Paragraph", "Four connected sentences — read them as a whole story.", [
      ("it-rdg-l1", "Lucia's week", [
        W("Mi chiamo Lucia e abito a Roma.", "My name is Lucia and I live in Rome.", ["my name is lucia and i live in rome"], "🙋‍♀️"),
        W("Ogni mattina vado a scuola in bicicletta.", "Every morning I go to school by bike.", ["every morning i cycle to school"], "🚲"),
        W("Il pomeriggio gioco con il mio cane al parco.", "In the afternoon I play with my dog in the park.", [], "🐕"),
        W("La domenica mangiamo la pasta con i miei nonni.", "On Sundays we eat pasta with my grandparents.", ["on sundays we have pasta with my grandparents"], "🍝"),
      ]),
    ]),
    ("it-casual-greet", "Casual Greetings", "What people actually say when they bump into a friend.", [
      ("it-cgr-l1", "Hey, what's up?", [
        W("Che c'è di nuovo?", "What's up?", ["what's new", "what is up"], "🤙", note="Word for word: what is there of new?"),
        W("Come va?", "How's it going?", ["how is it going"], "🙂", note="Word for word: how goes it?"),
        W("Quanto tempo!", "Long time no see!", ["it's been ages", "long time no see"], "🤗", note="Word for word: how much time!"),
        W("Ciao!", "Hi there!", ["hiya", "hey", "hi", "bye"], "👋", note="Ciao means both hello and goodbye between friends and family."),
        W("A domani!", "See you tomorrow!", ["see you tomorrow"], "🌙"),
      ]),
    ]),
    ("it-professional", "Formal Italian", "The language of letters, emails and official occasions.", [
      ("it-prof-l1", "Writing formally", [
        W("Gentili Signori", "Dear Sir or Madam", ["dear sir", "dear madam", "dear sirs"], "✉️"),
        W("Distinti saluti", "Yours faithfully", ["yours sincerely"], "🖋️", note="The classic way to end a formal letter."),
        W("La ringrazio per l'aiuto", "Thank you for your help (formal)", ["i appreciate your help", "thank you for your help"], "🙏"),
        W("Resto a Sua disposizione", "I remain at your disposal", ["i am at your service"], "🤝", note="In formal letters Sua is traditionally written with a capital S."),
        W("Cordiali saluti", "Kind regards", ["best regards", "warm regards"], "📧"),
      ]),
    ]),
    ("it-literary", "Songs & Poetry", "The poetic words behind Italian songs, films and poems.", [
      ("it-lit-l1", "Words from songs and poems", [
        W("l'anima", "Soul", ["the soul"], "🕊️", note="Anima mia ('my soul') is a loving way to say 'my dear'."),
        W("la luna", "Moon", ["the moon"], "🌙"),
        W("sognare", "To dream", ["dream"], "💭", note="As in the famous song Volare: 'nel blu dipinto di blu'."),
        W("il mare", "Sea", ["the sea"], "🌊"),
        W("per sempre", "Forever", ["for ever", "for good"], "♾️"),
      ]),
    ]),
  ]),
]


def build():
    levels, seen_ids, seen_text = [], set(), {}
    for level_name, units in COURSE:
        level = {"level": level_name, "units": []}
        for unit_id, unit_title, tagline, lessons in units:
            unit = {"id": unit_id, "title": unit_title, "tagline": tagline, "lessons": []}
            for lesson_id, lesson_title, words in lessons:
                lesson = {"id": lesson_id, "title": lesson_title, "words": []}
                ens = set()
                for i, (text, en, accept, emoji, extra) in enumerate(words):
                    wid = f"{lesson_id}-{i}"
                    assert wid not in seen_ids, wid
                    assert en.lower() not in ens, f"duplicate English in {lesson_id}: {en}"
                    if text.lower() in seen_text:
                        raise SystemExit(f"duplicate Italian '{text}' in {wid} and {seen_text[text.lower()]}")
                    seen_ids.add(wid); ens.add(en.lower()); seen_text[text.lower()] = wid
                    w = {"id": wid, "text": text, "en": en}
                    accept = [a.lower() for a in accept if a.lower() != en.lower()]
                    if accept:
                        w["accept"] = accept
                    if emoji:
                        w["emoji"] = emoji
                    w.update(extra)
                    lesson["words"].append(w)
                unit["lessons"].append(lesson)
            level["units"].append(unit)
        levels.append(level)
    return levels


if __name__ == "__main__":
    levels = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(levels, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    units = [u for l in levels for u in l["units"]]
    lessons = [le for u in units for le in u["lessons"]]
    words = [w for le in lessons for w in le["words"]]
    print(f"{OUT}: {len(levels)} levels, {len(units)} units, {len(lessons)} lessons, {len(words)} words")
