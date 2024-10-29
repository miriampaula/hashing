import random
import itertools
import pandas as pd

# Seturi extinse de nume pentru generare (200 fiecare)
nume_familie = [ "Popescu", "Ionescu", "Marin", "Dumitrescu", "Stan", "Stoica", "Gheorghe", "Popa", "Radu", "Munteanu",
    "Constantinescu", "Tudor", "Iliescu", "Dobre", "Barbu", "Nistor", "Sandu", "Dragomir", "Vasilescu", "Petrescu",
    "Nicolescu", "Manole", "Vasile", "Serban", "Mihai", "Avram", "Luca", "Dima", "Florea", "Toma", "Moldovan", 
    "Anghel", "Andrei", "Ciobanu", "Stefan", "Carp", "Grigore", "Cristea", "Nicolae", "Mircea", "Voicu", "Roman",
    "Matei", "Preda", "Iancu", "Oprea", "Diaconu", "Petre", "Mihail", "Olaru", "Sorescu", "Filip", "Alexandru",
    "Costache", "Radulescu", "Lupu", "Vlad", "Pascu", "Pana", "Dan", "Sava", "Cojocaru", "Neagu", "Moise", "Rusu",
    "Pop", "Damian", "Popovici", "Sima", "Lazar", "Dinu", "Tudose", "Dragan", "Gavrila", "Albu", "Ianculescu", 
    "Nistor", "Cornea", "Ioniță", "Cretu", "Bratu", "Visan", "Paraschiv", "Neculai", "Loghin", "Pasca", "Socol", 
    "Voinea", "Panait", "Tufis", "Craciun", "Nedelea", "Valcea", "Mihoc", "Antonescu", "Rogojan", "Oprescu", 
    "Dabija", "Bran", "Luminita", "Racovita", "Budescu", "Calinescu", "Nicoara", "Mazilu", "Curca", "Raicu", 
    "Cionca", "Veres", "Biris", "Butnaru", "Rosca", "Tarcau", "Guta", "Mateescu", "Stanescu", "Ciorba", "Mateiu", 
    "Sisu", "Boieru", "Donici", "Arbanas", "Sarbu", "Lipan", "Badea", "Toader", "Blaga", "Moldoveanu", "Petcu", 
    "Moisil", "Neculai", "Cimpoi", "Onu", "Samson", "Pintilie", "Ardelean", "Militaru", "Chelba", "Zamfir", "Stefan",
    "Spiru", "Nuta", "Boicu", "Stoleru", "Soare", "Daminescu", "Codrescu", "Crisan", "Banica", "Scutaru", "Neagu",
    "Baltaretu", "Urs", "Popeanu", "Bucur", "Macarie", "Costea", "Olteanu", "Costin", "Vornicu", "Berbecaru", 
    "Lazarescu", "Patrascu", "Purcaru", "Dobrica", "Poporaca", "Mihaila", "Voinescu", "Chiriac", "Dabija", 
    "Udrea", "Manastireanu", "Nechita", "Tita", "Visarion", "Arvinte", "Draganescu", "Vladut", "Turcanu", "Nacu", 
    "Nistor", "Ponta", "Benea", "Boboc", "Diaconu", "Popa", "Ciobanu", "Andrei", "Zorila", "Schwartz", "Manole", 
    "Vlasceanu", "Prisacariu", "Bejan", "Rusu", "Simion", "Damian", "Morar", "Serbanescu"
]

prenume_masculine = [ "Andrei", "Alexandru", "Gabriel", "Mihai", "Cristian", "Marian", "Ionut", "Radu", "Florin", "Paul", 
    "George", "Stefan", "Marius", "Constantin", "Claudiu", "Nicolae", "Dan", "Ciprian", "Vlad", "Sorin", "Victor",
    "Rares", "Razvan", "Robert", "Alin", "Valentin", "Costin", "Sergiu", "Eugen", "Emil", "Doru", "Sebastian", "Vasile",
    "Ilie", "Petru", "Bogdan", "Dacian", "Felix", "Adrian", "Gica", "Lucian", "Mugurel", "Octavian", "Emanuel", 
    "Gelu", "Alex", "Marcel", "Petrica", "Laurentiu", "Anghel", "Alexe", "Dorian", "Ion", "Alexe", "Horatiu",
    "Darius", "Stefan", "Ovidiu", "Iuliu", "Nicusor", "Tiberiu", "Ioan", "Cristi", "Luca", "Mihail", "Nicodim",
    "Danut", "Zamfir", "Iacob", "Nicodim", "Vasi", "Gabi", "Grigore", "Cornel", "Dinu", "Horia", "Cosmin", 
    "Ervin", "Sorin", "Felix", "Claudiu", "Dacian", "Miron", "Iuliu", "Vasile", "Ionel", "Robert", "Ilie", 
    "Petru", "Adrian", "Tiberiu", "Gabriel", "Radu", "Sebastian", "Costel", "Dorel", "Ovidiu", "Ciprian", 
    "Andi", "Dragan", "Petre", "Felix", "Cosmin", "Gheorghe", "Teodor", "Romeo", "Valeriu", "Aurel", "Florentin",
    "Virgil", "Tudor", "Zamfir", "Emilian", "Iulian", "Valentin", "Matei", "Narcis", "Pavel", "Dragos", "Cezar",
    "Constantin", "Stefan", "Nelu", "Calin", "Octavian", "Virgil", "Beniamin", "Dorin", "Aurelian", "Vasile", 
    "Armand", "Petronel", "Codrut", "Andi", "Cristi", "Luca", "Mihail", "Dragos", "Tudor", "Dorel", "Daniel", 
    "Mircea", "Catalin", "Dumitru", "Costica", "Sebastian", "Ion", "Valeriu", "Paul", "Lorin", "Ionel"
]

