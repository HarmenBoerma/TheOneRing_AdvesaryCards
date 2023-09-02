import pandas as pd
import re

def get_txt(path:str="./data/input/advesary.txt") -> list:
    """
    Get the raw txt format into a list form per advesary.

    Args:
        path: string with path to raw advesary file.
    Returns:
        advesaries: list with advesaries.
    """
    advesaries = []
    with open(path, "r", encoding="utf-8") as raw_data:
        lines = []
        for line in raw_data:
            if not line.strip():
                advesaries.append(lines)
                lines = []
                continue
            lines.append(line.strip())
        advesaries.append(lines)

    return advesaries

def extract_info(advesary_lines: list):
    """
    Extract all the information needed from the raw advesary list and put it into a dictionary.

    Args:
         advesary_lines: list with information about a single advesary.
    Returns:
        advesary: dict with all advesaries.
    """
    advesary = {
        "name": None,
        "attribute_level": None,
        "might": None,
        "endurance": None,
        "parry": None,
        "armour": None,
        "image": None,
        "flavor_text": " ".join(advesary_lines[1:advesary_lines.index(advesary_lines[0].upper())] if len(advesary_lines) else ""),
        "distinctive_features": None,
        "fell_abilities": None,
        "weapons": None,
        "card_front": "./images/template/card_layout_front.png",
        "card_back": "./images/template/card_layout_back.png",
    }

    for index, line in enumerate(advesary_lines):
        if index == 0:
            advesary["name"] = line.strip().title()
            advesary["image"] = "./images/advesaries/{}.png".format(line.strip().lower().replace(" ", "_"))
        if advesary["name"].upper() == line.strip():
            advesary["distinctive_features"] = advesary_lines[index+1]
        if line.strip().replace(" ", "_").lower() in advesary or line.strip().replace(" ", "_").lower() in ["hate", "resolve"]:
            line_stripped = line.strip().replace(" ", "_").lower()
    
            if line_stripped in ["hate", "resolve"]:
                advesary[line_stripped] = advesary_lines[index+1]
            else:
                advesary[line_stripped] = advesary_lines[index+1]
        if "COMBAT PROFICIENCIES:" in line or "Combat Proficiencies:" in line:
            print(advesary["name"])
            print(line)
            print([i for i, s in enumerate(advesary_lines) if "FELL ABILITIES:" in s or "Fell Abilities:" in s])
            end_index = [i for i, s in enumerate(advesary_lines) if "FELL ABILITIES:" in s or "Fell Abilities:" in s][0]
            weapons = " ".join(advesary_lines[index:end_index]).replace("COMBAT PROFICIENCIES: ", "").replace("Combat Proficiencies: ", "")

            found = re.findall(r"\(([^\)]+)\)", weapons)
            split_index = []
            for i in found:
                comma_index = weapons.index(i)
                split_index.append(comma_index+len(i)+1)

            weapon_list = []
            current_index = 0
            for list_index in split_index:
                if list_index <= len(weapons):
                    weapon_list.append(weapons[current_index:list_index])
                    current_index = list_index+2

            weapon_dict_list = []
            for weapon in weapon_list:
                weapon_dict = {}
                weapon_name = re.match(r"^.*?(?=[0-9])", weapon).group(0)
                weapon_dict["name"] = weapon_name.strip()
                weapon = weapon.replace(weapon_name, "")
                weapon_dict["skill"] = weapon[0]
                weapon = weapon[2:]
                weapon = weapon.replace("(", "").replace(")", "").split(",")
                if len(weapon) > 1:
                    weapon_dict["special_damage"] = weapon[1]

                weapon_dict["damage"], weapon_dict["injury"] = weapon[0].split("/")

                weapon_dict_list.append(weapon_dict)

            advesary["weapons"] = weapon_dict_list

        if "FELL ABILITIES:" in line or "Fell Abilities:" in line:
            fell_abilities = " ".join(advesary_lines[index:]).replace("FELL ABILITIES: ", "").replace("Fell Abilities: ", "").split(".")[:-1]
            abilities = []
            name = None
            effect = []
            for ability_index, ability in enumerate(fell_abilities):
                if len(ability.split(" ")) <= 5:
                    if name is not None:
                        abilities.append({"name": name, "effect": " ".join(effect)})

                        name = ability.strip()
                        effect = []
                        continue
                    name = ability.strip()
                else:
                    effect.append(ability.strip())


                if ability_index == len(fell_abilities)-1:
                    abilities.append({"name": name, "effect": " ".join(effect)})

            advesary["fell_abilities"] = abilities
    return advesary


def split_in_front_and_back(df):
    """
        Split the front and back information and merge them together into one Pandas Dataframe.

        Args:
            df: Pandas Dataframe with all the advesary information.
        Returns:
            df_final: Pandas Dataframe in the right format to be used by NanDeck.

    """
    front_columns = ["card_front", "name", "image", "attribute_level", "flavor_text", "distinctive_features"]
    df_front = df[front_columns].rename(columns={"card_front": "card_layout"})
    df_front["position"] = "front"
    
    
    back_columns = ["card_back", "might", "endurance", "parry", "armour", "weapons", "fell_abilities", "resolve", "hate"]
    df_back = df[back_columns].rename(columns={"card_back": "card_layout"})
    df_back["position"] = "back"

    df_final = pd.concat([df_front, df_back])
    return df_final


def write_to_csv_for_nandeck(advesaries_json_list:list, name:str="advesaries") -> None:
    """
        Write all the advesary information into a csv file. Weapons and Abilities are put into a HTML table to be renderd by NanDeck.
        
        Args:
            advesaries_json_list: list with advesary in dict format
            name: name of csv file to write.
    """
    for advesary in advesaries_json_list:
        weapon_table_html = "<table><tr><th>Name</th><th>Skill</th><th>Damage</th><th>Injury</th><th>Special Dmg</th></tr>"
        for weapon in advesary["weapons"]:
            weapon_table_html += "<tr><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(weapon["name"], weapon["skill"], weapon["damage"], weapon["injury"], weapon["special_damage"] if "special_damage" in weapon else "")
        weapon_table_html += "</table>"
        advesary["weapons"] = weapon_table_html

        ability_html = "<table><tr><th>Name</th><th>Effect</th></tr>"
        for ability in advesary["fell_abilities"]:
            ability_html += "<tr><td>{}</td><td>{}</td></tr>".format(ability["name"], ability["effect"])
        ability_html += "</table>"
        advesary["fell_abilities"] = ability_html
        
    df = pd.json_normalize(advesaries_json_list)
    print(df.head())
    df_final = split_in_front_and_back(df)
    df_final.to_csv(f'./data/output/{name}.csv', encoding='utf-8', index=False, header=True)


def generate_advesary_csv():
    """
        Main function.
    """
    # Advesaries from Offical books
    advesary_path = "./data/input/advesary.txt"

    # Advesaries from Circleofnoms TOR2e Adversary Conversion PDF 
    advesary_conversion_path = "./data/input/advesary_conversion.txt"

    raw_data = get_txt(advesary_conversion_path)

    advesaries_csv = []
    for advesary in raw_data:
        extracted_info = extract_info(advesary)
        advesaries_csv.append(extracted_info)

    write_to_csv_for_nandeck(advesaries_csv, "test")


if __name__ == "__main__":
    generate_advesary_csv()