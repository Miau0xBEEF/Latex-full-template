import re

ACRONYM_FILE = "acronym.tex"

# Function to read the existing acronyms from the file
def read_acronyms():
    with open(ACRONYM_FILE, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    acronym_entries = []
    glossary_entries = {}
    for line in lines:
        acronym_match = re.match(r"\\newacronym{([^}]+)}{([^}]+)}{([^}]+)}", line)
        glossary_match = re.match(r"\\newglossaryentry{([^}]+)}{name={(.*?)}, description={(.*?)}", line)
        
        if acronym_match:
            acronym_entries.append((acronym_match.group(1), acronym_match.group(2), acronym_match.group(3)))
        elif glossary_match:
            glossary_entries[glossary_match.group(1)] = (glossary_match.group(2), glossary_match.group(3))
    
    return acronym_entries, glossary_entries

# Function to insert a new acronym and glossary entry while keeping alphabetical order
def insert_acronym(acronyms, glossary_entries, new_acronym, glossary_name=None, glossary_desc=None):
    key, short, desc = new_acronym
    glossary_key = f"glos:{key}"
    
    if key in [a[0] for a in acronyms]:
        print(f"{key} already exists.")
        return acronyms, glossary_entries
    
    # Append glossary reference if a glossary entry is created
    if glossary_name and glossary_desc:
        desc = f"{desc} \\protect\\glsadd{{{glossary_key}}}"
        glossary_entries[glossary_key] = (glossary_name, glossary_desc)
    
    acronyms.append((key, short, desc))
    acronyms.sort(key=lambda x: x[0].lower())
    
    return acronyms, glossary_entries

# Function to write sorted acronyms and glossary entries back to the file
def write_acronyms(acronyms, glossary_entries):
    with open(ACRONYM_FILE, "w", encoding="utf-8") as file:
        for acronym in acronyms:
            file.write(f"\\newacronym{{{acronym[0]}}}{{{acronym[1]}}}{{{acronym[2]}}}\n")
            if f"glos:{acronym[0]}" in glossary_entries:
                g_name, g_desc = glossary_entries[f"glos:{acronym[0]}"]
                file.write(f"\\newglossaryentry{{glos:{acronym[0]}}}{{name={{{g_name}}}, description={{{g_desc}}}}}\n")

# Function to interactively add a new acronym
def add_acronym():
    acronyms, glossary_entries = read_acronyms()
    
    while True:
        key = input("Enter first argument (or type 'exit' to quit): ")
        if key.lower() == 'exit':
            break
        
        if key in [a[0] for a in acronyms]:
            print(f"{key} already exists.")
            continue
        
        short = input("Enter second argument: ")
        desc = input("Enter description: ")
        
        glossary_decision = input("Create glossary entry? (Press Enter to skip, type anything to confirm): ")
        glossary_name = glossary_desc = None
        if glossary_decision.strip():
            glossary_name = desc
            glossary_desc = input("Enter glossary description: ")
            
        acronyms, glossary_entries = insert_acronym(acronyms, glossary_entries, (key, short, desc), glossary_name, glossary_desc)
        write_acronyms(acronyms, glossary_entries)
        
        print(f"Acronym {key} added successfully!\n")

if __name__ == "__main__":
    add_acronym()
