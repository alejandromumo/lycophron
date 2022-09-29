import bibtexparser
import re
import ast
import calendar
import logging
from datetime import datetime

import projects.covihost.covihost_csv as covihost_csv

def keywords_parser(record):

    """
    # keywords at the middle
    test1 = "Animals, China, Chiroptera, Coronavirus, Coronavirus Infections, Genome, Viral, MERS-CoV, MERS–related betacoronavirus, Middle East Respiratory Syndrome Coronavirus, Middle East respiratory syndrome coronavirus, Middle East respiratory syndrome coronavirus–related betacoronavirus, Phylogeny, Vespertilio superans, bat, betacoronaviruses, coronavirus, dwc-relationship: dwc-host: \{verHost: bat\} dwc-virus: \{abVirus: Bat CoV HKU4\}, dwc-host: \{sciHost: Chaerephon sp., verHost: bat\}, dwc-relationship: dwc-host: \{verHost: bat\} dwc-virus: \{abVirus: Rf1\}, dwc-relationship: dwc-host: \{verHost: bat\} dwc-virus: \{abVirus: SARSr-Rh-BatCoV Rp3\}, dwc-virus: \{abVirus: CoV\}, lineage, lineage C betacoronavirus, reservoir, sequencing, viruses"
    test2 = "Chiroptera, bats, control, coronavirus, dwc-relationship: dwc-host: \{verHost: bat\} dwc-virus: \{abVirus: Bat CoV HKU2\}, dwc-host: \{sciHost: Chaerephon sp., verHost: bat\}, dwc-relationship: dwc-host: \{verHost: bat\} dwc-virus: \{abVirus: Rf1\}, dwc-relationship: dwc-host: \{verHost: bat\} dwc-virus: \{abVirus: SARSr-Rh-BatCoV Rp3\}, dwc-virus: \{abVirus: CoV\}," #keywords at the beginning
    test3 = "dwc-relationship: dwc-host: \{verHost: guinean pig\} dwc-virus: \{sciVirus: reovirus, abVirus: ReoV\}, dwc-relationship: dwc-host: \{sciHost: Paguma larvata, verHost: palm civets\} dwc-virus: \{abVirus: SARS-CoV\}, dwc-virus: \{abVirus: SARS-CoV\}, dwc-host: \{sciHost: Chaerephon sp., verHost: bat\}, dwc-relationship: dwc-host: \{verHost: bat\} dwc-virus: \{abVirus: Rf1\}, dwc-relationship: dwc-host: \{verHost: bat\} dwc-virus: \{abVirus: SARSr-Rh-BatCoV Rp3\}, dwc-virus: \{abVirus: CoV\}," # no keywords
    #keywords at the end
    test4 = "dwc-relationship: dwc-host: \{verHost: guinean pig\} dwc-virus: \{sciVirus: coronavirus, abVirus: SARS-CoV\}, dwc-host: \{sciHost: Chaerephon sp., verHost: bat\}, dwc-relationship: dwc-host: \{verHost: bat\} dwc-virus: \{abVirus: Rf1\}, dwc-relationship: dwc-host: \{verHost: bat\} dwc-virus: \{abVirus: SARSr-Rh-BatCoV Rp3\}, dwc-virus: \{abVirus: CoV\}, Chiroptera, Vânia, Corona" 

    list_of_tests = [test1, test2, test3, test4]
    """

    result = {}

    raw_tags = record['keywords']

    keywords = []
    list_of_relationships = []

    disposable_keywords = ['{\\textless}Has Supplementary Material{\\textgreater}',
        '{\\textless}Closed Access{\\textgreater}',
        '{\\textless}Has Two Versions{\\textgreater}',
        '{\\textless}Scanned Paper{\\textgreater}',
        ]

    for each in disposable_keywords:
        raw_tags = raw_tags.replace(each + ', ', "")

    dwc_tags = ""

    pattern = re.compile('\},\s(?!(dwc)).*')

    if pattern.search(raw_tags) != None:
        dwc_tags = raw_tags[raw_tags.find("dwc-"):pattern.search(raw_tags).span()[0] + 3]
    elif raw_tags.find("dwc-") > 0:
        dwc_tags = raw_tags[raw_tags.find("dwc-"):]
    else:
        dwc_tags = raw_tags

    keywords = raw_tags.replace(dwc_tags, "").split(sep=", ")

    dwc_items = dwc_tags.split(sep="}, ")

    for dwc_item in dwc_items:
        if "dwc-relationship" in dwc_item:
            dwc_str = dwc_item

            dwc_edited_str = dwc_str.replace("dwc-relationship: ", "").replace("dwc-host:", "'subject':").replace("\\{sciHost: ", "[").replace("\\{verHost: ", "[").replace(" verHost: " , " ").replace("dwc-virus:", ", 'object': ").replace("\{sciVirus: ", "[").replace("\{abVirus: ", "[").replace(" abVirus: " , " ").replace("}", "").replace("\\", "]")
            dwc_edited_str = "{" + dwc_edited_str.replace("[", "['").replace(", ", "', '").replace("]", "']").replace(" ', ''object':", ", 'object':") + "}"

            dwc_dict = ast.literal_eval(dwc_edited_str)

            list_of_relationships.append(dwc_dict)


    common_keywords = ['biotic associations',
        'biotic interaction',
        'biotic relations',
        'CETAF-taskforce',
        'Coronaviridae',
        'corona viruses',
        'covid',
        'covid-19',
        'pathogen-host',
        'pathogens',
        'Viridae',
        'virus-host'
        ]


    for word in keywords:

        if word == '':
            keywords.remove(word)


    if len(keywords) == 1 and keywords[0] == '':
        keywords = []

    result["keywords"] = list(set(keywords + common_keywords))

    result["biotic relationships"] = {"obo:RO_0002453": list_of_relationships}

    return result


