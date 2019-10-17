# -*- coding: utf-8 -*-

import argparse
import os
import mmap
import re
import pip
import io
from pip._internal.utils.misc import get_installed_distributions

def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

def append_to_file(text):
    f = open(args.output+".strings", "a+")
    f.write(text+"\n")
    f.close()

def append_to_file_dest(text, dest):
    f = open(args.output+"_"+dest+".strings", "a+")
    text = text.encode('utf-8')
    f.write(text+"\n")
    f.close()

# check installed packages
installed_packages = get_installed_distributions()
flat_installed_packages = [package.project_name for package in installed_packages]

# parse args
parser = argparse.ArgumentParser()
parser.add_argument("directory", help="the directory to search localizable strings in")
parser.add_argument("--output", default="Localizable", help="the file (without extension) to output the localizable strings")
parser.add_argument("--no-comments", action='store_true', help="use this to skip comments on the localizable strings")
parser.add_argument("--locale-origin", help="set the origin locale for auto translation")
parser.add_argument("--locale-target", help="set the target locale for auto translation")
args = parser.parse_args()

# check if you need to translate
if args.locale_origin and args.locale_target:
    if 'googletrans' not in flat_installed_packages:
        print("Installing googletrans... ")
        install('googletrans')
    from googletrans import Translator
    translator = Translator()
else:
    print("locale-origin and locale-target are both needed for translation")

# get swift files in directory
for file in os.listdir(args.directory):
    if file.endswith(".swift"):
        f = os.path.join(args.directory, file)
        print("Searching... " + f)
        # with open(f, 'r+') as f:
        with io.open(f, 'r+', encoding="utf-8") as f:
            data = mmap.mmap(f.fileno(), 0)
            # /NSLocalizedString\((.*)\)/gm
            results = re.finditer('NSLocalizedString\(\"(.*)\"\)', data)
            if results:
                for result in results:
                    result = result.group(1).replace("value:","").replace("comment:","")
                    result = re.sub(r'\",(\s*)\"', '","', result)
                    groups = result.split('","')
                    key = groups[0].replace("\"","").strip()
                    value = groups[1].strip()
                    comment = groups[2].strip()
                    if args.no_comments:
                        trans = ""
                        trans_dest = ""
                    else:
                        trans = "/* " + comment + " */\n"
                        trans_dest = "/* " + comment + " */\n"
                    trans += "\"" + key + "\" = \"" + value + "\";\n"
                    append_to_file(trans)
                    if args.locale_origin and args.locale_target:
                        try:
                            value_dest = translator.translate(value, src=args.locale_origin, dest=args.locale_target)
                        except:
                            value_dest.text = value
                        trans_dest += "\"" + key + "\" = \"" + value_dest.text + "\";\n"
                        append_to_file_dest(trans_dest, args.locale_target)
                    print("found translation: " + key)
