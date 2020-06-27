# python_night_shift_edna_files_generator
python script for creating night shift files using c# edna historian exe

## packaging this python script
use the following command
```bat
pyinstaller src\data_creator.py
```

## eDNA historian adapter exe file
The exe file that is used as eDNA adapter is created by publishing the ASP.NET Core console app hosted at 

## edna historian exe adapter output string format
The adapter output string if quality not included will be like
```
<timestamp1>, <val1>, <timestamp2>, <val2>, ...
```

The adapter output string if quality is included will be like
```
<timestamp1>, <val1>, <quality1>, <timestamp2>, <val2>, <quality2>, ...
```

quality value in the output string is an integer with one of the following values
```
GOOD = 0, BAD = 1, SUSPECT = 2, REPLACED = 3
```