import csv
from dataclasses import dataclass, asdict
import json
import sys
from collections import defaultdict
from typing import List


@dataclass
class GroupItem:
    item: str
    state: str
    desc: str
    colour: str


@dataclass
class Group:
    name: str
    items: List[GroupItem]


def main():
    if len(sys.argv) < 3:
        usage()
        sys.exit(1)

    file_path = sys.argv[1]
    csv_data = None
    with open(file_path) as fh:
        csv_data = list(csv.DictReader(fh))

    if csv_data is None:
        print(f"No data loaded from {file_path}")
        sys.exit(1)

    metadata = prompt_for_meta()
    output = generate_output(metadata, csv_data)

    output_path = sys.argv[2]
    with open(output_path, "w") as fh:
        fh.write(output)
        print(f"Wrote {output_path}")


def generate_output(metadata, csv_data):
    groups = {}

    for row in csv_data:
        gname = row["GROUP"]
        group = groups.get(gname, Group(name=gname, items=[]))
        group.items.append(
            GroupItem(
                item=row["ITEM NAME"],
                state=row["ITEM STATE"],
                desc=row["ITEM DESC"],
                colour=row["ITEM COLOUR"],
            )
        )
        groups[gname] = group

    json_output = json.dumps(
        {
            "name": metadata["aircraft"],
            "author": metadata["author_name"],
            "groups": [asdict(g) for g in groups.values()],
        },
        indent=2,
    )

    return json_output


def prompt_for_meta():
    ac_name = input("What is the aircaft name? ")
    author_name = input("What is the author name? ")
    return {
        "aircraft": ac_name,
        "author_name": author_name,
    }


def usage():
    print(
        """convert.py usage:

python convert.py [input_csv_file_path] [output_checklist_name]
"""
    )


if __name__ == "__main__":
    main()