prenume_feminine = [ "Maria", "Elena", "Ioana", "Gabriela", "Mihaela", "Alina", "Andreea", "Diana", "Cristina", 
    "Roxana", "Monica", "Simona", "Ramona", "Adriana", "Daniela", "Anca", "Oana", "Valentina", "Bianca", "Loredana", 
    "Mariana", "Irina", "Nicoleta", "Luminita", "Corina", "Lucia", "Ana", "Sorina", "Violeta", "Anisoara", 
    "Paula", "Georgiana", "Florentina", "Marilena", "Camelia", "Roxana", "Silvia", "Adina", "Doina", "Nadia", 
    "Raluca", "Sabina", "Cristina", "Marcela", "Lacramioara", "Ecaterina", "Maricica", "Mihaiela", "Genoveva", 
    "Madalina", "Aura", "Sanda", "Irina", "Ionela", "Petronela", "Rodica", "Elisabeta", "Ruxandra", "Viorela",
    "Magdalena", "Eugenia", "Liliana", "Olivia", "Sorana", "Lorelei", "Teodora", "Antoaneta", "Andreea", "Sonia", 
    "Angelica", "Clara", "Veronica", "Erika", "Gabriela", "Dafina", "Claudia", "Florica", "Alma", "Letitia", 
    "Felicia", "Ileana", "Natalia", "Eliza", "Emanuela", "Marcela", "Romina", "Celina", "Marinela", "Iulia", 
    "Doinita", "Laura", "Mirela", "Luminita", "Elvira", "Rucsandra", "Sofia", "Rodica", "Dochia", "Veronica", 
    "Liana", "Aurica", "Catinca", "Dora", "Sabina", "Gabriela", "Georgeta", "Valeria", "Margareta", "Elena",
    "Virginia", "Lavinia", "Dorina", "Sanziana", "Narcisa", "Anisoara", "Marina", "Silvica", "Letitia"
]

# Parametri pentru generare
num_records = 1_000_000
female_ratio = 0.511  # 51.1%
num_females = int(num_records * female_ratio)
num_males = num_records - num_females

# Creăm liste goale pentru a aduna combinațiile generate
female_combinations = set()
male_combinations = set()

# Generare unică până la atingerea numărului dorit de înregistrări pentru femei
print("Generare nume pentru femei...")
while len(female_combinations) < num_females:
    fam = random.choice(nume_familie)
    fn, sn = random.sample(prenume_feminine, 2)  # selectăm două prenume unice
    full_name = (fam, fn, sn)
    female_combinations.add(full_name)  # `set` gestionează automat unicitățile

    # Afișează progresul la fiecare 100.000 de nume generate
    if len(female_combinations) % 100000 == 0:
        print(f"{len(female_combinations)} nume de femei generate.")

# Generare unică până la atingerea numărului dorit de înregistrări pentru bărbați
print("Generare nume pentru bărbați...")
while len(male_combinations) < num_males:
    fam = random.choice(nume_familie)
    fn, sn = random.sample(prenume_masculine, 2)  # selectăm două prenume unice
    full_name = (fam, fn, sn)
    male_combinations.add(full_name)  # `set` gestionează automat unicitățile

    # Afișează progresul la fiecare 100.000 de nume generate
    if len(male_combinations) % 100000 == 0:
        print(f"{len(male_combinations)} nume de bărbați generate.")

# Creăm DataFrame cu datele și salvăm în CSV
data_records = [("F", f"{fam} {fn} {sn}") for fam, fn, sn in female_combinations] + \
               [("M", f"{fam} {fn} {sn}") for fam, fn, sn in male_combinations]

print("Salvare în CSV...")
df = pd.DataFrame(data_records, columns=["Sex", "Full_Name"])
df.to_csv("nume_unice.csv", index=False)
print("Generarea și salvarea au fost finalizate!")