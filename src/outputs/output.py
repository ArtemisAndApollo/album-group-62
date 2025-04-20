import csv
import datetime
from xml.dom.minidom import Document
import json

def save_to_csv(filename, fieldnames, rows, display_header=False, with_timestamp=False, timestamp_value=None):
    if with_timestamp:
        filename += _get_timestamp(timestamp_value)
    filename += ".csv"

    with open(filename,"w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if display_header:
            writer.writeheader()
        writer.writerows(rows)

def save_to_xml(filename, root: Document, with_timestamp=False, timestamp_value=None, pretty_xml = True, encoding='utf-8'):
    if with_timestamp:
        filename += _get_timestamp(timestamp_value)
    filename += ".xml"

    with open(filename, 'w', encoding=encoding) as f:
        if pretty_xml:
            f.write(root.toprettyxml(indent='  ', encoding=encoding).decode(encoding))
        else:
            f.write(root.toxml(encoding=encoding).decode(encoding))

def save_to_json(filename, data, with_timestamp=False, timestamp_value=None):
    if with_timestamp:
        filename += _get_timestamp(timestamp_value)
    filename += ".json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def pretty_print_disk_entries(entries, max_entries, id_length, entry_name):
    
    print(f"Total number of {entry_name} entries:", len(entries))
    print(f"Printing {max_entries} of them:")

    for i, entry in enumerate(entries):
        if i >= max_entries:
            break
        print(f"\n-------------- {entry_name} number: {i+1} --------------\n")
        for key, value in entry.items():
            tab = "\t"
            if len(key) <= id_length:
                tab += "\t"
            if isinstance(value, list):
                print(f"{key}: {tab}{('\n\t'+tab).join(value)}")
            else:
                print(f"{key}: {tab+str(value)}")
        print('\n')

def pretty_print_disk_entry_with_id(entries, id_length, entry_name, ids):
    
    # print(f"Total number of {entry_name} entries:", len(entries))

    for i, entry in enumerate(entries):
        # Check if the entry id is in the list of ids
        if entry['id'] not in ids:
            continue

        # print(f"\n-------------- {entry_name} number: {i+1} --------------\n")

        for key, value in entry.items():
            tab = "\t"
            if len(key) <= id_length:
                tab += "\t"
            if isinstance(value, list):
                if key == 'cid':
                    print(f"{key}: {tab}{(", ").join(value)}")
                else:
                    print(f"{key}: {tab}{('\n\t'+tab).join(value)}")
            else:
                print(f"{key}: {tab+str(value)}")
        print('\n')

def _get_timestamp(timestamp_value=None):
    if timestamp_value is None:
        timestamp = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")
    else:
        timestamp = timestamp_value
    
    return timestamp
