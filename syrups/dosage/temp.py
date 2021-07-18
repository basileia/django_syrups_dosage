from .secrets import get_db_connection


def init_sirups():

    sirups = get_db_connection()
    sirups.delete_many({})

    entries = []

    amoksiklav_forte = {
        "Name": "AMOKSIKLAV_FORTE 312,5 MG/5 ML",
        "Age": {
            "0 - 24": {"Max": 40},
            "24 - 216": {"Min": 20, "Max": 60}
        },
        "Units": "na den",
        "Weight": {"40": "Maximální dávka je 30 ml na den."},  # na den
        "Max dosage": 2400,
        "Strength": 50,
        "Strength units": "mg/ml"
    }
    entries.append(amoksiklav_forte)

    amoksiklav = {
        "Name": "AMOKSIKLAV 457 MG/5 ML",
        "Age": {
            "0 - 2": "Nelze určit doporučené dávkování.",  # months
            "2 - 24": {"Max": 45},
            "24 - 216": {"Min": 25, "Max": 70},
        },
        "Units": "na den",
        "Weight": {"40": "Zvolte lékovou formu určenou pro dospělé."},
        "Max dosage": 2800,
        "Strength": 80,
        "Strength units": "mg/ml",
    }
    entries.append(amoksiklav)

    augmentin = {
        "Name": "AUGMENTIN 400 MG/5 ML + 57 MG/5 ML",
        "Age": {
            "0 - 2": "Nelze určit doporučené dávkování.",  # months
            "2 - 24": {"Max": 45},
            "24 - 216": {"Min": 25, "Max": 70},
        },
        "Units": "na den",
        "Weight": {"40": "Zvolte lékovou formu určenou pro dospělé."},
        "Max dosage": 2800,
        "Strength": 80,
        "Strength units": "mg/ml",
    }
    entries.append(augmentin)

    cefzil = {
        "Name": "CEFZIL O.S. 250 MG",
        "Age": {
            "0 - 6": "Nelze určit doporučené dávkování.",  # months
            "6 - 144": {"Min": 7.5, "Max": 15},
            "144 - 216": "250 - 500 mg max 2x denně"
        },
        "Strength": 50,
        "Max dosage": 500,  # na dávku
        "Units": "na dávku, max 2x denně",
        "Strength units": "mg/ml"
    }
    entries.append(cefzil)

    fromilid = {
        "Name": "FROMILID 125 MG/5 ML",
        "Age": {
            "0 - 6": "Nelze určit doporučené dávkování",
            "6 - 144": {"Min": 7.5, "Max": 15},
            "144 - 216": "Použijte lékovou formu pro dospělé."
        },
        "Units": "na dávku, max 2x denně",
        "Strength": 25,
        "Strength units": "mg/ml",
        "Max dosage": 500
    }
    entries.append(fromilid)

    erdomed = {
        "Name": "ERDOMED 35MG/ML POR PLV SUS",
        "Weight": {
            "0 - 15": "Tento přípravek není vhodný",  # kg
            "15 - 21": "2,5 ml 2krát denně",
            "21 - 31": "5 ml 2krát denně",
            "31 - 300": "5 ml 3krát denně",
        },
        "Age": {"216": "8,5 ml 2-3x denně"},
    }
    entries.append(erdomed)

    sumetrolim = {
        "Name": "SUMETROLIM 40 MG/ML + 8 MG/ML SIRUP",
        "Age": {
            "0 - 1": "Nelze určit doporučené dávkování",
            "1 - 144": {"Max": 100},
            "144 - 1200": "Maximálně 2x denně 30 ml."
        },
        "Strength": 40,
        "Strength units": "mg/ml",
        "Units": "na den",
        "Max dosage": 2400,
        "Poznámka": "Přípravek vhodný od 6-ti týdnů."
    }
    entries.append(sumetrolim)

    ospen750 = {
        "Name": "OSPEN_0,75 MIU/5 ML",
        "Age": {
            "0 - 3": "Nelze určit doporučené dávkování",
            "3 - 216": {"Co 6 hodin": 0.02, "Co 8 hodin": 0.03}
        },
        "Units": "na dávku",
        "Strength": 0.15,
        "Strength units": "MIU/ml",
    }
    entries.append(ospen750)

    ospen400 = {
        "Name": "OSPEN_0,4 MIU/5 ML",
        "Age": {
            "0 - 3": "Nelze určit doporučené dávkování",
            "3 - 216": {"Co 6 hodin": 0.02, "Co 8 hodin": 0.03}
        },
        "Units": "na dávku",
        "Strength": 0.08,
        "Strength units": "MIU/ml"
    }
    entries.append(ospen400)

    klacid125 = {
        "Name": "KLACID_125 MG/5 ML",
        "Age": {
            "0 - 6": "Nelze určit doporučené dávkování",
            "6 - 145": {"Min": 7.5, "Max": 15},
            "145 - 216": "Klinické studie byly dělány u dětí do 12-ti let."
        },
        "Units": "na dávku, max 2x denně",
        "Max dosage": 500,
        "Strength": 25,
        "Strength units": "mg/ml",

    }
    entries.append(klacid125)

    klacid250 = {
        "Name": "KLACID_250 MG/5 ML",
        "Age": {
            "0 - 6": "Nelze určit doporučené dávkování",
            "6 - 145": {"Min": 7.5, "Max": 30},
            "145 - 216": "Klinické studie byly dělány u dětí do 12-ti let."
        },
        "Max dosage": 500,
        "Units": "na dávku, max 2x denně",
        "Strength": 50,
        "Strength units": "mg/,l",
    }
    entries.append(klacid250)

    ospamox = {
        "Name": "OSPAMOX 250 MG/5 ML",
        "Weight": {
            "0 - 40": {"Min": 20, "Max": 100},
            "40 - 300": {"Max": 6000}
        },
        "Units": "na den",
        "Strength": 50,
        "Strength units": "mg/ml",
    }
    entries.append(ospamox)

    sumamed = {
        "Name": "SUMAMED 20 MG/ML",
        "Max": 20,
        "Units": "na den",
        "Strength": 20,
        "Strength units": "mg/ml",
    }
    entries.append(sumamed)

    sumamed_forte = {
        "Name": "SUMAMED_FORTE 40 MG/ML",
        "Max": 20,
        "Units": "na den",
        "Strength": 40,
        "Strength units": "mg/ml"
    }
    entries.append(sumamed_forte)

    zinnat = {
        "Name": "ZINNAT 125MG POR GRA SUS 50ML",
        "Age": {
            "0 - 3": "Tento přípravek není vhodný",
            "3 - 216": {"Min": 10, "Max": 15},
        },
        "Weight": {"40": {"Min": 250, "Max": 500}},
        "Max dosage": 250,
        "Units": "na dávku pro děti do 40-ti kg, max 2x denně",
        "Strength": 25,
        "Strength units": "mg/ml",
    }
    entries.append(zinnat)

    entries = sorted(entries, key=lambda x: x["Name"])

    sirups.insert_many(entries)
