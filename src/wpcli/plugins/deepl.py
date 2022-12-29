import deepl
from ..conf import DEEPL_AUTH_KEY, DEEPL_LANG, DEEPL_FROM_TO_LANG

translator = deepl.Translator(DEEPL_AUTH_KEY)


def retranslate(value):
    res_lang = translate(value, lang=DEEPL_LANG)
    resp_lang_tmp = translate(res_lang, lang=DEEPL_FROM_TO_LANG)
    return translate(resp_lang_tmp, lang=DEEPL_LANG)


def translate(value, lang=DEEPL_LANG):
    if not value or value == '':
        return value
    r = translator.translate_text(value, target_lang=lang)
    return r.text
