"""Build courses/es/curriculum.json (the Spanish course) from the readable lists below.

Run: python tools/content/build_spanish.py
Each word: (spanish, english, [other accepted English answers], emoji, {extra fields})
Spain (Castilian) Spanish throughout. Word ids: es-<lesson>-<n>.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "courses" / "es" / "curriculum.json"


def W(text, en, accept=None, emoji=None, **extra):
    return (text, en, accept or [], emoji, extra)


COURSE = [
  ("Beginner", [
    ("es-basics1", "Greetings", "The words you'll use every single day.", [
      ("es-b1-l1", "Hello & thanks", [
        W("Hola", "Hello", ["hi", "hiya"], "👋", note="The h is always silent: OH-la."),
        W("Gracias", "Thank you", ["thanks", "thank you very much"], "🙏"),
        W("Sí", "Yes", ["yeah"], "✅"),
        W("No", "No", [], "❌"),
        W("Perdón", "Sorry", ["excuse me", "pardon", "pardon me"], "😔"),
        W("De nada", "You're welcome", ["no problem", "not at all", "you are welcome"], "😌"),
      ]),
      ("es-b1-l2", "How are you?", [
        W("¿Qué tal?", "How are you?", ["how's it going", "how are things", "how are you doing"], "🙂"),
        W("Bien", "Good", ["well", "fine", "ok"], "👍"),
        W("Muy bien", "Very good", ["very well", "really good"], "😄"),
        W("¿Y tú?", "And you?", ["what about you", "and yourself"], "🫵"),
        W("Adiós", "Goodbye", ["bye", "bye bye"], "👋"),
        W("Hasta luego", "See you later", ["see you", "bye for now", "later"], "🙋"),
      ]),
    ]),
    ("es-numbers1", "Numbers 1–10", "Count on your fingers together.", [
      ("es-n1-l1", "One to five", [
        W("uno", "One", ["1"], "1️⃣"), W("dos", "Two", ["2"], "2️⃣"), W("tres", "Three", ["3"], "3️⃣"),
        W("cuatro", "Four", ["4"], "4️⃣"), W("cinco", "Five", ["5"], "5️⃣"),
      ]),
      ("es-n1-l2", "Six to ten", [
        W("seis", "Six", ["6"], "6️⃣"), W("siete", "Seven", ["7"], "7️⃣"), W("ocho", "Eight", ["8"], "8️⃣"),
        W("nueve", "Nine", ["9"], "9️⃣"), W("diez", "Ten", ["10"], "🔟"),
      ]),
    ]),
    ("es-numbers2", "Bigger Numbers", "Eleven, twenty, and counting by tens.", [
      ("es-n2-l1", "Eleven to fifteen", [
        W("once", "Eleven", ["11"]), W("doce", "Twelve", ["12"]), W("trece", "Thirteen", ["13"]),
        W("catorce", "Fourteen", ["14"]), W("quince", "Fifteen", ["15"]),
      ]),
      ("es-n2-l2", "Counting by tens", [
        W("veinte", "Twenty", ["20"]), W("treinta", "Thirty", ["30"]), W("cuarenta", "Forty", ["40"]),
        W("cincuenta", "Fifty", ["50"]), W("cien", "One hundred", ["100", "a hundred", "hundred"], "💯"),
      ]),
    ]),
    ("es-family", "Family", "Mamá, papá and everyone in between. El = he, la = she.", [
      ("es-fam-l1", "Close family", [
        W("la madre", "Mother", ["mum", "mom", "mummy", "the mother"], "👩", note="Mamá is 'mum'."),
        W("el padre", "Father", ["dad", "daddy", "the father"], "👨", note="Papá is 'dad'."),
        W("el hermano", "Brother", ["the brother"], "👦"),
        W("la hermana", "Sister", ["the sister"], "👧"),
        W("el hijo", "Son", ["the son"], "🧒"),
        W("la hija", "Daughter", ["the daughter"], "👶"),
      ]),
      ("es-fam-l2", "Grandparents & more", [
        W("el abuelo", "Grandfather", ["grandad", "grandpa", "granddad"], "👴"),
        W("la abuela", "Grandmother", ["grandma", "granny", "nan", "nana"], "👵"),
        W("el tío", "Uncle", [], "🧔"),
        W("la tía", "Aunt", ["auntie", "aunty"], "👩‍🦰"),
        W("el primo", "Cousin", ["cousin (boy)"], "🧑"),
        W("la familia", "Family", ["the family"], "👨‍👩‍👧‍👦"),
      ]),
    ]),
    ("es-colors", "Colours & Shapes", "The colour comes after the thing: un coche rojo, a red car.", [
      ("es-col-l1", "Colours", [
        W("rojo", "Red", [], "🔴", swatch="#c0392b"),
        W("azul", "Blue", [], "🔵", swatch="#1f5fa8"),
        W("verde", "Green", [], "🟢", swatch="#2e8b57"),
        W("amarillo", "Yellow", [], "🟡", swatch="#f1c40f"),
        W("negro", "Black", [], "⚫", swatch="#222222"),
        W("blanco", "White", [], "⚪", swatch="#f8f8f8"),
      ]),
      ("es-col-l2", "Shapes", [
        W("el círculo", "Circle", ["a circle"], "⭕"),
        W("el cuadrado", "Square", ["a square"], "🟥"),
        W("el triángulo", "Triangle", ["a triangle"], "🔺"),
        W("la estrella", "Star", ["a star"], "⭐"),
        W("el corazón", "Heart", ["a heart"], "❤️"),
      ]),
    ]),
    ("es-food", "Food & Drink", "Tapas, tortilla and everything in between.", [
      ("es-food-l1", "Foods", [
        W("el pan", "Bread", [], "🍞"),
        W("el queso", "Cheese", [], "🧀"),
        W("el arroz", "Rice", [], "🍚"),
        W("la manzana", "Apple", ["an apple"], "🍎"),
        W("el pollo", "Chicken", [], "🍗"),
        W("el huevo", "Egg", ["an egg"], "🥚"),
      ]),
      ("es-food-l2", "Drinks & taste", [
        W("el agua", "Water", [], "💧", note="Agua is a 'she' word but uses el, to make it easier to say."),
        W("la leche", "Milk", [], "🥛"),
        W("el zumo", "Juice", [], "🧃", note="In Spain it's zumo; in Latin America, jugo."),
        W("el café", "Coffee", [], "☕"),
        W("rico", "Tasty", ["delicious", "yummy"], "😋"),
        W("picante", "Spicy", ["hot"], "🌶️"),
      ]),
    ]),
    ("es-phrases", "Everyday Phrases", "Small words that unlock real conversations.", [
      ("es-phr-l1", "Asking for things", [
        W("por favor", "Please", [], "🥺"),
        W("quiero", "I want", ["i would like", "i'd like"], "🙋"),
        W("necesito", "I need", [], "🙌"),
        W("¿Dónde está el baño?", "Where is the toilet?", ["where's the toilet", "where is the bathroom", "where's the bathroom"], "🚻"),
        W("No entiendo", "I don't understand", ["i do not understand"], "🤷"),
        W("Más despacio, por favor", "Slower, please", ["more slowly please", "slowly please"], "🐢"),
      ]),
      ("es-phr-l2", "Question words", [
        W("¿Qué?", "What?", [], "❓"),
        W("¿Quién?", "Who?", [], "🧑"),
        W("¿Dónde?", "Where?", [], "📍"),
        W("¿Cuándo?", "When?", [], "🕐"),
        W("¿Por qué?", "Why?", [], "🤔"),
        W("¿Cuánto?", "How much?", ["how many"], "💰"),
      ]),
    ]),
    ("es-time", "Time & Days", "Days of the week — and no capital letters in Spanish!", [
      ("es-time-l1", "Weekdays", [
        W("lunes", "Monday"), W("martes", "Tuesday"), W("miércoles", "Wednesday"),
        W("jueves", "Thursday"), W("viernes", "Friday"),
      ]),
      ("es-time-l2", "Weekend & today", [
        W("sábado", "Saturday"), W("domingo", "Sunday"),
        W("hoy", "Today", [], "📅"),
        W("mañana", "Tomorrow", [], "🌅", note="Mañana also means 'morning'."),
        W("ayer", "Yesterday", [], "⏪"),
      ]),
    ]),
    ("es-places", "Places & Directions", "Getting around town.", [
      ("es-pl-l1", "Places", [
        W("la casa", "House", ["home", "the house"], "🏠"),
        W("el colegio", "School", ["the school"], "🏫"),
        W("la playa", "Beach", ["the beach"], "🏖️"),
        W("el parque", "Park", ["the park"], "🌳"),
        W("la tienda", "Shop", ["store", "the shop"], "🏪"),
        W("el hospital", "Hospital", ["the hospital"], "🏥", note="The h is silent: os-pee-TAL."),
      ]),
      ("es-pl-l2", "Directions", [
        W("a la izquierda", "On the left", ["left", "to the left"], "⬅️"),
        W("a la derecha", "On the right", ["right", "to the right"], "➡️"),
        W("todo recto", "Straight on", ["straight ahead", "straight"], "⬆️"),
        W("aquí", "Here", [], "📌"),
        W("allí", "There", ["over there"], "👉"),
        W("cerca", "Near", ["close", "nearby"], "🤏"),
      ]),
    ]),
    ("es-shopping", "Shopping & Money", "Prices, paying and 'just looking'.", [
      ("es-shop-l1", "At the shop", [
        W("¿Cuánto cuesta?", "How much is it?", ["how much does it cost", "how much"], "🏷️"),
        W("caro", "Expensive", ["dear"], "💸"),
        W("barato", "Cheap", [], "🪙"),
        W("Solo estoy mirando", "I'm just looking", ["just looking", "i am just looking"], "👀"),
        W("la talla", "Size", ["clothes size"], "👕"),
        W("Me lo llevo", "I'll take it", ["i will take it"], "🛍️"),
      ]),
      ("es-shop-l2", "Paying up", [
        W("el dinero", "Money", [], "💶"),
        W("la tarjeta", "Card", ["bank card", "credit card"], "💳"),
        W("en efectivo", "In cash", ["cash"], "💵"),
        W("la cuenta", "The bill", ["bill", "check", "the check"], "🧾"),
        W("el cambio", "Change", ["the change"], "🪙"),
        W("la tienda de regalos", "Gift shop", ["souvenir shop", "the gift shop"], "🎁"),
      ]),
    ]),
    ("es-travel", "Travel & Transport", "How you'll get to Spain — and around it.", [
      ("es-trv-l1", "Getting around", [
        W("el coche", "Car", ["the car"], "🚗", note="Spain: coche. Latin America: carro or auto."),
        W("el autobús", "Bus", ["the bus"], "🚌"),
        W("el tren", "Train", ["the train"], "🚆"),
        W("el avión", "Plane", ["aeroplane", "airplane", "the plane"], "✈️"),
        W("la bici", "Bike", ["bicycle", "the bike"], "🚲"),
        W("a pie", "On foot", ["walking"], "🚶"),
      ]),
      ("es-trv-l2", "At the airport", [
        W("el aeropuerto", "Airport", ["the airport"], "🛫"),
        W("el pasaporte", "Passport", ["the passport"], "🛂"),
        W("la maleta", "Suitcase", ["the suitcase", "luggage"], "🧳"),
        W("el billete", "Ticket", ["the ticket"], "🎫"),
        W("la puerta", "Gate", ["door", "the gate"], "🚪"),
        W("el vuelo", "Flight", ["the flight"], "🛬"),
      ]),
    ]),
    ("es-weather", "Weather & Seasons", "Small talk that works anywhere — Spain mostly says hace sol!", [
      ("es-wx-l1", "What's it like out?", [
        W("Hace calor", "It's hot", ["it is hot"], "🥵"),
        W("Hace frío", "It's cold", ["it is cold"], "🥶"),
        W("Hace sol", "It's sunny", ["it is sunny"], "☀️"),
        W("Llueve", "It's raining", ["it is raining", "it rains"], "🌧️"),
        W("Hace viento", "It's windy", ["it is windy"], "💨"),
        W("Está nublado", "It's cloudy", ["it is cloudy"], "☁️"),
      ]),
      ("es-wx-l2", "Seasons", [
        W("la primavera", "Spring", [], "🌸"),
        W("el verano", "Summer", [], "🌞"),
        W("el otoño", "Autumn", ["fall"], "🍂"),
        W("el invierno", "Winter", [], "❄️"),
        W("el tiempo", "The weather", ["weather"], "🌦️", note="Tiempo also means 'time'."),
      ]),
    ]),
    ("es-feelings", "Feelings & Health", "Saying how you actually feel.", [
      ("es-feel-l1", "Feelings", [
        W("contento", "Happy", ["glad", "pleased"], "😊", note="A girl says contenta."),
        W("triste", "Sad", [], "😢"),
        W("cansado", "Tired", [], "😴", note="A girl says cansada."),
        W("enfadado", "Angry", ["cross", "annoyed"], "😠"),
        W("nervioso", "Nervous", [], "😬"),
        W("aburrido", "Bored", ["boring"], "🥱"),
      ]),
      ("es-feel-l2", "Feeling unwell", [
        W("Me duele la cabeza", "I have a headache", ["my head hurts"], "🤕"),
        W("Me duele la barriga", "I have a tummy ache", ["my tummy hurts", "stomach ache", "my stomach hurts"], "🤢"),
        W("Estoy enfermo", "I'm ill", ["i am ill", "i'm sick", "i am sick"], "🤒"),
        W("el médico", "Doctor", ["the doctor"], "🩺"),
        W("la farmacia", "Pharmacy", ["chemist", "the chemist"], "💊"),
        W("Tengo fiebre", "I have a temperature", ["i have a fever"], "🌡️"),
      ]),
    ]),
    ("es-sentences", "Putting It Together", "Whole sentences, built from everything so far.", [
      ("es-sen-l1", "Talking about yourself", [
        W("Me llamo Ana", "My name is Ana", ["i'm called ana", "i am called ana"], "🙋"),
        W("Tengo diez años", "I'm ten years old", ["i am ten", "i'm ten", "i am ten years old"], "🎂", note="In Spanish you 'have' years: tengo = I have."),
        W("Soy de Inglaterra", "I'm from England", ["i am from england"], "🌍"),
        W("Vivo en Londres", "I live in London", [], "🏙️"),
        W("Hablo un poco de español", "I speak a little Spanish", ["i speak a bit of spanish"], "💬"),
        W("Me gusta el chocolate", "I like chocolate", [], "🍫"),
      ]),
      ("es-sen-l2", "A day in words", [
        W("Me levanto", "I get up", [], "⏰"),
        W("Desayuno", "I have breakfast", ["i eat breakfast"], "🥣"),
        W("Voy al colegio", "I go to school", [], "🎒"),
        W("Como con mi familia", "I eat with my family", ["i have lunch with my family"], "🍽️"),
        W("Juego en el parque", "I play in the park", [], "⚽"),
        W("Me acuesto", "I go to bed", [], "🛏️"),
      ]),
    ]),
  ]),
  ("Elementary", [
    ("es-gender", "El & La", "Every Spanish noun is a 'he' or a 'she' word — learn the little word in front.", [
      ("es-gen-l1", "The: el or la?", [
        W("el perro", "The dog", ["dog"], "🐶"),
        W("el gato", "The cat", ["cat"], "🐱"),
        W("la mesa", "The table", ["table"], "🍽️"),
        W("el libro", "The book", ["book"], "📖"),
        W("la ventana", "The window", ["window"], "🪟"),
      ]),
      ("es-gen-l2", "A or an: un or una?", [
        W("un plátano", "A banana", ["banana"], "🍌"),
        W("una naranja", "An orange", ["orange"], "🍊"),
        W("un lápiz", "A pencil", ["pencil"], "✏️"),
        W("una silla", "A chair", ["chair"], "🪑"),
        W("unos zapatos", "Some shoes", ["shoes"], "👟"),
      ]),
    ]),
    ("es-routine", "Daily Routine", "The verbs and time words behind an ordinary day.", [
      ("es-rtn-l1", "Morning to night", [
        W("Me ducho", "I have a shower", ["i shower", "i take a shower"], "🚿"),
        W("Me lavo los dientes", "I brush my teeth", [], "🪥"),
        W("Me visto", "I get dressed", [], "👕"),
        W("Como", "I eat", [], "🍴"),
        W("Trabajo", "I work", [], "💼"),
        W("Duermo", "I sleep", [], "😴"),
      ]),
      ("es-rtn-l2", "What time is it?", [
        W("¿Qué hora es?", "What time is it?", ["what's the time"], "⏰"),
        W("Es la una", "It's one o'clock", ["it is one o'clock", "it's one"], "🕐"),
        W("Son las dos", "It's two o'clock", ["it is two o'clock", "it's two"], "🕑"),
        W("y media", "Half past", ["and a half"], "🕧"),
        W("por la mañana", "In the morning", [], "🌄"),
        W("por la noche", "At night", ["in the evening"], "🌙"),
      ]),
    ]),
    ("es-serestar", "Ser & Estar", "Two verbs for 'to be': ser for what you are, estar for how or where you are.", [
      ("es-se-l1", "Ser: who and what", [
        W("Soy alto", "I'm tall", ["i am tall"], "📏"),
        W("Soy inglés", "I'm English", ["i am english"], "🇬🇧"),
        W("Es mi hermana", "She's my sister", ["she is my sister", "this is my sister"], "👧"),
        W("Es muy simpático", "He's very nice", ["he is very nice", "he's very friendly"], "😊"),
        W("Somos una familia", "We are a family", ["we're a family"], "👨‍👩‍👧"),
      ]),
      ("es-se-l2", "Estar: how and where", [
        W("Estoy bien", "I'm fine", ["i am fine", "i'm well", "i am well"], "👍"),
        W("Estoy en casa", "I'm at home", ["i am at home"], "🏡"),
        W("¿Dónde estás?", "Where are you?", [], "🗺️"),
        W("Está aquí", "It's here", ["he's here", "she's here", "it is here"], "📍"),
        W("La sopa está fría", "The soup is cold", [], "🥣"),
      ]),
    ]),
    ("es-compare", "Comparisons", "More than, less than, and the best.", [
      ("es-cmp-l1", "More, less, most", [
        W("más grande", "Bigger", ["larger"], "🐘"),
        W("más pequeño", "Smaller", [], "🐭"),
        W("mejor", "Better", ["best"], "👍"),
        W("peor", "Worse", ["worst"], "👎"),
        W("el más rápido", "The fastest", ["fastest"], "🏃"),
        W("tan alto como", "As tall as", [], "📐"),
      ]),
    ]),
    ("es-restaurant", "At the Restaurant", "Order tapas, ask for the menu and pay the bill.", [
      ("es-res-l1", "Ordering food", [
        W("la carta", "The menu", ["menu"], "📜"),
        W("Para mí, una tortilla", "A Spanish omelette for me", ["i'll have a spanish omelette", "for me a spanish omelette"], "🍳"),
        W("¿Qué quieres beber?", "What would you like to drink?", ["what do you want to drink"], "🥤"),
        W("sin cebolla", "Without onion", ["no onion"], "🧅"),
        W("¡Está buenísimo!", "It's delicious!", ["it is delicious", "it's really good"], "😋"),
        W("La cuenta, por favor", "The bill, please", ["the check please", "bill please"], "🧾"),
      ]),
    ]),
    ("es-plans", "Making Plans", "Arranging to meet up — the most useful conversation of all.", [
      ("es-pln-l1", "Are you free?", [
        W("¿Estás libre el sábado?", "Are you free on Saturday?", ["are you free saturday"], "📅"),
        W("¿Quedamos?", "Shall we meet up?", ["shall we meet", "do you want to meet"], "🤝"),
        W("¿A qué hora?", "What time?", ["at what time"], "⏰"),
        W("Vale", "OK", ["okay", "alright", "all right"], "👌", note="You'll hear vale all day long in Spain."),
        W("Lo siento, no puedo", "Sorry, I can't", ["sorry i cannot"], "🙅"),
        W("¡Nos vemos!", "See you!", ["see you then", "see you soon"], "👋"),
      ]),
    ]),
  ]),
  ("Intermediate", [
    ("es-connectors", "Connectors", "And, but, because, if — the words that join ideas together.", [
      ("es-con-l1", "Joining ideas", [
        W("y", "And", [], "➕"),
        W("pero", "But", [], "↔️"),
        W("porque", "Because", [], "💡"),
        W("si", "If", [], "❔", note="No accent: si = if. With an accent: sí = yes."),
        W("o", "Or", [], "🔀"),
        W("también", "Also", ["too", "as well"], "➕"),
      ]),
    ]),
    ("es-directions2", "Giving Directions", "Full sentences for getting someone from A to B.", [
      ("es-dir2-l1", "Turn here", [
        W("Gira a la izquierda", "Turn left", ["turn to the left"], "⬅️"),
        W("Sigue todo recto", "Go straight on", ["keep going straight", "go straight ahead"], "⬆️"),
        W("Cruza la calle", "Cross the street", ["cross the road"], "🚸"),
        W("Está al lado del banco", "It's next to the bank", ["it is next to the bank"], "🏦"),
        W("la segunda calle", "The second street", ["the second road", "second street"], "2️⃣"),
        W("Está a cinco minutos", "It's five minutes away", ["it is five minutes away"], "⏱️"),
      ]),
    ]),
    ("es-people-desc", "Describing People", "Height, hair and character — words change for boys and girls.", [
      ("es-pd-l1", "Appearance", [
        W("alto", "Tall", [], "🦒"),
        W("bajo", "Short", [], "🐁"),
        W("delgado", "Thin", ["slim"], "🧍"),
        W("el pelo rubio", "Blond hair", ["fair hair", "blonde hair"], "👱"),
        W("los ojos azules", "Blue eyes", [], "👀"),
        W("la barba", "Beard", ["a beard"], "🧔"),
      ]),
      ("es-pd-l2", "Character", [
        W("simpático", "Nice", ["friendly", "kind"], "😊"),
        W("tímido", "Shy", [], "🙈"),
        W("divertido", "Fun", ["funny"], "😂"),
        W("trabajador", "Hard-working", ["hardworking", "hard working"], "💪"),
        W("perezoso", "Lazy", [], "🦥"),
        W("generoso", "Generous", [], "🎁"),
      ]),
    ]),
    ("es-work", "Work & Occupations", "What do you do? — jobs and talking about work.", [
      ("es-work-l1", "Occupations", [
        W("el profesor", "Teacher", ["the teacher"], "👨‍🏫"),
        W("la enfermera", "Nurse", ["the nurse"], "👩‍⚕️"),
        W("el policía", "Police officer", ["policeman", "the police officer"], "👮"),
        W("el cocinero", "Chef", ["cook", "the chef"], "👨‍🍳"),
        W("el bombero", "Firefighter", ["fireman", "the firefighter"], "👨‍🚒"),
        W("el granjero", "Farmer", ["the farmer"], "👨‍🌾"),
      ]),
      ("es-work-l2", "The world of work", [
        W("¿En qué trabajas?", "What do you do?", ["what is your job", "what's your job"], "💼"),
        W("la oficina", "Office", ["the office"], "🏢"),
        W("el jefe", "Boss", ["the boss"], "👔"),
        W("la reunión", "Meeting", ["the meeting"], "🗓️"),
        W("el sueldo", "Salary", ["wages", "pay"], "💶"),
        W("las vacaciones", "Holidays", ["holiday", "vacation"], "🏝️"),
      ]),
    ]),
    ("es-dialogues", "Short Conversations", "Real back-and-forth exchanges, not just single words.", [
      ("es-dlg-l1", "At a café", [
        W("¿Qué te pongo?", "What can I get you?", ["what would you like"], "☕"),
        W("Un café con leche, por favor", "A white coffee, please", ["a coffee with milk please"], "🥛"),
        W("¿Algo más?", "Anything else?", [], "➕"),
        W("Nada más, gracias", "Nothing else, thanks", ["that's all thanks", "nothing more thank you"], "🙏"),
      ]),
      ("es-dlg-l2", "Asking for help", [
        W("¿Me puedes ayudar?", "Can you help me?", ["could you help me"], "🆘"),
        W("Claro", "Of course", ["sure", "certainly"], "👍"),
        W("Estoy perdido", "I'm lost", ["i am lost"], "🗺️"),
        W("¿Hablas inglés?", "Do you speak English?", [], "🇬🇧"),
      ]),
    ]),
    ("es-emergency", "Health & Emergencies", "The phrases you hope you'll never need — but should know anyway.", [
      ("es-emg-l1", "Getting help fast", [
        W("¡Socorro!", "Help!", [], "🆘"),
        W("Llama a una ambulancia", "Call an ambulance", [], "🚑"),
        W("Es una emergencia", "It's an emergency", ["it is an emergency"], "🚨"),
        W("He perdido mi pasaporte", "I've lost my passport", ["i have lost my passport", "i lost my passport"], "🛂"),
        W("Soy alérgico a los frutos secos", "I'm allergic to nuts", ["i am allergic to nuts"], "🥜"),
        W("¿Dónde está el hospital?", "Where is the hospital?", ["where's the hospital"], "🏥"),
      ]),
    ]),
  ]),
  ("Upper-Intermediate", [
    ("es-opinions", "Opinions & Agreement", "Saying what you think, and whether you agree.", [
      ("es-opn-l1", "What do you think?", [
        W("Creo que sí", "I think so", [], "👍"),
        W("Creo que no", "I don't think so", ["i do not think so"], "👎"),
        W("Estoy de acuerdo", "I agree", [], "🤝"),
        W("No estoy de acuerdo", "I disagree", ["i don't agree", "i do not agree"], "🙅"),
        W("En mi opinión", "In my opinion", [], "💭"),
        W("Depende", "It depends", ["that depends"], "⚖️"),
      ]),
    ]),
    ("es-past", "Talking About the Past", "The past tense for things that happened and finished: fui, comí, hablé.", [
      ("es-pst-l1", "What did you do?", [
        W("Ayer fui a la playa", "Yesterday I went to the beach", ["i went to the beach yesterday"], "🏖️"),
        W("Comí paella", "I ate paella", ["i had paella"], "🥘"),
        W("Hablé con mi abuela", "I talked to my grandma", ["i spoke to my grandmother", "i talked to my grandmother"], "📞"),
        W("Vimos una película", "We watched a film", ["we saw a film", "we watched a movie"], "🎬"),
        W("¿Qué hiciste?", "What did you do?", [], "❓"),
        W("Fue muy divertido", "It was really fun", ["it was a lot of fun", "it was very fun"], "🎉"),
      ]),
    ]),
    ("es-storytelling", "Telling a Story", "The linking words that turn events into a story.", [
      ("es-str-l1", "Once upon a time", [
        W("Había una vez", "Once upon a time", [], "📖"),
        W("Primero", "First", ["first of all", "firstly"], "1️⃣"),
        W("Luego", "Then", ["next", "later"], "➡️"),
        W("De repente", "Suddenly", ["all of a sudden"], "⚡"),
        W("Al final", "In the end", ["finally", "at the end"], "🏁"),
        W("Y vivieron felices", "And they lived happily ever after", ["they lived happily ever after"], "🏰"),
      ]),
    ]),
    ("es-register", "Tú & Usted", "Friendly tú for family and friends, polite usted for strangers and older people.", [
      ("es-reg-l1", "Polite or friendly?", [
        W("señor", "Mr", ["sir", "mister"], "🎩"),
        W("señora", "Mrs", ["madam", "ma'am"], "👒"),
        W("usted", "You (polite)", ["you formal", "you"], "🤵"),
        W("tú", "You (friendly)", ["you informal", "you"], "🙂"),
        W("¿Cómo está usted?", "How are you? (polite)", ["how are you formal"], "🎩"),
        W("Encantado de conocerle", "Pleased to meet you", ["nice to meet you"], "🤝"),
      ]),
    ]),
    ("es-phone", "Phone Conversations", "Talking on the phone has its own set phrases.", [
      ("es-phn-l1", "On the line", [
        W("¿Diga?", "Hello? (on the phone)", ["hello on the phone"], "📞", note="Spaniards answer the phone with ¿Diga? or ¿Sí?"),
        W("¿De parte de quién?", "Who's calling?", ["who is calling", "who's speaking"], "☎️"),
        W("Un momento, por favor", "One moment, please", ["just a moment please", "hold on please"], "⏳"),
        W("Te llamo luego", "I'll call you later", ["i will call you later"], "📱"),
        W("Se ha cortado", "We got cut off", ["the line went dead", "it cut off"], "📵"),
        W("¿Me oyes?", "Can you hear me?", [], "👂"),
      ]),
    ]),
    ("es-idioms", "Idioms & Expressions", "Phrases that don't translate word for word, but every Spaniard knows.", [
      ("es-idm-l1", "How Spanish really talks", [
        W("estar en las nubes", "To daydream", ["to have your head in the clouds", "to be in the clouds"], "☁️"),
        W("ser pan comido", "To be a piece of cake", ["to be easy", "easy peasy"], "🍰"),
        W("tomar el pelo", "To pull someone's leg", ["to tease", "to wind someone up"], "😜"),
        W("costar un ojo de la cara", "To cost an arm and a leg", ["to be very expensive"], "💸"),
        W("estar como una cabra", "To be bonkers", ["to be crazy", "to be mad", "to be nuts"], "🐐"),
      ]),
    ]),
  ]),
  ("Advanced", [
    ("es-business", "Business Spanish", "Vocabulary for the office and the meeting room.", [
      ("es-biz-l1", "At the office", [
        W("la empresa", "Company", ["business", "firm", "the company"], "🏭"),
        W("el cliente", "Client", ["customer", "the client"], "🤝"),
        W("el contrato", "Contract", ["the contract"], "📝"),
        W("el presupuesto", "Budget", ["quote", "estimate"], "📊"),
        W("la factura", "Invoice", ["bill", "the invoice"], "🧾"),
        W("las ventas", "Sales", ["the sales"], "📈"),
      ]),
    ]),
    ("es-news", "News & Society", "The words behind newspapers and the evening news.", [
      ("es-news-l1", "Reading the news", [
        W("las noticias", "The news", ["news"], "📰"),
        W("el gobierno", "Government", ["the government"], "🏛️"),
        W("las elecciones", "Elections", ["the elections"], "🗳️"),
        W("la economía", "Economy", ["the economy"], "💹"),
        W("el medio ambiente", "Environment", ["the environment"], "🌍"),
        W("la sociedad", "Society", [], "👥"),
      ]),
    ]),
    ("es-future", "Future & 'Would'", "Will, would and 'if I were…' — where Spanish verbs get interesting.", [
      ("es-fut-l1", "What will happen?", [
        W("Mañana iré al cine", "Tomorrow I'll go to the cinema", ["i will go to the cinema tomorrow", "tomorrow i will go to the cinema"], "🍿"),
        W("Lloverá", "It will rain", ["it'll rain"], "☔"),
        W("Será fácil", "It will be easy", ["it'll be easy"], "✅"),
        W("Me gustaría viajar", "I would like to travel", ["i'd like to travel"], "🧭"),
        W("¿Podrías ayudarme?", "Could you help me?", [], "🙏"),
        W("Si fuera rico, compraría un barco", "If I were rich, I would buy a boat", ["if i was rich i would buy a boat", "if i were rich i'd buy a boat"], "⛵"),
      ]),
    ]),
    ("es-proverbs", "Proverbs & Sayings", "Refranes — sayings every Spaniard grows up with.", [
      ("es-prv-l1", "Common sayings", [
        W("Más vale tarde que nunca", "Better late than never", [], "⏰"),
        W("A quien madruga, Dios le ayuda", "The early bird catches the worm", ["early bird gets the worm"], "🐦"),
        W("En boca cerrada no entran moscas", "Silence is golden", ["keep your mouth shut"], "🤐"),
        W("Poco a poco se va lejos", "Slowly but surely", ["little by little you go far", "slow and steady"], "🐢"),
        W("Dime con quién andas y te diré quién eres", "You are the company you keep", ["a man is known by the company he keeps"], "👫"),
      ]),
    ]),
    ("es-debate", "Discussion & Debate", "Weighing up pros and cons like a native speaker.", [
      ("es-dbt-l1", "Weighing it up", [
        W("Por un lado", "On the one hand", [], "☝️"),
        W("Por otro lado", "On the other hand", [], "✋"),
        W("Sin embargo", "However", ["nevertheless"], "🔄"),
        W("Además", "Moreover", ["furthermore", "what's more", "besides"], "➕"),
        W("las ventajas", "The advantages", ["advantages", "pros"], "✅"),
        W("las desventajas", "The disadvantages", ["disadvantages", "cons"], "❌"),
      ]),
    ]),
  ]),
  ("Fluency & Mastery", [
    ("es-slang", "Slang & Casual Speech", "The words you won't find in a textbook, but hear everywhere in Spain.", [
      ("es-slg-l1", "Sounding natural", [
        W("¡Qué guay!", "How cool!", ["cool", "that's cool"], "😎"),
        W("¡Tío!", "Mate!", ["dude", "buddy", "mate"], "🤙", note="Friends call each other tío or tía — not just uncles and aunts!"),
        W("Mola mucho", "It's really cool", ["it rocks", "it's great"], "🤘"),
        W("¡Qué rollo!", "What a drag!", ["how boring", "what a pain"], "🙄"),
        W("Estoy flipando", "I can't believe it", ["i'm amazed", "i am amazed", "i'm shocked"], "🤯"),
        W("Me da igual", "I don't mind", ["i don't care", "whatever"], "🤷"),
      ]),
    ]),
    ("es-reactions", "Humour & Reactions", "The little exclamations real conversations run on.", [
      ("es-rxn-l1", "Reacting naturally", [
        W("¡Venga!", "Come on!", ["come on"], "💪"),
        W("¡Ojalá!", "I hope so!", ["hopefully", "if only"], "🤞"),
        W("¡Qué pena!", "What a shame!", ["what a pity"], "😞"),
        W("¡No me digas!", "No way!", ["you don't say", "really"], "😮"),
        W("¡Madre mía!", "Oh my goodness!", ["oh my god", "wow", "goodness me"], "😱"),
      ]),
    ]),
    ("es-reading", "Reading a Short Paragraph", "Four connected sentences — read them as a whole story.", [
      ("es-rdg-l1", "Lucía's week", [
        W("Me llamo Lucía y vivo en Sevilla.", "My name is Lucía and I live in Seville.", ["my name is lucia and i live in seville"], "🙋‍♀️"),
        W("Todas las mañanas voy al colegio en bici.", "Every morning I go to school by bike.", ["every morning i cycle to school"], "🚲"),
        W("Por la tarde juego con mi perro en el parque.", "In the afternoon I play with my dog in the park.", [], "🐕"),
        W("Los domingos comemos paella con mis abuelos.", "On Sundays we eat paella with my grandparents.", ["on sundays we have paella with my grandparents"], "🥘"),
      ]),
    ]),
    ("es-casual-greet", "Casual Greetings", "What people actually say when they bump into a friend.", [
      ("es-cgr-l1", "Hey, what's up?", [
        W("¿Qué pasa?", "What's up?", ["what's happening", "what is up"], "🤙"),
        W("¿Cómo va?", "How's it going?", ["how is it going"], "🙂"),
        W("¡Cuánto tiempo!", "Long time no see!", ["it's been ages", "long time no see"], "🤗"),
        W("Buenas", "Hi there", ["hiya", "hey"], "👋"),
        W("¡Hasta mañana!", "See you tomorrow!", ["see you tomorrow"], "🌙"),
      ]),
    ]),
    ("es-professional", "Formal Spanish", "The language of letters, emails and official occasions.", [
      ("es-prof-l1", "Writing formally", [
        W("Estimado señor", "Dear Sir", [], "✉️"),
        W("Le saluda atentamente", "Yours sincerely", ["yours faithfully"], "🖋️"),
        W("Le agradezco su ayuda", "Thank you for your help (formal)", ["i appreciate your help", "thank you for your help"], "🙏"),
        W("Quedo a su disposición", "I remain at your disposal", ["i am at your service"], "🤝"),
        W("Un cordial saludo", "Kind regards", ["best regards", "warm regards"], "📧"),
      ]),
    ]),
    ("es-literary", "Songs & Poetry", "The poetic words behind Spanish songs, films and poems.", [
      ("es-lit-l1", "Words from songs and poems", [
        W("el alma", "Soul", ["the soul"], "🕊️"),
        W("la luna", "Moon", ["the moon"], "🌙"),
        W("soñar", "To dream", ["dream"], "💭"),
        W("el mar", "Sea", ["the sea"], "🌊"),
        W("para siempre", "Forever", ["for ever", "always"], "♾️"),
      ]),
    ]),
  ]),
]


def build():
    levels, seen_ids, seen_text = [], set(), {}
    for level_name, units in COURSE:
        level = {"level": level_name, "units": []}
        for unit_id, title, tagline, lessons in units:
            unit = {"id": unit_id, "title": title, "tagline": tagline, "lessons": []}
            for lesson_id, lesson_title, words in lessons:
                lesson = {"id": lesson_id, "title": lesson_title, "words": []}
                ens = set()
                for i, (text, en, accept, emoji, extra) in enumerate(words):
                    wid = f"{lesson_id}-{i}"
                    assert wid not in seen_ids, wid
                    assert en.lower() not in ens, f"duplicate English in {lesson_id}: {en}"
                    if text.lower() in seen_text:
                        raise SystemExit(f"duplicate Spanish '{text}' in {wid} and {seen_text[text.lower()]}")
                    seen_ids.add(wid); ens.add(en.lower()); seen_text[text.lower()] = wid
                    w = {"id": wid, "text": text, "en": en}
                    if accept:
                        w["accept"] = [a.lower() for a in accept if a.lower() != en.lower()]
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
    print(f"{OUT}: {len(levels)} levels, {len(units)} units, {len(lessons)} lessons, {len(words)} words, "
          f"{sum(len(w['text']) for w in words)} characters of Spanish")
