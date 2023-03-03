# SimToolkitPro Checklist Generator

This repo contains a script to convert a CSV checklist to a JSON checklist
suitable for use with [SimToolkitPro][fstk]

## Usage

```shell
python convert.py path/to/input.csv path/to/output.checklist
```

## CSV Format

The CSV file must include headers in the following order:

```text
GROUP
ITEM NAME
ITEM STATE
ITEM DESC
ITEM COLOUR
```

`GROUP` can be the special value `!!META` to provide the checklist name & author
name.

The `ITEM NAME` column should be one of `Name` or `Author`.

The `ITEM STATE` column should provide the appropriate value.

For example, to set the checklist name to `C172 - Normal Procedures` with the
author set to `Kermit` the row would look like:

```csv
!!META,Name,C172 - Normal Procedures,,
!!META,Author,Kermit,,
```

## Author Format

I am versioning the checklists in the author field in this format:

`Lee vYYMMDDN` where the parts are year, month, day with padded zeroes and an
incrementing value starting at 1 in the event I have multiple versions on the
same day.

For example: `Lee v2303021` is the first version released on March 2nd 2023.

[fstk]: https://simtoolkitpro.co.uk/
