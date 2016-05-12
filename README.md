# Introduction
This script automatically annotates papers on europepmc.org using hypothesis with information gleaned from ContentMine.
Currently it provides information on the IUCN conservation status of species from Wikidata.
 
# Installation Instructions
You must have python 3 and pip installed to use this script.

To run this script you should clone this repository somewhere local.

You should also make a virtualenv to keep the packages from this script from cluttering up your system wide selection of packages.
 
```
virtualenv cmhypy-virtualenv
source cmhypy-virtualenv/bin/activate
pip install -r <path to where you cloned this repo>/cmhypy/requirements.txt
```

The script must be pointed at a CProject *in the current directory* that has been mined for facts with ami. See http://contentmine.org for more
details.

You must also register for an account at http://hypothes.is and then get and API key from the developers page from
account settings.

```
python <path to where you cloned this repo>/cmhypy/cmhypy.py <CprojectName> -u <hypothes.is username> -k <api key> 
```


# Thanks
Thanks goes to hypothesis for the annotation tool, europepmc for hosting of the paper, Chris Kittel who wrote the pyCProject
library for reading ContentMine output, Wikidata (and the WDQS) for providing the ICUN status data and finally to
Raymond Yee who wrote the initial implementation of the python hypothesis client which is available
 at https://github.com/rdhyee/hypothesisapi

## Pronounciation
I propose cmhypy is pronounced See-Emm-Hi-Pi
