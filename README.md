# jsonLdMetaExamples

simple json Ld meta-examples. based on Leigh Dodds armed-forces metadata example:
https://github.com/ldodds/ons-metadata-examples

## explanation

If you start with the assumption you have a loadfile at hand, you can generate a metadata file including 1.) Static MetaData (publisher etc), 2.) Metadata thats specificed in the load file (geography, time, dimensions, etc).

thats what the script does, three example of generated metafiles are included to give us an idea of where we're heading. the order is a bit off compared to Leighs but it doesnt really matter with json.


## Whats the next move?

There's two other metadata sources to consider in order to complete these examples.

System Generated Data: landing page, identifier, anything in distribution

Simple Reference Metadata: title, descripton, keywords etc .... basically any still missing.

The outstanding issue is going to be deciding on a process/mechanism/tool to capture the simple reference metadata as there's not really a practical way to automate this.


## How do I use this script?

Honestly it's pretty hacky so I'd just use the examples. 

If you absulutely have to though...............

Unzip the jsonDUMP file
pip install pandas
drop a V3 load file into the directory and ```python json_derrive.py <filename>```

It doesn't currently do months (didn't get around to it) but there's no blocker to it.
