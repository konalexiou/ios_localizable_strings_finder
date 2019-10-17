
# iOS/swift localizable strings finder (and auto translator)

This software searches throught your ios swift project, finds all localizable strings and saves them in a localizable.strings file. You can also have these values auto translated with the help of [ssut/py-googletrans](https://github.com/ssut/py-googletrans) package for python.

## Installing

Cloning the repository and running the command is all it takes. If you are using the translator the ssut/py-googletrans package will automatically install if it is not already installed.


## Usage

Basic usage of this script

    python find_localizable_strings.py <path-to-swift-project/directory-with-swift-files>

#### Optional parameters
If you want to modify the output filename use:

    --output <filename-without-extension>
If you prefer to have comments removed from the localized strings you can use:

    --no-comments

If you want to automatically trasnlate the values to another language you can use the following optional arguments:

    --locale-origin <origin-locale-2digit-code> --locale-target <target-locale-2digit-code>

#### Examples
Your project is located in your home folder,  you want to have all project localizable strings in a strings.strings (strings_fr.strings translated strings filename) file and also translate them from english to frensh you can use:

    python find_localizable_strings.py ~/ios-project/project --output strings --no-comments --locale-origin en --locale-target fr



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
