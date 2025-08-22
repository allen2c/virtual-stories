# Virtual Stories

[![PyPI version](https://img.shields.io/pypi/v/virtual-stories.svg)](https://pypi.org/project/virtual-stories/)
[![Python Version](https://img.shields.io/pypi/pyversions/virtual-stories.svg)](https://pypi.org/project/virtual-stories/)
[![License](https://img.shields.io/pypi/l/virtual-stories.svg)](https://opensource.org/licenses/MIT)

The directory structure of the virtual stories is as follows: `virtual_stories/{DOMAIN}/{TOPIC}/{SEQ_NUM}_{DIALOGUE_NAME}_{LANGUAGE_CODE}.txt`

- `{DOMAIN}`: The business domain or industry category, such as "entertainment_platform", "fitness_center", "public_utilities", "e_commerce", "healthcare", "automotive", "financial_services", "telecommunications", "education", "travel_aviation", etc.
- `{TOPIC}`: The type of customer service interaction, such as "product_inquiry", "technical_support", "order_issues", "complaints_resolution", "billing_payment", "after_sales_service", "appointment_scheduling", "loyalty_programs", "emergency_support", "feedback_suggestions".
- `{SEQ_NUM}`: A unique sequential number for each dialogue within a topic, starting from 1 without zero-padding (e.g., 1, 2, 3, not 01, 02, 03).
- `{DIALOGUE_NAME}`: A brief, descriptive name for the dialogue that follows Python variable naming conventions (lowercase with underscores, no special characters or spaces).
- `{LANGUAGE_CODE}`: The ISO language code with hyphens replaced by underscores (e.g., "zh_CN" for Chinese Simplified, "en" for English, "ja" for Japanese).

Dialogue file example:

```plaintext
"""
This is a docstring section.
You can write dialogue description here.
Allowable roles: `user`, `assistant`, `system`, `developer`, `tool`
Valid channels: analysis, commentary, final. Channel must be included for every message.
"""

system:
System prompt put here.

user:
User say something. For example, "What's the weather like in Boston?"

assistant channel=analysis:
# If the channel is `analysis`, that means the assistant is analyzing, thinking and reasoning about the user's message. Content example:
The user is asking for the weather in Boston. I should use the `get_current_weather` tool. I will default to celsius since no unit was specified.

assistant channel=commentary to=tool.get_current_weather:
# The tool is called `get_current_weather`. The tool call must be in channel `commentary`. For example:
{"location": "Boston, MA", "unit": "celsius"}

tool.get_current_weather channel=commentary to=assistant:
The tool output is returned to the assistant in channel `commentary`. For example:
{"temperature": "22", "unit": "celsius", "description": "Partly cloudy"}

assistant channel=analysis:
The tool provided the weather data for Boston: 22 degrees Celsius and partly cloudy. I will now format this into a clear, concise sentence for the user.

assistant channel=final:
The current weather in Boston is 22°C and partly cloudy. 🌤️
```

## Features

## Supported Languages

```python
class LanguageCodes(StrEnum):
    ABKHAZ = "ab"
    ACEHNESE = "ace"
    ACHOLI = "ach"
    AFRIKAANS = "af"
    ALBANIAN = "sq"
    ALUR = "alz"
    AMHARIC = "am"
    ARABIC = "ar"
    ARMENIAN = "hy"
    ASSAMESE = "as"
    AWADHI = "awa"
    AYMARA = "ay"
    AZERBAIJANI = "az"
    BALINESE = "ban"
    BAMBARA = "bm"
    BASHKIR = "ba"
    BASQUE = "eu"
    BATAK_KARO = "btx"
    BATAK_SIMALUNGUN = "bts"
    BATAK_TOBA = "bbc"
    BELARUSIAN = "be"
    BEMBA = "bem"
    BENGALI = "bn"
    BETAWI = "bew"
    BHOJPURI = "bho"
    BIKOL = "bik"
    BOSNIAN = "bs"
    BRETON = "br"
    BULGARIAN = "bg"
    BURYAT = "bua"
    CANTONESE = "yue"
    CATALAN = "ca"
    CEBUANO = "ceb"
    CHICHEWA_NYANJA = "ny"
    CHINESE_SIMPLIFIED = "zh-CN"
    CHINESE_SIMPLIFIED_2 = "zh"
    CHINESE_TRADITIONAL = "zh-TW"
    CHUVASH = "cv"
    CORSICAN = "co"
    CRIMEAN_TATAR = "crh"
    CROATIAN = "hr"
    CZECH = "cs"
    DANISH = "da"
    DINKA = "din"
    DIVEHI = "dv"
    DOGRI = "doi"
    DOMBE = "dov"
    DUTCH = "nl"
    DZONGKHA = "dz"
    ENGLISH = "en"
    ESPERANTO = "eo"
    ESTONIAN = "et"
    EWE = "ee"
    FIJIAN = "fj"
    FILIPINO_TAGALOG = "fil"
    FILIPINO_TAGALOG_2 = "tl"
    FINNISH = "fi"
    FRENCH = "fr"
    FRENCH_FR = "fr-FR"
    FRENCH_CA = "fr-CA"
    FRISIAN = "fy"
    FULFULDE = "ff"
    GA = "gaa"
    GALICIAN = "gl"
    GANDA_LUGANDA = "lg"
    GEORGIAN = "ka"
    GERMAN = "de"
    GREEK = "el"
    GUARANI = "gn"
    GUJARATI = "gu"
    HAITIAN_CREOLE = "ht"
    HAKHA_CHIN = "cnh"
    HAUSA = "ha"
    HAWAIIAN = "haw"
    HEBREW = "iw"
    HEBREW_2 = "he"
    HILIGAYNON = "hil"
    HINDI = "hi"
    HMONG = "hmn"
    HUNGARIAN = "hu"
    HUNSRIK = "hrx"
    ICELANDIC = "is"
    IGBO = "ig"
    ILOKO = "ilo"
    INDONESIAN = "id"
    IRISH = "ga"
    ITALIAN = "it"
    JAPANESE = "ja"
    JAVANESE = "jw"
    JAVANESE_2 = "jv"
    KANNADA = "kn"
    KAPAMPANGAN = "pam"
    KAZAKH = "kk"
    KHMER = "km"
    KIGA = "cgg"
    KINYARWANDA = "rw"
    KITUBA = "ktu"
    KONKANI = "gom"
    KOREAN = "ko"
    KRIO = "kri"
    KURDISH_KURMANJI = "ku"
    KURDISH_SORANI = "ckb"
    KYRGYZ = "ky"
    LAO = "lo"
    LATGALIAN = "ltg"
    LATIN = "la"
    LATVIAN = "lv"
    LIGURIAN = "lij"
    LIMBURGAN = "li"
    LINGALA = "ln"
    LITHUANIAN = "lt"
    LOMBARD = "lmo"
    LUO = "luo"
    LUXEMBOURGISH = "lb"
    MACEDONIAN = "mk"
    MAITHILI = "mai"
    MAKASSAR = "mak"
    MALAGASY = "mg"
    MALAY = "ms"
    MALAY_JAWI = "ms-Arab"
    MALAYALAM = "ml"
    MALTESE = "mt"
    MAORI = "mi"
    MARATHI = "mr"
    MEADOW_MARI = "chm"
    MEITEILON_MANIPURI = "mni-Mtei"
    MINANG = "min"
    MIZO = "lus"
    MONGOLIAN = "mn"
    MYANMAR_BURMESE = "my"
    NDEBELE_SOUTH = "nr"
    NEPALBHASA_NEWARI = "new"
    NEPALI = "ne"
    NORTHERN_SOTHO_SEPEDI = "nso"
    NORWEGIAN = "no"
    NUER = "nus"
    OCCITAN = "oc"
    ODIA_ORIYA = "or"
    OROMO = "om"
    PANGASINAN = "pag"
    PAPIAMENTO = "pap"
    PASHTO = "ps"
    PERSIAN = "fa"
    POLISH = "pl"
    PORTUGUESE = "pt"
    PORTUGUESE_PT = "pt-PT"
    PORTUGUESE_BR = "pt-BR"
    PUNJABI = "pa"
    PUNJABI_SHAHMUKHI = "pa-Arab"
    QUECHUA = "qu"
    ROMANI = "rom"
    ROMANIAN = "ro"
    RUNDI = "rn"
    RUSSIAN = "ru"
    SAMOAN = "sm"
    SANGO = "sg"
    SANSKRIT = "sa"
    SCOTS_GAELIC = "gd"
    SERBIAN = "sr"
    SESOTHO = "st"
    SEYCHELLOIS_CREOLE = "crs"
    SHAN = "shn"
    SHONA = "sn"
    SICILIAN = "scn"
    SILESIAN = "szl"
    SINDHI = "sd"
    SINHALA = "si"
    SLOVAK = "sk"
    SLOVENIAN = "sl"
    SOMALI = "so"
    SPANISH = "es"
    SUNDANESE = "su"
    SWAHILI = "sw"
    SWATI = "ss"
    SWEDISH = "sv"
    TAJIK = "tg"
    TAMIL = "ta"
    TATAR = "tt"
    TELUGU = "te"
    TETUM = "tet"
    THAI = "th"
    TIGRINYA = "ti"
    TSONGA = "ts"
    TSWANA = "tn"
    TURKISH = "tr"
    TURKMEN = "tk"
    TWI_AKAN = "ak"
    UKRAINIAN = "uk"
    URDU = "ur"
    UYGHUR = "ug"
    UZBEK = "uz"
    VIETNAMESE = "vi"
    WELSH = "cy"
    XHOSA = "xh"
    YIDDISH = "yi"
    YORUBA = "yo"
    YUCATEC_MAYA = "yua"
    ZULU = "zu"
```

## Installation

## Quick Start

### Basic Usage

## Configuration

## License

MIT License
