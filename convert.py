import csv
import json
import sys
from dataclasses import asdict, dataclass
from typing import Dict, Final, List, TypedDict

META_KEY: Final[str] = "!!META"


class Metadata(TypedDict):
    name: str
    author: str


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

    output = generate_output(csv_data)

    output_path = sys.argv[2]

    if output_path == "-":
        print(output)
        return

    with open(output_path, "w") as fh:
        fh.write(output)
        print(f"Wrote {output_path}")


def generate_output(csv_data) -> str:
    metadata: Metadata = {
        "name": "STK Generator Checklist",
        "author": "STK Generator",
    }
    groups: Dict[str, Group] = {}

    for row in csv_data:
        gname = row["GROUP"]
        if gname == META_KEY:
            metadata = update_meta(metadata, row)
            continue
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
            "name": metadata["name"],
            "author": metadata["author"],
            "groups": [asdict(g) for g in groups.values()],
        },
        indent=2,
    )

    return json_output


def update_meta(metadata, row) -> Metadata:
    metadata[row["ITEM NAME"].lower()] = row["ITEM STATE"]
    return metadata


def usage():
    print(
        """convert.py usage:

python convert.py [input_csv_file_path] [output_checklist_name]

Use `-` for the output to write to standard out.
"""
    )


if __name__ == "__main__":
    main()
