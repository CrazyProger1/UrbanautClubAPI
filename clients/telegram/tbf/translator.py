import functools
import gettext
import os
from conf import settings
from .models import TelegramUser, Language
from utils import filesystem, cls_utils


class Translator(metaclass=cls_utils.SingletonMeta):
    def __init__(self, domain: str = None):
        self._domain = domain
        self._loaded_packs: dict[str, gettext.GNUTranslations] = {}
        self._translation_files_content = {}
        self._load()

    @functools.cache
    def _get_translation_file_path(self, language: Language):
        return os.path.join(
            settings.L18N.LOCALE_FOLDER,
            language.short_name,
            'LC_MESSAGES',
            self._domain + '.po'
        )

    def _read_translation_file(self, language: Language):
        self._translation_files_content[language.short_name] = filesystem.read(
            self._get_translation_file_path(language),
            encoding='utf-8'
        )

    @functools.cache
    def _update_translation_file(self, language: Language, key: str):
        self._translation_files_content[language.short_name] += f'''
msgid "{key}"
msgstr "{key}"
'''
        filesystem.write(
            self._get_translation_file_path(language),
            self._translation_files_content[language.short_name],
            encoding='utf-8'
        )

    def _load(self):
        for language in Language.select():
            try:
                self._loaded_packs.update({
                    language.short_name: gettext.translation(
                        domain=self._domain,
                        localedir=settings.L18N.LOCALE_FOLDER,
                        languages=[language.short_name]
                    )})
                if settings.L18N.UPDATE_TRANSLATIONS:
                    self._read_translation_file(language)
            except FileNotFoundError:
                if settings.DEBUG:
                    continue
                raise

    @functools.cache
    def translate(
            self,
            key: str,
            user: TelegramUser = None,
            language: Language = None,
            default: str = None,
    ) -> str:

        if not language and user:
            language = user.language

        if not language:
            language = Language.get_default()

        lang_name = language.short_name
        try:
            translation = self._loaded_packs[lang_name].gettext(key)
            if translation == key:
                if settings.L18N.UPDATE_TRANSLATIONS:
                    self._update_translation_file(language, key)
                return default or translation
            return translation
        except KeyError as e:
            return key


@functools.cache
def _(key: str, user: TelegramUser = None, language: Language = None, default: str = None) -> str:
    translator = Translator()
    return translator.translate(key, user, language, default=default)
