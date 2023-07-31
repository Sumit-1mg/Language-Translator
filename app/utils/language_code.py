class LanguageCodeHandler:
    def __init__(self):
        self.language_code = {
                'afrikaans': 'af',
                'albanian': 'sq',
                'amharic': 'am',
                'arabic': 'ar',
                'armenian': 'hy',
                'assamese': 'as',
                'aymara': 'ay',
                'azerbaijani': 'az',
                'aambara': 'bm',
                'aasque': 'eu',
                'belarusian': 'be',
                'bengali': 'bn',
                'bhojpuri': 'bho',
                'bosnian': 'bs',
                'bulgarian': 'bg',
                'catalan': 'ca',
                'cebuano': 'ceb',
                'chinese (Simplified)': 'zh-CN',
                'chinese (Traditional)': 'zh-TW',
                'corsican': 'co',
                'croatian': 'hr',
                'czech': 'cs',
                'danish': 'da',
                'dhivehi': 'dv',
                'dogri': 'doi',
                'dutch': 'nl',
                'english': 'en',
                'esperanto': 'eo',
                'estonian': 'et',
                'ewe': 'ee',
                'filipino (Tagalog)': 'fil',
                'finnish': 'fi',
                'french': 'fr',
                'frisian': 'fy',
                'galician': 'gl',
                'georgian': 'ka',
                'german': 'de',
                'greek': 'el',
                'guarani': 'gn',
                'gujarati': 'gu',
                'haitian Creole': 'ht',
                'hausa': 'ha',
                'hawaiian': 'haw',
                'hebrew': 'he',
                'hindi': 'hi',
                'hmong': 'hmn',
                'hungarian': 'hu',
                'icelandic': 'is',
                'igbo': 'ig',
                'ilocano': 'ilo',
                'indonesian': 'id',
                'irish': 'ga',
                'italian': 'it',
                'japanese': 'ja',
                'javanese': 'jv',
                'kannada': 'kn',
                'kazakh': 'kk',
                'khmer': 'km',
                'kinyarwanda': 'rw',
                'konkani': 'gom',
                'korean': 'ko',
                'krio': 'kri',
                'kurdish': 'ku',
                'kurdish (Sorani)': 'ckb',
                'kyrgyz	': 'ky',
                'lao': 'lo',
                'latin': 'la',
                'latvian': 'lv',
                'lingala': 'ln',
                'lithuanian': 'lt',
                'luganda': 'lg',
                'luxembourgish': 'lb',
                'macedonian': 'mk',
                'maithili': 'mai',
                'malagasy': 'mg',
                'malay': 'ms',
                'malayalam': 'ml',
                'maltese': 'mt',
                'maori': 'mi',
                'marathi': 'mr',
                'meiteilon (Manipuri)': 'mni-Mtei',
                'mizo': 'lus',
                'mongolian': 'mn',
                'myanmar (Burmese)': 'my',
                'nepali': 'ne',
                'norwegian': 'no',
                'nyanja (Chichewa)': 'ny',
                'odia (Oriya)': 'or',
                'oromo': 'om',
                'pashto': 'ps',
                'persian': 'fa',
                'polish': 'pl',
                'portuguese (Portugal, Brazil)': 'pt',
                'punjabi': 'pa',
                'quechua': 'qu',
                'romanian': 'ro',
                'russian': 'ru',
                'samoan': 'sm',
                'sanskrit' :'sa',
                'scots Gaelic': 'gd',
                'sepedi': 'nso',
                'serbian': 'sr',
                'sesotho': 'st',
                'shona': 'sn',
                'sindhi': 'sd',
                'sinhala (Sinhalese)': 'si',
                'slovak': 'sk',
                'slovenian': 'sl',
                'somali': 'so',
                'spanish': 'es',
                'sundanese': 'su',
                'swahili': 'sw',
                'swedish': 'sv',
                'tagalog (Filipino)': 'tl',
                'tajik': 'tg',
                'tamil': 'ta',
                'tatar': 'tt',
                'telugu': 'te',
                'thai': 'th',
                'tigrinya': 'ti',
                'tsonga': 'ts',
                'turkish': 'tr',
                'turkmen': 'tk',
                'twi (Akan)': 'ak',
                'ukrainian': 'uk',
                'urdu': 'ur',
                'uyghur': 'ug',
                'uzbek': 'uz',
                'vietnamese': 'vi',
                'welsh': 'cy',
                'xhosa': 'xh',
                'yiddish': 'yi',
                'yoruba': 'yo',
                'zulu': 'zu'}

    def get_code(self,language):
        '''
        if we give language name then it will return the language code
        '''
        return self.language_code[language.strip().lower()]

    def get_language(self,code):
        '''
        if we give language code then it will return the language name.
        '''
        code_lang = {v: k for k, v in self.language_code.items()}
        language = code_lang[code]
        return language[0].upper() + language[1:]

    def is_valid_language(self,language):
        '''
        Validate whether the given language is in the list of supported languages.
        Parameters:
        language (str): The language to be checked.
        Returns: bool: True if the language is supported, False otherwise.
        '''
        return language.strip().lower() in set(self.language_code.keys())

    def get_all_language(self):
        '''
        return the dictionary in which all language names and there codes are stored.
        '''
        return self.language_code