def get_publication_type(record):

    if record["ENTRYTYPE"] == "techreport":
        return "preprint"
    elif record["ENTRYTYPE"] == "incollection":
        return "section"
    elif record["ENTRYTYPE"] == "article":
        return "article"


def get_date(record):

    zenodo_date = "YYYY-MM-DD"

    year = record['year']

    if "month" in record.keys():
        month = record['month']
        month_int = list(calendar.month_name).index(month.capitalize())

        days_in_month = calendar.monthrange(int(year), month_int)[1]
        last_day = datetime(int(year), month_int, days_in_month).day
        #zenodo_date = zenodo_date.replace("YYYY", year).replace("MM", str(month_int))

    else:
        month_int = "01"
        last_day = "01"
        #zenodo_date = zenodo_date.replace("YYYY", year).replace("MM", "01")

    zenodo_date = zenodo_date.replace("DD", str(last_day)).replace("MM", str(month_int)).replace("YYYY", year)

    return zenodo_date


def get_authors(record):

    zenodo_creators = []

    list_of_authors = record["author"].split(sep=" and ")

    for author in list_of_authors:
        temp_dict = {}

        temp_dict["name"] = author

        zenodo_creators.append(temp_dict)

    return zenodo_creators


def convert_to_zenodo(filepath, resulting_filepath):

    #logging.basicConfig(filename='projects/covihost/logs/convert.log')

    with open(filepath, encoding='utf-8') as bibtex_file:
        bibtex_str = bibtex_file.read()

    parser = bibtexparser.bparser.BibTexParser(common_strings=True)

    bib_database = bibtexparser.loads(bibtex_str, parser=parser)

    list_of_records = bib_database.entries

    data_dump = []

    counter = 0

    for record in list_of_records:

        counter = counter + 1

        try:

            zenodo_record = {}

            zenodo_record["upload_type"] = "publication"
            zenodo_record["publication_type"] = get_publication_type(record)
            publication_date = get_date(record)
            zenodo_record["title"] = record["title"].replace("{", "").replace("}", "")
            zenodo_record["creators"] = get_authors(record)
            zenodo_record["description"] = record["abstract"] if "abstract" in record.keys() else "No abstract found"
            zenodo_record["access_right"] = "open"
            zenodo_record["license"] = "cc-by"
            zenodo_record["publication_date"] = get_date(record)
            zenodo_record["doi"] = record["doi"]

            zenodo_record["contributors"] = [{"name":"Plazi", "type":"DataCurator"}]
            zenodo_record["communities"] = [{"identifier":"biosyslit"}, {"identifier": "coviho"}, {"identifier": "globalbioticinteractions"}]
            #zenodo_record["communities"] = [{"identifier":"biosyslit"}]

            zenodo_record["language"] = "eng"

            keywords = keywords_parser(record)

            zenodo_record["keywords"] = keywords['keywords']

            zenodo_record["custom"] = keywords['biotic relationships']

            if zenodo_record["publication_type"] == "section":
                zenodo_record["partof_title"] = record["booktitle"]
                zenodo_record["partof_pages"] = record["pages"] if "pages" in record.keys() else ""
            else:
                zenodo_record["journal_title"] = record["journal"]
                zenodo_record["journal_volume"] = record["volume"] if "volume" in record.keys() else ""
                zenodo_record["journal_issue"] = record["number"] if "number" in record.keys() else ""
                zenodo_record["journal_pages"] = record["pages"] if "pages" in record.keys() else ""

            empty_keys = []

            for key in zenodo_record:
                if zenodo_record[key] == "":
                    empty_keys.append(key)

            for empty_key in empty_keys:
                zenodo_record.pop(empty_key)


            data_dump.append(zenodo_record)

        except Exception as e:
            status = "[CONVERT] Record #{counter}, DOI={doi} couldn't be converted. Problematic field: {error}.".format(counter=counter, doi=record["doi"], error=str(e.args))

            logging.error(status)
            print(status)

    fieldnames = list(data_dump[0].keys())
    fieldnames.append("partof_title")
    fieldnames.append("partof_pages")

    covihost_csv.write_csv(resulting_filepath, data_dump, fieldnames)

