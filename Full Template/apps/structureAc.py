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
    
    return lines, acronym_entries, glossary_entries

# Function to insert a new acronym and glossary entry while keeping alphabetical order
def insert_acronym(lines, acronyms, new_acronym, glossary_entries, glossary_desc=None):
    key, short, desc = new_acronym
    existing_keys = [a[0] for a in acronyms]
    glossary_key = f"glos:{key}"
    
    if key in existing_keys:
        print(f"{key} already exists.")
        return lines
    
    # Append glossary reference if a glossary entry is created
    if glossary_desc:
        desc_with_glossary = f"{desc} \\protect\\glsadd{{{glossary_key}}}"
    else:
        desc_with_glossary = desc
    
    acronyms.append((key, short, desc_with_glossary))
    acronyms.sort(key=lambda x: x[0].lower())
    
    # Reconstruct the file with sorted acronyms
    new_lines = []
    added_acronym = False
    added_glossary = False
    
    for line in lines:
        if line.startswith("\\newacronym{") and not added_acronym:
            for acronym in acronyms:
                new_lines.append(f"\\newacronym{{{acronym[0]}}}{{{acronym[1]}}}{{{acronym[2]}}}\n")
            added_acronym = True
        elif line.startswith("\\newglossaryentry{") and not added_glossary:
            for g_key, (g_name, g_desc) in glossary_entries.items():
                new_lines.append(f"\\newglossaryentry{{{g_key}}}{{name={{{g_name}}}, description={{{g_desc}}}}}\n")
            added_glossary = True
        else:
            new_lines.append(line)
    
    # Ensure glossary entries are added if missing
    if glossary_desc and glossary_key not in glossary_entries:
        glossary_entry = f"\\newglossaryentry{{{glossary_key}}}{{name={{{desc}}}, description={{{glossary_desc}}}}}\n"
        new_lines.append(glossary_entry)
        glossary_entries[glossary_key] = (desc, glossary_desc)
    
    return new_lines

# Function to interactively add a new acronym
def add_acronym():
    lines, acronyms, glossary_entries = read_acronyms()
    
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
        glossary_desc = None
        if glossary_decision.strip():
            glossary_desc = input("Enter glossary description: ")
            
        new_lines = insert_acronym(lines, acronyms, (key, short, desc), glossary_entries, glossary_desc)
        
        with open(ACRONYM_FILE, "w", encoding="utf-8") as file:
            file.writelines(new_lines)
        
        print(f"Acronym {key} added successfully!\n")

if __name__ == "__main__":
    add_acronym()
