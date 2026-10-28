"""Build courses/fr/curriculum.json (the French course) from the readable lists below.

Run: python tools/content/build_french.py
Each word: (french, english, [other accepted English answers], emoji, {extra fields})
France French throughout, same units and order as the Spanish course, with the
grammar units swapped for French ones (Le & La, Être & Avoir, Tu & Vous).
Word ids: fr-<lesson>-<n>. A space before ? and ! (French style) is written as a
non-breaking space so the mark never wraps onto a line of its own.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "courses" / "fr" / "curriculum.json"
NBSP = " "


def W(text, en, accept=None, emoji=None, **extra):
    text = text.replace(" ?", NBSP + "?").replace(" !", NBSP + "!")
    return (text, en, accept or [], emoji, extra)


COURSE = [
  ("Beginner", [
    ("fr-basics1", "Greetings", "The words you'll use every single day.", [
      ("fr-b1-l1", "Hello & thanks", [
        W("Bonjour", "Hello", ["hi", "hiya", "good morning", "good day"], "👋", note="Use bonjour all day. In the evening it becomes bonsoir."),
        W("Merci", "Thank you", ["thanks", "thank you very much"], "🙏"),
        W("Oui", "Yes", ["yeah"], "✅", note="Sounds like 'wee'."),
        W("Non", "No", [], "❌", note="Almost the same as English! Say it through your nose and don't finish the n: noh(n)."),
        W("Pardon", "Sorry", ["excuse me", "pardon", "pardon me"], "😔", note="Same spelling as English, said par-DOHN."),
        W("De rien", "You're welcome", ["no problem", "not at all", "you are welcome"], "😌"),
      ]),
      ("fr-b1-l2", "How are you?", [
        W("Ça va ?", "How are you?", ["how's it going", "how are things", "how are you doing"], "🙂", note="Ask it with ça va? and answer it with ça va! (I'm fine)."),
        W("Bien", "Good", ["well", "fine", "ok"], "👍"),
        W("Très bien", "Very good", ["very well", "really good"], "😄"),
        W("Et toi ?", "And you?", ["what about you", "and yourself"], "🫵"),
        W("Au revoir", "Goodbye", ["bye", "bye bye"], "👋"),
        W("À plus tard", "See you later", ["see you", "bye for now", "later"], "🙋"),
      ]),
    ]),
    ("fr-numbers1", "Numbers 1–10", "Count on your fingers together.", [
      ("fr-n1-l1", "One to five", [
        W("un", "One", ["1"], "1️⃣"), W("deux", "Two", ["2"], "2️⃣"), W("trois", "Three", ["3"], "3️⃣"),
        W("quatre", "Four", ["4"], "4️⃣"), W("cinq", "Five", ["5"], "5️⃣"),
      ]),
      ("fr-n1-l2", "Six to ten", [
        W("six", "Six", ["6"], "6️⃣", note="Said 'seess'."), W("sept", "Seven", ["7"], "7️⃣", note="The p is silent: set."),
        W("huit", "Eight", ["8"], "8️⃣", note="Said 'weet'."), W("neuf", "Nine", ["9"], "9️⃣"), W("dix", "Ten", ["10"], "🔟", note="Said 'deess'."),
      ]),
    ]),
    ("fr-numbers2", "Bigger Numbers", "Eleven, twenty, and counting by tens.", [
      ("fr-n2-l1", "Eleven to fifteen", [
        W("onze", "Eleven", ["11"]), W("douze", "Twelve", ["12"]), W("treize", "Thirteen", ["13"]),
        W("quatorze", "Fourteen", ["14"]), W("quinze", "Fifteen", ["15"]),
      ]),
      ("fr-n2-l2", "Counting by tens", [
        W("vingt", "Twenty", ["20"], note="The g and t are silent: van."), W("trente", "Thirty", ["30"]), W("quarante", "Forty", ["40"]),
        W("cinquante", "Fifty", ["50"]), W("cent", "One hundred", ["100", "a hundred", "hundred"], "💯", note="The t is silent: son."),
      ]),
    ]),
    ("fr-family", "Family", "Maman, papa and everyone in between. Le = he, la = she.", [
      ("fr-fam-l1", "Close family", [
        W("la mère", "Mother", ["mum", "mom", "mummy", "the mother"], "👩", note="Maman is 'mum'."),
        W("le père", "Father", ["dad", "daddy", "the father"], "👨", note="Papa is 'dad'."),
        W("le frère", "Brother", ["the brother"], "👦"),
        W("la sœur", "Sister", ["the sister"], "👧"),
        W("le fils", "Son", ["the son"], "🧒", note="The l is silent: feess."),
        W("la fille", "Daughter", ["the daughter", "girl"], "👶", note="Fille also means 'girl'."),
      ]),
      ("fr-fam-l2", "Grandparents & more", [
        W("le grand-père", "Grandfather", ["grandad", "grandpa", "granddad"], "👴"),
        W("la grand-mère", "Grandmother", ["grandma", "granny", "nan", "nana"], "👵"),
        W("l'oncle", "Uncle", ["the uncle"], "🧔"),
        W("la tante", "Aunt", ["auntie", "aunty"], "👩‍🦰"),
        W("le cousin", "Cousin", ["cousin (boy)"], "🧑", note="A girl cousin is la cousine."),
        W("la famille", "Family", ["the family"], "👨‍👩‍👧‍👦"),
      ]),
    ]),
    ("fr-colors", "Colours & Shapes", "The colour usually comes after the thing: une voiture rouge, a red car.", [
      ("fr-col-l1", "Colours", [
        W("rouge", "Red", [], "🔴", swatch="#c0392b"),
        W("bleu", "Blue", [], "🔵", swatch="#1f5fa8"),
        W("vert", "Green", [], "🟢", swatch="#2e8b57"),
        W("jaune", "Yellow", [], "🟡", swatch="#f1c40f"),
        W("noir", "Black", [], "⚫", swatch="#222222"),
        W("blanc", "White", [], "⚪", swatch="#f8f8f8"),
      ]),
      ("fr-col-l2", "Shapes", [
        W("le cercle", "Circle", ["a circle"], "⭕"),
        W("le carré", "Square", ["a square"], "🟥"),
        W("le triangle", "Triangle", ["a triangle"], "🔺"),
        W("l'étoile", "Star", ["a star"], "⭐"),
        W("le cœur", "Heart", ["a heart"], "❤️"),
      ]),
    ]),
    ("fr-food", "Food & Drink", "Croissants, cheese and everything in between.", [
      ("fr-food-l1", "Foods", [
        W("le pain", "Bread", [], "🍞"),
        W("le fromage", "Cheese", [], "🧀"),
        W("le riz", "Rice", [], "🍚"),
        W("la pomme", "Apple", ["an apple"], "🍎"),
        W("le poulet", "Chicken", [], "🍗"),
        W("l'œuf", "Egg", ["an egg"], "🥚"),
      ]),
      ("fr-food-l2", "Drinks & taste", [
        W("l'eau", "Water", [], "💧", note="Eau sounds just like 'oh'."),
        W("le lait", "Milk", [], "🥛"),
        W("le jus", "Juice", [], "🧃"),
        W("le café", "Coffee", [], "☕"),
        W("délicieux", "Tasty", ["delicious", "yummy"], "😋"),
        W("épicé", "Spicy", ["hot"], "🌶️"),
      ]),
    ]),
    ("fr-phrases", "Everyday Phrases", "Small words that unlock real conversations.", [
      ("fr-phr-l1", "Asking for things", [
        W("s'il vous plaît", "Please", [], "🥺", note="To friends and family, say s'il te plaît."),
        W("je voudrais", "I would like", ["i'd like", "i want"], "🙋"),
        W("j'ai besoin de", "I need", [], "🙌"),
        W("Où sont les toilettes ?", "Where is the toilet?", ["where's the toilet", "where is the bathroom", "where's the bathroom", "where are the toilets"], "🚻"),
        W("Je ne comprends pas", "I don't understand", ["i do not understand"], "🤷"),
        W("Plus lentement, s'il vous plaît", "Slower, please", ["more slowly please", "slowly please"], "🐢"),
      ]),
      ("fr-phr-l2", "Question words", [
        W("Quoi ?", "What?", [], "❓"),
        W("Qui ?", "Who?", [], "🧑"),
        W("Où ?", "Where?", [], "📍"),
        W("Quand ?", "When?", [], "🕐"),
        W("Pourquoi ?", "Why?", [], "🤔"),
        W("Combien ?", "How much?", ["how many"], "💰"),
      ]),
    ]),
    ("fr-time", "Time & Days", "Days of the week — and no capital letters in French!", [
      ("fr-time-l1", "Weekdays", [
        W("lundi", "Monday"), W("mardi", "Tuesday"), W("mercredi", "Wednesday"),
        W("jeudi", "Thursday"), W("vendredi", "Friday"),
      ]),
      ("fr-time-l2", "Weekend & today", [
        W("samedi", "Saturday"), W("dimanche", "Sunday"),
        W("aujourd'hui", "Today", [], "📅"),
        W("demain", "Tomorrow", [], "🌅"),
        W("hier", "Yesterday", [], "⏪"),
      ]),
    ]),
    ("fr-places", "Places & Directions", "Getting around town.", [
      ("fr-pl-l1", "Places", [
        W("la maison", "House", ["home", "the house"], "🏠"),
        W("l'école", "School", ["the school"], "🏫"),
        W("la plage", "Beach", ["the beach"], "🏖️"),
        W("le parc", "Park", ["the park"], "🌳"),
        W("le magasin", "Shop", ["store", "the shop"], "🏪"),
        W("l'hôpital", "Hospital", ["the hospital"], "🏥", note="The h is silent: oh-pee-TAL."),
      ]),
      ("fr-pl-l2", "Directions", [
        W("à gauche", "On the left", ["left", "to the left"], "⬅️"),
        W("à droite", "On the right", ["right", "to the right"], "➡️"),
        W("tout droit", "Straight on", ["straight ahead", "straight"], "⬆️"),
        W("ici", "Here", [], "📌"),
        W("là-bas", "There", ["over there"], "👉"),
        W("près", "Near", ["close", "nearby"], "🤏"),
      ]),
    ]),
    ("fr-shopping", "Shopping & Money", "Prices, paying and 'just looking'.", [
      ("fr-shop-l1", "At the shop", [
        W("C'est combien ?", "How much is it?", ["how much does it cost", "how much"], "🏷️"),
        W("cher", "Expensive", ["dear"], "💸"),
        W("pas cher", "Cheap", ["inexpensive", "not expensive"], "🪙"),
        W("Je regarde seulement", "I'm just looking", ["just looking", "i am just looking"], "👀"),
        W("la taille", "Size", ["clothes size"], "👕"),
        W("Je le prends", "I'll take it", ["i will take it"], "🛍️"),
      ]),
      ("fr-shop-l2", "Paying up", [
        W("l'argent", "Money", [], "💶", note="Argent also means 'silver'."),
        W("la carte bancaire", "Card", ["bank card", "credit card", "debit card"], "💳"),
        W("en espèces", "In cash", ["cash"], "💵"),
        W("l'addition", "The bill", ["bill", "check", "the check"], "🧾"),
        W("la monnaie", "Change", ["the change"], "🪙"),
        W("la boutique de souvenirs", "Gift shop", ["souvenir shop", "the gift shop"], "🎁"),
      ]),
    ]),
    ("fr-travel", "Travel & Transport", "How you'll get to France — and around it.", [
      ("fr-trv-l1", "Getting around", [
        W("la voiture", "Car", ["the car"], "🚗"),
        W("le bus", "Bus", ["the bus"], "🚌"),
        W("le train", "Train", ["the train"], "🚆"),
        W("l'avion", "Plane", ["aeroplane", "airplane", "the plane"], "✈️"),
        W("le vélo", "Bike", ["bicycle", "the bike"], "🚲"),
        W("à pied", "On foot", ["walking"], "🚶"),
      ]),
      ("fr-trv-l2", "At the airport", [
        W("l'aéroport", "Airport", ["the airport"], "🛫"),
        W("le passeport", "Passport", ["the passport"], "🛂"),
        W("la valise", "Suitcase", ["the suitcase", "luggage"], "🧳"),
        W("le billet", "Ticket", ["the ticket"], "🎫"),
        W("la porte", "Gate", ["door", "the gate"], "🚪"),
        W("le vol", "Flight", ["the flight"], "🛬"),
      ]),
    ]),
    ("fr-weather", "Weather & Seasons", "Small talk that works anywhere — the French love to talk about the weather too!", [
      ("fr-wx-l1", "What's it like out?", [
        W("Il fait chaud", "It's hot", ["it is hot"], "🥵"),
        W("Il fait froid", "It's cold", ["it is cold"], "🥶"),
        W("Il y a du soleil", "It's sunny", ["it is sunny"], "☀️"),
        W("Il pleut", "It's raining", ["it is raining", "it rains"], "🌧️"),
        W("Il y a du vent", "It's windy", ["it is windy"], "💨"),
        W("C'est nuageux", "It's cloudy", ["it is cloudy"], "☁️"),
      ]),
      ("fr-wx-l2", "Seasons", [
        W("le printemps", "Spring", [], "🌸"),
        W("l'été", "Summer", [], "🌞"),
        W("l'automne", "Autumn", ["fall"], "🍂", note="The m is silent: oh-TON."),
        W("l'hiver", "Winter", [], "❄️"),
        W("le temps", "The weather", ["weather"], "🌦️", note="Temps also means 'time'."),
      ]),
    ]),
    ("fr-feelings", "Feelings & Health", "Saying how you actually feel.", [
      ("fr-feel-l1", "Feelings", [
        W("content", "Happy", ["glad", "pleased"], "😊", note="A girl says contente."),
        W("triste", "Sad", [], "😢"),
        W("fatigué", "Tired", [], "😴", note="A girl writes fatiguée. It sounds the same!"),
        W("fâché", "Angry", ["cross", "annoyed"], "😠", note="A girl writes fâchée."),
        W("nerveux", "Nervous", [], "😬", note="A girl says nerveuse."),
        W("Je m'ennuie", "I'm bored", ["i am bored", "bored"], "🥱"),
      ]),
      ("fr-feel-l2", "Feeling unwell", [
        W("J'ai mal à la tête", "I have a headache", ["my head hurts"], "🤕"),
        W("J'ai mal au ventre", "I have a tummy ache", ["my tummy hurts", "stomach ache", "my stomach hurts"], "🤢"),
        W("Je suis malade", "I'm ill", ["i am ill", "i'm sick", "i am sick"], "🤒"),
        W("le médecin", "Doctor", ["the doctor"], "🩺"),
        W("la pharmacie", "Pharmacy", ["chemist", "the chemist"], "💊"),
        W("J'ai de la fièvre", "I have a temperature", ["i have a fever"], "🌡️"),
      ]),
    ]),
    ("fr-sentences", "Putting It Together", "Whole sentences, built from everything so far.", [
      ("fr-sen-l1", "Talking about yourself", [
        W("Je m'appelle Anne", "My name is Anne", ["i'm called anne", "i am called anne"], "🙋"),
        W("J'ai dix ans", "I'm ten years old", ["i am ten", "i'm ten", "i am ten years old"], "🎂", note="In French you 'have' years: j'ai = I have."),
        W("Je viens d'Angleterre", "I'm from England", ["i am from england", "i come from england"], "🌍"),
        W("J'habite à Londres", "I live in London", [], "🏙️"),
        W("Je parle un peu français", "I speak a little French", ["i speak a bit of french"], "💬"),
        W("J'aime le chocolat", "I like chocolate", ["i love chocolate"], "🍫"),
      ]),
      ("fr-sen-l2", "A day in words", [
        W("Je me lève", "I get up", [], "⏰"),
        W("Je prends mon petit-déjeuner", "I have breakfast", ["i eat breakfast", "i have my breakfast"], "🥣"),
        W("Je vais à l'école", "I go to school", [], "🎒"),
        W("Je mange avec ma famille", "I eat with my family", ["i have lunch with my family"], "🍽️"),
        W("Je joue au parc", "I play in the park", [], "⚽"),
        W("Je me couche", "I go to bed", [], "🛏️"),
      ]),
    ]),
  ]),
  ("Elementary", [
    ("fr-gender", "Le & La", "Every French noun is a 'he' or a 'she' word — learn the little word in front.", [
      ("fr-gen-l1", "The: le or la?", [
        W("le chien", "The dog", ["dog"], "🐶"),
        W("le chat", "The cat", ["cat"], "🐱", note="The t is silent: sha."),
        W("la table", "The table", ["table"], "🍽️"),
        W("le livre", "The book", ["book"], "📖"),
        W("la fenêtre", "The window", ["window"], "🪟"),
      ]),
      ("fr-gen-l2", "A or an: un or une?", [
        W("une banane", "A banana", ["banana"], "🍌"),
        W("une orange", "An orange", ["orange"], "🍊"),
        W("un crayon", "A pencil", ["pencil"], "✏️"),
        W("une chaise", "A chair", ["chair"], "🪑"),
        W("des chaussures", "Some shoes", ["shoes"], "👟", note="Des means 'some' for more than one thing."),
      ]),
    ]),
    ("fr-routine", "Daily Routine", "The verbs and time words behind an ordinary day.", [
      ("fr-rtn-l1", "Morning to night", [
        W("Je me douche", "I have a shower", ["i shower", "i take a shower"], "🚿"),
        W("Je me brosse les dents", "I brush my teeth", [], "🪥"),
        W("Je m'habille", "I get dressed", [], "👕"),
        W("Je mange", "I eat", [], "🍴"),
        W("Je travaille", "I work", [], "💼"),
        W("Je dors", "I sleep", [], "😴"),
      ]),
      ("fr-rtn-l2", "What time is it?", [
        W("Quelle heure est-il ?", "What time is it?", ["what's the time"], "⏰"),
        W("Il est une heure", "It's one o'clock", ["it is one o'clock", "it's one"], "🕐"),
        W("Il est deux heures", "It's two o'clock", ["it is two o'clock", "it's two"], "🕑"),
        W("et demie", "Half past", ["and a half"], "🕧", note="Il est deux heures et demie: it's half past two."),
        W("le matin", "In the morning", ["the morning", "morning"], "🌄"),
        W("le soir", "In the evening", ["the evening", "evening", "at night"], "🌙"),
      ]),
    ]),
    ("fr-etreavoir", "Être & Avoir", "The two most important verbs: être (to be) and avoir (to have).", [
      ("fr-ea-l1", "Être: to be", [
        W("Je suis grand", "I'm tall", ["i am tall"], "📏", note="A girl says grande."),
        W("Je suis anglais", "I'm English", ["i am english"], "🇬🇧", note="A girl says anglaise."),
        W("C'est ma sœur", "She's my sister", ["she is my sister", "this is my sister", "it's my sister"], "👧"),
        W("Il est très gentil", "He's very nice", ["he is very nice", "he's very kind"], "😊"),
        W("Nous sommes une famille", "We are a family", ["we're a family"], "👨‍👩‍👧"),
      ]),
      ("fr-ea-l2", "Avoir: to have", [
        W("J'ai un chien", "I have a dog", ["i've got a dog"], "🐕"),
        W("Tu as faim ?", "Are you hungry?", [], "🍽️", note="In French you 'have hunger': avoir faim."),
        W("J'ai soif", "I'm thirsty", ["i am thirsty"], "🥤", note="You 'have thirst': avoir soif."),
        W("Il a froid", "He's cold", ["he is cold"], "🥶", note="You 'have cold': avoir froid."),
        W("Nous avons une voiture", "We have a car", ["we've got a car"], "🚙"),
      ]),
    ]),
    ("fr-compare", "Comparisons", "More than, less than, and the best.", [
      ("fr-cmp-l1", "More, less, most", [
        W("plus grand", "Bigger", ["larger", "taller"], "🐘"),
        W("plus petit", "Smaller", [], "🐭"),
        W("meilleur", "Better", ["best"], "👍"),
        W("pire", "Worse", ["worst"], "👎"),
        W("le plus rapide", "The fastest", ["fastest"], "🏃"),
        W("aussi grand que", "As tall as", ["as big as"], "📐"),
      ]),
    ]),
    ("fr-restaurant", "At the Restaurant", "Order a crêpe, ask for the menu and pay the bill.", [
      ("fr-res-l1", "Ordering food", [
        W("la carte", "The menu", ["menu"], "📜", note="Le menu in France means a set meal at a fixed price."),
        W("Pour moi, une crêpe", "A pancake for me", ["a crepe for me", "i'll have a pancake", "i'll have a crepe", "for me a pancake"], "🥞"),
        W("Qu'est-ce que tu veux boire ?", "What would you like to drink?", ["what do you want to drink"], "🥤"),
        W("sans oignon", "Without onion", ["no onion"], "🧅"),
        W("C'est délicieux !", "It's delicious!", ["it is delicious", "it's really good"], "😋"),
        W("L'addition, s'il vous plaît", "The bill, please", ["the check please", "bill please"], "🧾"),
      ]),
    ]),
    ("fr-plans", "Making Plans", "Arranging to meet up — the most useful conversation of all.", [
      ("fr-pln-l1", "Are you free?", [
        W("Tu es libre samedi ?", "Are you free on Saturday?", ["are you free saturday"], "📅"),
        W("On se voit ?", "Shall we meet up?", ["shall we meet", "do you want to meet"], "🤝"),
        W("À quelle heure ?", "What time?", ["at what time"], "⏰"),
        W("D'accord", "OK", ["okay", "alright", "all right", "agreed"], "👌", note="You'll hear d'accord all day long in France."),
        W("Désolé, je ne peux pas", "Sorry, I can't", ["sorry i cannot"], "🙅"),
        W("À bientôt !", "See you soon!", ["see you", "see you then"], "👋"),
      ]),
    ]),
  ]),
  ("Intermediate", [
    ("fr-connectors", "Connectors", "And, but, because, if — the words that join ideas together.", [
      ("fr-con-l1", "Joining ideas", [
        W("et", "And", [], "➕", note="The t is silent: ay."),
        W("mais", "But", [], "↔️"),
        W("parce que", "Because", [], "💡"),
        W("si", "If", [], "❔"),
        W("ou", "Or", [], "🔀", note="No accent: ou = or. With an accent: où = where."),
        W("aussi", "Also", ["too", "as well"], "🔁"),
      ]),
    ]),
    ("fr-directions2", "Giving Directions", "Full sentences for getting someone from A to B.", [
      ("fr-dir2-l1", "Turn here", [
        W("Tournez à gauche", "Turn left", ["turn to the left"], "⬅️"),
        W("Continuez tout droit", "Go straight on", ["keep going straight", "go straight ahead"], "⬆️"),
        W("Traversez la rue", "Cross the street", ["cross the road"], "🚸"),
        W("C'est à côté de la banque", "It's next to the bank", ["it is next to the bank"], "🏦"),
        W("la deuxième rue", "The second street", ["the second road", "second street"], "2️⃣"),
        W("C'est à cinq minutes", "It's five minutes away", ["it is five minutes away"], "⏱️"),
      ]),
    ]),
    ("fr-people-desc", "Describing People", "Height, hair and character — words change for boys and girls.", [
      ("fr-pd-l1", "Appearance", [
        W("grand", "Tall", ["big"], "🦒"),
        W("petit", "Short", ["small", "little"], "🐁"),
        W("mince", "Thin", ["slim"], "🧍"),
        W("les cheveux blonds", "Blond hair", ["fair hair", "blonde hair"], "👱"),
        W("les yeux bleus", "Blue eyes", [], "👀", note="Les yeux sounds like 'lay-zyuh'."),
        W("la barbe", "Beard", ["a beard"], "🧔"),
      ]),
      ("fr-pd-l2", "Character", [
        W("sympa", "Nice", ["friendly", "kind"], "😊"),
        W("timide", "Shy", [], "🙈"),
        W("drôle", "Funny", ["fun"], "😂"),
        W("travailleur", "Hard-working", ["hardworking", "hard working"], "💪"),
        W("paresseux", "Lazy", [], "🦥"),
        W("généreux", "Generous", [], "🎁"),
      ]),
    ]),
    ("fr-work", "Work & Occupations", "What do you do? — jobs and talking about work.", [
      ("fr-work-l1", "Occupations", [
        W("le professeur", "Teacher", ["the teacher"], "👨‍🏫"),
        W("l'infirmière", "Nurse", ["the nurse"], "👩‍⚕️"),
        W("le policier", "Police officer", ["policeman", "the police officer"], "👮"),
        W("le cuisinier", "Chef", ["cook", "the chef"], "👨‍🍳"),
        W("le pompier", "Firefighter", ["fireman", "the firefighter"], "👨‍🚒"),
        W("l'agriculteur", "Farmer", ["the farmer"], "👨‍🌾"),
      ]),
      ("fr-work-l2", "The world of work", [
        W("Qu'est-ce que tu fais dans la vie ?", "What do you do?", ["what is your job", "what's your job"], "💼"),
        W("le bureau", "Office", ["the office", "desk"], "🏢", note="Bureau also means 'desk'."),
        W("le patron", "Boss", ["the boss"], "👔"),
        W("la réunion", "Meeting", ["the meeting"], "🗓️"),
        W("le salaire", "Salary", ["wages", "pay"], "💶"),
        W("les vacances", "Holidays", ["holiday", "vacation"], "🏝️"),
      ]),
    ]),
    ("fr-dialogues", "Short Conversations", "Real back-and-forth exchanges, not just single words.", [
      ("fr-dlg-l1", "At a café", [
        W("Qu'est-ce que je vous sers ?", "What can I get you?", ["what would you like"], "☕"),
        W("Un café au lait, s'il vous plaît", "A white coffee, please", ["a coffee with milk please"], "🥛"),
        W("Autre chose ?", "Anything else?", [], "➕"),
        W("C'est tout, merci", "That's all, thanks", ["nothing else thanks", "that's all thank you"], "🙏"),
      ]),
      ("fr-dlg-l2", "Asking for help", [
        W("Vous pouvez m'aider ?", "Can you help me?", ["could you help me"], "🆘"),
        W("Bien sûr", "Of course", ["sure", "certainly"], "👍"),
        W("Je suis perdu", "I'm lost", ["i am lost"], "🗺️", note="A girl writes perdue."),
        W("Vous parlez anglais ?", "Do you speak English?", [], "🇬🇧"),
      ]),
    ]),
    ("fr-emergency", "Health & Emergencies", "The phrases you hope you'll never need — but should know anyway.", [
      ("fr-emg-l1", "Getting help fast", [
        W("Au secours !", "Help!", [], "🆘"),
        W("Appelez une ambulance", "Call an ambulance", [], "🚑"),
        W("C'est une urgence", "It's an emergency", ["it is an emergency"], "🚨"),
        W("J'ai perdu mon passeport", "I've lost my passport", ["i have lost my passport", "i lost my passport"], "🛂"),
        W("Je suis allergique aux fruits à coque", "I'm allergic to nuts", ["i am allergic to nuts"], "🥜", note="Fruits à coque means all kinds of nuts."),
        W("Où est l'hôpital ?", "Where is the hospital?", ["where's the hospital"], "🏥"),
      ]),
    ]),
  ]),
  ("Upper-Intermediate", [
    ("fr-opinions", "Opinions & Agreement", "Saying what you think, and whether you agree.", [
      ("fr-opn-l1", "What do you think?", [
        W("Je pense que oui", "I think so", [], "👍"),
        W("Je ne pense pas", "I don't think so", ["i do not think so"], "👎"),
        W("Je suis d'accord", "I agree", [], "🤝"),
        W("Je ne suis pas d'accord", "I disagree", ["i don't agree", "i do not agree"], "🙅"),
        W("À mon avis", "In my opinion", [], "💭"),
        W("Ça dépend", "It depends", ["that depends"], "⚖️"),
      ]),
    ]),
    ("fr-past", "Talking About the Past", "The past tense for things that happened and finished: je suis allé, j'ai mangé, j'ai parlé.", [
      ("fr-pst-l1", "What did you do?", [
        W("Hier, je suis allé à la plage", "Yesterday I went to the beach", ["i went to the beach yesterday"], "🏖️", note="A girl writes allée. It sounds the same."),
        W("J'ai mangé des crêpes", "I ate pancakes", ["i had pancakes", "i ate crepes", "i had crepes"], "🥞"),
        W("J'ai parlé avec ma grand-mère", "I talked to my grandma", ["i spoke to my grandmother", "i talked to my grandmother"], "📞"),
        W("Nous avons regardé un film", "We watched a film", ["we saw a film", "we watched a movie"], "🎬"),
        W("Qu'est-ce que tu as fait ?", "What did you do?", [], "❓"),
        W("C'était très amusant", "It was really fun", ["it was a lot of fun", "it was very fun"], "🎉"),
      ]),
    ]),
    ("fr-storytelling", "Telling a Story", "The linking words that turn events into a story.", [
      ("fr-str-l1", "Once upon a time", [
        W("Il était une fois", "Once upon a time", [], "📖"),
        W("D'abord", "First", ["first of all", "firstly"], "1️⃣"),
        W("Ensuite", "Then", ["next", "after that"], "➡️"),
        W("Tout à coup", "Suddenly", ["all of a sudden"], "⚡"),
        W("À la fin", "In the end", ["finally", "at the end"], "🏁"),
        W("Ils vécurent heureux", "And they lived happily ever after", ["they lived happily ever after"], "🏰"),
      ]),
    ]),
    ("fr-register", "Tu & Vous", "Friendly tu for family and friends, polite vous for strangers and older people.", [
      ("fr-reg-l1", "Polite or friendly?", [
        W("monsieur", "Mr", ["sir", "mister"], "🎩"),
        W("madame", "Mrs", ["madam", "ma'am"], "👒"),
        W("vous", "You (polite)", ["you formal", "you"], "🤵", note="Vous is also 'you' for more than one person."),
        W("tu", "You (friendly)", ["you informal", "you"], "🙂"),
        W("Comment allez-vous ?", "How are you? (polite)", ["how are you formal", "how are you"], "🧑‍💼"),
        W("Enchanté", "Pleased to meet you", ["nice to meet you"], "🤝", note="A woman writes enchantée. It sounds the same."),
      ]),
    ]),
    ("fr-phone", "Phone Conversations", "Talking on the phone has its own set phrases.", [
      ("fr-phn-l1", "On the line", [
        W("Allô ?", "Hello? (on the phone)", ["hello on the phone", "hello"], "📞", note="The French only say allô on the phone."),
        W("C'est de la part de qui ?", "Who's calling?", ["who is calling", "who's speaking"], "☎️"),
        W("Un instant, s'il vous plaît", "One moment, please", ["just a moment please", "hold on please"], "⏳"),
        W("Je te rappelle plus tard", "I'll call you later", ["i will call you later", "i'll call you back later"], "📱"),
        W("Ça a coupé", "We got cut off", ["the line went dead", "it cut off"], "📵"),
        W("Tu m'entends ?", "Can you hear me?", [], "👂"),
      ]),
    ]),
    ("fr-idioms", "Idioms & Expressions", "Phrases that don't translate word for word, but everyone in France knows.", [
      ("fr-idm-l1", "How French really talks", [
        W("avoir la tête dans les nuages", "To daydream", ["to have your head in the clouds"], "☁️"),
        W("c'est du gâteau", "It's a piece of cake", ["it's easy", "easy peasy"], "🍰", note="Word for word: it's some cake!"),
        W("poser un lapin", "To stand someone up", ["to not turn up"], "🐰", note="Word for word: to put down a rabbit!"),
        W("coûter les yeux de la tête", "To cost an arm and a leg", ["to be very expensive"], "💸", note="Word for word: to cost the eyes from your head."),
        W("avoir un chat dans la gorge", "To have a frog in your throat", ["to have a croaky voice"], "🐱", note="In French it's a cat, not a frog!"),
      ]),
    ]),
  ]),
  ("Advanced", [
    ("fr-business", "Business French", "Vocabulary for the office and the meeting room.", [
      ("fr-biz-l1", "At the office", [
        W("l'entreprise", "Company", ["business", "firm", "the company"], "🏭"),
        W("le client", "Client", ["customer", "the client"], "🤝"),
        W("le contrat", "Contract", ["the contract"], "📝"),
        W("le budget", "Budget", ["the budget"], "📊"),
        W("la facture", "Invoice", ["bill", "the invoice"], "🧾"),
        W("les ventes", "Sales", ["the sales"], "📈"),
      ]),
    ]),
    ("fr-news", "News & Society", "The words behind newspapers and the evening news.", [
      ("fr-news-l1", "Reading the news", [
        W("les infos", "The news", ["news"], "📰", note="Short for les informations."),
        W("le gouvernement", "Government", ["the government"], "🏛️"),
        W("les élections", "Elections", ["the elections"], "🗳️"),
        W("l'économie", "Economy", ["the economy"], "💹"),
        W("l'environnement", "Environment", ["the environment"], "🌍"),
        W("la société", "Society", [], "👥"),
      ]),
    ]),
    ("fr-future", "Future & 'Would'", "Will, would and 'if I were…' — where French verbs get interesting.", [
      ("fr-fut-l1", "What will happen?", [
        W("Demain, j'irai au cinéma", "Tomorrow I'll go to the cinema", ["i will go to the cinema tomorrow", "tomorrow i will go to the cinema"], "🍿"),
        W("Il pleuvra", "It will rain", ["it'll rain"], "☔"),
        W("Ce sera facile", "It will be easy", ["it'll be easy"], "✅"),
        W("J'aimerais voyager", "I would like to travel", ["i'd like to travel"], "🧭"),
        W("Pourriez-vous m'aider ?", "Could you help me?", [], "🙏"),
        W("Si j'étais riche, j'achèterais un bateau", "If I were rich, I would buy a boat", ["if i was rich i would buy a boat", "if i were rich i'd buy a boat"], "⛵"),
      ]),
    ]),
    ("fr-proverbs", "Proverbs & Sayings", "Proverbes — sayings every French child grows up with.", [
      ("fr-prv-l1", "Common sayings", [
        W("Mieux vaut tard que jamais", "Better late than never", [], "⏰"),
        W("L'avenir appartient à ceux qui se lèvent tôt", "The early bird catches the worm", ["early bird gets the worm"], "🌅", note="Word for word: the future belongs to those who get up early."),
        W("Petit à petit, l'oiseau fait son nid", "Slowly but surely", ["little by little", "slow and steady"], "🐦", note="Word for word: little by little, the bird builds its nest."),
        W("Qui se ressemble s'assemble", "Birds of a feather flock together", [], "👫"),
        W("Quand le chat n'est pas là, les souris dansent", "When the cat's away, the mice will play", ["when the cat is away the mice will play"], "🐭", note="Word for word: the mice dance!"),
      ]),
    ]),
    ("fr-debate", "Discussion & Debate", "Weighing up pros and cons like a native speaker.", [
      ("fr-dbt-l1", "Weighing it up", [
        W("D'un côté", "On the one hand", [], "☝️"),
        W("D'un autre côté", "On the other hand", [], "✋"),
        W("Cependant", "However", ["nevertheless"], "🔄"),
        W("De plus", "Moreover", ["furthermore", "what's more", "besides"], "➕"),
        W("les avantages", "The advantages", ["advantages", "pros"], "✅"),
        W("les inconvénients", "The disadvantages", ["disadvantages", "cons", "drawbacks"], "❌"),
      ]),
    ]),
  ]),
  ("Fluency & Mastery", [
    ("fr-slang", "Slang & Casual Speech", "The words you won't find in a textbook, but hear everywhere in France.", [
      ("fr-slg-l1", "Sounding natural", [
        W("C'est trop cool !", "That's so cool!", ["how cool", "cool", "that's cool"], "😎"),
        W("Mec", "Mate", ["dude", "buddy", "guy"], "🤙", note="Friends call each other mec, a bit like 'mate'."),
        W("Ça déchire !", "It's brilliant!", ["it rocks", "it's great", "it's amazing"], "🤘"),
        W("C'est relou !", "What a pain!", ["what a drag", "how annoying"], "🙄", note="Relou is lourd (heavy) said backwards. That's verlan, French backslang!"),
        W("J'hallucine !", "I can't believe it!", ["i'm amazed", "i am amazed", "i'm shocked"], "🤯"),
        W("Je m'en fiche", "I don't care", ["i don't mind", "whatever"], "🤷"),
      ]),
    ]),
    ("fr-reactions", "Humour & Reactions", "The little exclamations real conversations run on.", [
      ("fr-rxn-l1", "Reacting naturally", [
        W("Allez !", "Come on!", ["come on", "go on"], "💪"),
        W("J'espère bien !", "I hope so!", ["hopefully", "i hope so"], "🤞"),
        W("Dommage !", "What a shame!", ["what a pity", "too bad"], "😞"),
        W("C'est pas vrai !", "No way!", ["you're joking", "really"], "😮"),
        W("Oh là là !", "Oh my goodness!", ["oh my god", "wow", "goodness me", "oh dear"], "😱", note="Yes, the French really say it, and they say it a lot!"),
      ]),
    ]),
    ("fr-reading", "Reading a Short Paragraph", "Four connected sentences — read them as a whole story.", [
      ("fr-rdg-l1", "Lucie's week", [
        W("Je m'appelle Lucie et j'habite à Lyon.", "My name is Lucie and I live in Lyon.", ["my name is lucie and i live in lyon"], "🙋‍♀️"),
        W("Tous les matins, je vais à l'école à vélo.", "Every morning I go to school by bike.", ["every morning i cycle to school"], "🚲"),
        W("L'après-midi, je joue avec mon chien au parc.", "In the afternoon I play with my dog in the park.", [], "🐕"),
        W("Le dimanche, nous mangeons des crêpes avec mes grands-parents.", "On Sundays we eat pancakes with my grandparents.", ["on sundays we have pancakes with my grandparents", "on sundays we eat crepes with my grandparents"], "🥞"),
      ]),
    ]),
    ("fr-casual-greet", "Casual Greetings", "What people actually say when they bump into a friend.", [
      ("fr-cgr-l1", "Hey, what's up?", [
        W("Quoi de neuf ?", "What's up?", ["what's new", "what is up"], "🤙"),
        W("Ça roule ?", "How's it going?", ["how is it going"], "🙂", note="Word for word: is it rolling?"),
        W("Ça fait longtemps !", "Long time no see!", ["it's been ages", "long time no see"], "🤗"),
        W("Salut !", "Hi there!", ["hiya", "hey", "hi"], "👋", note="Salut also means 'bye' between friends."),
        W("À demain !", "See you tomorrow!", ["see you tomorrow"], "🌙"),
      ]),
    ]),
    ("fr-professional", "Formal French", "The language of letters, emails and official occasions.", [
      ("fr-prof-l1", "Writing formally", [
        W("Madame, Monsieur", "Dear Sir or Madam", ["dear sir", "dear madam"], "✉️"),
        W("Veuillez agréer mes salutations distinguées", "Yours faithfully", ["yours sincerely"], "🖋️", note="The classic French letter ending. It's long, but everyone uses it."),
        W("Je vous remercie de votre aide", "Thank you for your help (formal)", ["i appreciate your help", "thank you for your help"], "🙏"),
        W("Je reste à votre disposition", "I remain at your disposal", ["i am at your service"], "🤝"),
        W("Bien cordialement", "Kind regards", ["best regards", "warm regards"], "📧"),
      ]),
    ]),
    ("fr-literary", "Songs & Poetry", "The poetic words behind French songs, films and poems.", [
      ("fr-lit-l1", "Words from songs and poems", [
        W("l'âme", "Soul", ["the soul"], "🕊️"),
        W("la lune", "Moon", ["the moon"], "🌙", note="As in the old song Au clair de la lune."),
        W("rêver", "To dream", ["dream"], "💭"),
        W("la mer", "Sea", ["the sea"], "🌊"),
        W("pour toujours", "Forever", ["for ever", "always"], "♾️"),
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
                        raise SystemExit(f"duplicate French '{text}' in {wid} and {seen_text[text.lower()]}")
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
