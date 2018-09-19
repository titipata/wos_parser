# Parser for Web of Science XML dataset

Python XML parser for Web of Science XML file. See example XML file from
[yadudoc/wos_builder](https://github.com/yadudoc/wos_builder/blob/master/sample.xml).
The implementation is based on [yadudoc/wos_builder](https://github.com/yadudoc/wos_builder).
I just make is as a function that can be easily integrate with others platform like
Spark or multiprocessing.

## Example

```python
import wos_parser as wp
records = wp.read_xml('sample.xml')
authors = [wp.extract_authors(record) for record in records] # you can flatten and transform to dataframe
```

## Parser Available

Using `read_xml` in order to read Web of Science XML file to list of element trees.
Each element tree can be parsed to these following function to get dictionary or
list of dictionary output.

- `extract_pub_info`
- `extract_authors`
- `extract_addresses`
- `extract_publisher`
- `extract_funding`
- `extract_conferences`
- `extract_references`
- `extract_identifiers`

## Installation

Clone the repository and install using `setup.py`

```bash
$ git clone https://github.com/titipata/wos_parser
$ cd wos_parser
$ python setup.py install
```

or via pip

```bash
$ pip install git+https://github.com/titipata/wos_parser.git
```

## License

MIT License Copyright (c) 2016 Titipat Achakulvisut
