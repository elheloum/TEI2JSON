# TEI2JSON

TEI2JSON is a Python script that allows its user to convert a TEI documentation (extracted from : http://roma.tei-c.org) into a json encoded document.

## Installation

To use this script, the user needs to install the library that is used in this script: 
- Beautiful soup 

```bash
pip install beautifulsoup4
```
He also needs to make sure he has the following libraries: 
- json
- OrderedDict

## Input

To test the script, the user can use one of the following files as an input file : 
- myTEI-3.rng
- myTEI-4.rng

## Usage

For the instance, the script is works perfectly from the IDE : PyCharm or Spyder.
Therefore, to get the perfect result, it should be launched from one of those IDE. 

The script contains 2 methods. It is fundamental to launch the first method (def file_tag(rng_file)) before the second one. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)