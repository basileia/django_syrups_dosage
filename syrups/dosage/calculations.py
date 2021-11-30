from decouple import config
from pymongo import MongoClient
from sys import maxsize


def get_connection():
    return MongoClient(
        config('MONGODB_URI')
    )


def get_db_connection():
    connection = get_connection()
    db = connection.sirups_information
    return db.sirups


def age_to_months(age):
    """
    Converts age from years to months
    """
    return age * 12


def dict_keys_to_list(syrup, key_type):
    """
    Converts dict keys to int list
    """
    keysList = list(syrup[key_type].keys())
    for i in range(len(keysList)):
        keysList[i] = keysList[i].split(" - ")
        for j in range(len(keysList[i])):
            keysList[i][j] = int(keysList[i][j])
    return keysList


def get_range(keysList, value):
    """
    Get range of age or weight acoording to value
    """
    for i in range(len(keysList)):
        if keysList[i][0] <= value < keysList[i][1]:
            return keysList[i]


def int_list_to_string(numbers):
    """
    Converts int list to string
    """
    string_ints = [str(int) for int in numbers]
    return " - ".join(string_ints)


def calculate_dosage(syrup, age_weight, range_string, weight, min_or_max):
    return round(
        (syrup[age_weight][range_string][min_or_max] * weight) / syrup["Strength"], 2
    )


def dosage_range_by_age_and_weight(age, weight, syrup_name):
    """
    Acoording to age and weight returns min and max dosage or messages.
    Output is a list.
    """
    dosage = {}

    syrups = get_db_connection()
    if syrup_name == "AMOKSIKLAV":
        syrup_name = "AMOKSIKLAV 457 MG/5 ML"
    elif syrup_name == "ZINNAT":
        syrup_name = "ZINNAT 125MG POR GRA SUS 50ML"
    elif syrup_name == "AMOKSIKLAV_FORTE":
        syrup_name = "AMOKSIKLAV_FORTE 312,5 MG/5 ML"
    elif syrup_name == "AUGMENTIN":
        syrup_name = "AUGMENTIN 400 MG/5 ML + 57 MG/5 ML"
    elif syrup_name == "CEFZIL":
        syrup_name = "CEFZIL O.S. 250 MG"
    elif syrup_name == "FROMILID":
        syrup_name = "FROMILID 125 MG/5 ML"
    elif syrup_name == "SUMETROLIM":
        syrup_name = "SUMETROLIM 40 MG/ML + 8 MG/ML SIRUP"
    elif syrup_name == "KLACID_125":
        syrup_name = "KLACID_125 MG/5 ML"
    elif syrup_name == "KLACID_250":
        syrup_name = "KLACID_250 MG/5 ML"

    syrup = syrups.find_one({"Name":  syrup_name})  # months, kg

    max_age = 216
    if age > max_age:
        dosage["Message"] = "Zvolte lékovou formu pro dospělé"
        return [dosage["Message"]]

    age_values = dict_keys_to_list(syrup, "Age")
    age_range_ints = get_range(age_values, age)
    age_range_string = int_list_to_string(age_range_ints)

    result = []
    result.append("Dávkování pro sirup " + syrup_name.replace("_", " "))
    try:
        result.append(syrup["Poznámka"])
    except(KeyError):
        pass
    result.append("Dávkování: " + syrup["Units"])
    try:
        max_weight = "".join(syrup["Weight"].keys())
    except(KeyError):
        max_weight = maxsize

    if weight > int(max_weight):
        if len(syrup["Weight"][max_weight]) > 3:
            dosage["Message"] = syrup["Weight"][max_weight]
            return [dosage["Message"]]
        else:
            possible_keys = "".join(syrup["Weight"][max_weight].keys())
            if "Min" in possible_keys:
                dosage["Min"] = syrup["Weight"][max_weight]["Min"] / syrup["Strength"]
                result.append("Minimální dávka: " + str(dosage["Min"]) + " ml")
            if "Max" in possible_keys:
                dosage["Max"] = syrup["Weight"][max_weight]["Max"] / syrup["Strength"]
                result.append("Maximální dávka: " + str(dosage["Max"]) + " ml")
    else:
        if len((syrup["Age"][age_range_string])) > 3:
            dosage["Message"] = syrup["Age"][age_range_string]
            return [dosage["Message"]]
        possible_keys = "".join(syrup["Age"][age_range_string].keys())
        if "Min" in possible_keys:
            dosage["Min"] = calculate_dosage(syrup, "Age", age_range_string, weight, "Min")
            result.append("Minimální dávka: " + str(dosage["Min"]) + " ml")
        if "Max" in possible_keys:
            dosage["Max"] = calculate_dosage(syrup, "Age", age_range_string, weight, "Max")
            result.append("Maximální dávka: " + str(dosage["Max"]) + " ml")

    if "Max dosage" in syrup:
        dosage["Max dosage"] = syrup["Max dosage"] / syrup["Strength"]
        result.append("Maximální dávka nesmí překročit: " + str(dosage["Max dosage"]) + " ml")
    return result


