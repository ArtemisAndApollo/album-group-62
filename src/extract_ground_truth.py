from handlers.handler_factory import HandlerFactory
from outputs.output import pretty_print_disk_entries, pretty_print_disk_entry_with_cid, save_to_csv

def _save_ground_truth(filepath, ground_truth):
    ids = ["id_0", "cid_0", "id_1", "cid_1"]
    ground_truth_ids = []

    for gt in ground_truth:
        filtered_gt = \
        {
            key: (";".join(gt[key]) if key in {'cid_0', 'cid_1'} else gt[key])
            for key in ids if key in gt
        }
        ground_truth_ids.append(filtered_gt)

    save_to_csv(filepath, ids, ground_truth_ids)

if __name__ == "__main__":

    # Mining XML file with CDDB dublicates
    factory = HandlerFactory()
    total_items_dubs = 298 # Total number is 298
    filepath_cddb_dups_data = "data/cddb_9763_dups.xml"
    cddb_dups_handler_all = factory.create("dups", data_path=filepath_cddb_dups_data, total_items=total_items_dubs)
    cddb_dups_entries_all = cddb_dups_handler_all.get_entries()

    # Printing details
    max_entries = 0 
    id_length = 5 # Ideal for cbbd_9763_dups.xml
    # pretty_print_disk_entries(entries=cddb_dups_entries_all, max_entries=max_entries, id_length=5, entry_name="Disk")
    pretty_print_disk_entry_with_cid(entries=cddb_dups_entries_all, id_length=id_length, entry_name="Disk", cids=["ad10720c"])

    # Saving to CSV
    if len(cddb_dups_entries_all) == 298:
        ground_truth_path = r"output/ground_truth/ground_truth"
        _save_ground_truth(ground_truth_path, cddb_dups_entries_all)
    
    