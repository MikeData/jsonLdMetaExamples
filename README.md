# jsonLdMetaExamples

simple json Ld meta-examples. based on Leigh Dodds armed-forces metadata example:
https://github.com/ldodds/ons-metadata-examples

## explanation

If you start on the assmumption you have a loadfile at hand, you can generate a metadata file including 1.) Static MetaData (publisher etc), 2.) Metadata thats specificed in the laod file (geography, time, dimensions, etc).

thats what the script does, three example of auto generated metafiles are included.

## Whats the next move?

There's two other metadata sources to consider when populating these files.

System Generated Data: landing page, identifier, anything in distribution

Simple Reference Metadata: title, descripton, keywords etc .... basically any leftover missing fields.

The outstanding issue is going to be deciding on a process/mechanism/tool to capture this missing metadata.

## How do I use this?

Unzip the jsonDUMP file
pip install pandas
drop a V3 load file into the directory and ```python json_derrive.py <filename>```

BUT there's not that much to see and its pretty hacky. Would advise people just look at the provided examples.