def dosage_erdomed(weight, age):
    """
    Returns the correct dose for the child according to the entered weight
    and age.
    Output is a list.
    """
    syrups = get_db_connection()
    syrup = syrups.find_one({"Name": "ERDOMED 35MG/ML POR PLV SUS"})

    if age > int(list(syrup["Age"].keys())[0]):
        return syrup["Age"]["216"]
    weight_values = dict_keys_to_list(syrup, "Weight")
    weight_range_ints = get_range(weight_values, weight)
    weight_range_string = int_list_to_string(weight_range_ints)
    return ["Doporučené dávkování: " + syrup["Weight"][weight_range_string]]


def dosage_ospen(weight, age, syrup_name):
    """
    Returns the correct dose for the child according to the entered weight
    and age.
    Output is a list.
    """
    dosage = {}

    syrups = get_db_connection()
    if syrup_name == "OSPEN_0,75":
        syrup_name = "OSPEN_0,75 MIU/5 ML"
    elif syrup_name == "OSPEN_0,4":
        syrup_name = "OSPEN_0,4 MIU/5 ML"

    syrup = syrups.find_one({"Name":  syrup_name})
    age_values = dict_keys_to_list(syrup, "Age")
    age_range_ints = get_range(age_values, age)
    age_range_string = int_list_to_string(age_range_ints)

    if age > 216:
        return ["Kontrola dávkování pouze pro pediatrickou populaci."]

    result = []
    result.append("Obvyklé dávkování pro pediatrickou populaci pro sirup " + syrup_name.replace("_", " "))
    result.append("Dávkování: " + syrup["Units"])

    if len((syrup["Age"][age_range_string])) > 10:
        result.append(syrup["Age"][age_range_string])
        return result
    possible_keys = "".join(syrup["Age"][age_range_string].keys())

    if "Co 6 hodin" in possible_keys:
        dosage["Co 6 hodin"] = calculate_dosage(syrup, "Age", age_range_string, weight, "Co 6 hodin")
        result.append("Co 6 hodin: " + str(dosage["Co 6 hodin"]) + " ml")
    if "Co 8 hodin" in possible_keys:
        dosage["Co 8 hodin"] = calculate_dosage(syrup, "Age", age_range_string, weight, "Co 8 hodin")
        result.append("Co 8 hodin: " + str(dosage["Co 8 hodin"]) + " ml")
    if "Max dosage" in syrup:
        dosage["Max dosage"] = syrup["Max dosage"] / syrup["Strength"]
        result.append("Maximální dávka nesmí překročit: " + str(dosage["Max dosage"]) + " ml")
    return result


def dosage_ospamox(weight):
    """
    Returns the correct dose for the child according to the entered weight
    and age.
    Output is a list.
    """
    result = []
    dosage = {}
    syrup_name = "OSPAMOX 250 MG/5 ML"
    result.append("Dávkování pro sirup " + syrup_name)

    syrups = get_db_connection()
    syrup = syrups.find_one({"Name":  syrup_name})
    result.append("Dávkování: " + syrup["Units"])
    weight_values = dict_keys_to_list(syrup, "Weight")
    weight_range_ints = get_range(weight_values, weight)
    weight_range_string = int_list_to_string(weight_range_ints)

    possible_keys = "".join(syrup["Weight"][weight_range_string].keys())
    if "Min" in possible_keys:
        dosage["Min"] = calculate_dosage(syrup, "Weight", weight_range_string, weight, "Min")
        result.append("Minimální dávka: " + str(dosage["Min"]) + " ml")
    if "Max" in possible_keys:
        dosage["Max"] = calculate_dosage(syrup, "Weight", weight_range_string, weight, "Max")
        result.append("Maximální dávka: " + str(dosage["Max"]) + " ml")

    if "Max dosage" in syrup:
        dosage["Max dosage"] = syrup["Max dosage"] / syrup["Strength"]
        result.append("Maximální dávka nesmí překročit: " + str(dosage["Max dosage"]) + " ml")
    return result


def dosage_sumamed(weight, syrup_name):
    """
    Returns the correct dose for the child according to the entered weight
    and age.
    Output is a list.
    """
    result = []
    if syrup_name == "SUMAMED":
        syrup_name = "SUMAMED 20 MG/ML"
    elif syrup_name == "SUMAMED_FORTE":
        syrup_name = "SUMAMED_FORTE 40 MG/ML"

    syrups = get_db_connection()
    syrup = syrups.find_one({"Name":  syrup_name})
    result.append("Dávkování pro sirup " + syrup_name.replace("_", " "))
    result.append("Dávkování: " + syrup["Units"])
    dosage = round((syrup["Max"] * weight) / syrup["Strength"], 2)
    result.append("Maximální dávka: " + str(dosage) + " ml")
    return result
