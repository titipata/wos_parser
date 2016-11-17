# Parser for Web of Science XML dataset

Python XML parser for Web of Science XML file. See example XML file from
[yadudoc/wos_builder](https://github.com/yadudoc/wos_builder/blob/master/sample.xml).
The implementation is based on [yadudoc/wos_builder](https://github.com/yadudoc/wos_builder).
I just try to make is as function.

## Example

```python
import wos_parser as wp
records = wp.read_xml('sample.xml')
authors = [wp.extract_authors(record) for record in records] # you can flatten and transform to dataframe
```

## Parser Available

- `extract_authors`
- `extract_addresses`
- `extract_keywords`
- `extract_publisher`

## Installation

Clone the repository and install using `setup.py`

```bash
$ git clone https://github.com/titipata/wos_parser
$ cd wos_parser
$ python setup.py install
```

## License

MIT License Copyright (c) 2016 Titipat Achakulvisut
