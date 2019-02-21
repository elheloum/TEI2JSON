# TEI2JSON

TEI2JSON is a Python script that allows its user to convert a TEI documentation (extracted from : http://roma2.tei-c.org) into a json encoded document. 

## Installation

To use this script, you need python3. You also need to install requirements.txt :

```bash
pip install -r requirements.txt
```

## Input

To test the script, the user can use one of the following files as an input file :
- input/myTEI-3.rng
- input/myTEI-4.rng

## Usage

This project contains 3 scripts:TEI2JSON.py, recup_attributes and recup_children. 
- TEI2JSON.py is the main script (the one that should be launched) .
- recup_attributes and recup_children are support scripts which contain functions that are called by TEI2JSON.py.
  
The script works perfectly from an IDE like PyCharm or Spyder or directly from the the command prompt.  

Thus, you can run the converter by launching the main script from the command prompt, using the line :
```python
python TEI2JSON.py <name_of_an_rng_file>
```
For example :
```python
python TEI2JSON.py input/myTEI-3.rng
```

If you have both Python 2 and Python 3 on your machine, use this line:
```python
python3 TEI2JSON.py <name_of_an_rng_file>
```
For example :
```python
python3 TEI2JSON.py input/myTEI-3.rng
```
or you can launch it directly from the IDE of your choice.

## Documentation

To read the documentation of the project please follow the link below when you download the project : 
[Documentation/documentation.html](Documentation/documentation.html)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
