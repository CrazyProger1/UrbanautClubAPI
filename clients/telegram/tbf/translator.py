import functools
import gettext

from conf import settings
from .models import TelegramUser, Language
from utils import filesystem, cls_utils


class Translator(metaclass=cls_utils.SingletonMeta):
    def __init__(self, domain: str = None):
        self._domain = domain
        self._loaded_packs: dict[str, gettext.GNUTranslations] = {}
        self._load()

    def _load(self):
        for language in Language.select():
            try:
                self._loaded_packs.update({
                    language.short_name: gettext.translation(
                        domain=self._domain,
                        localedir=settings.L18N.LOCALE_FOLDER,
                        languages=[language.short_name]
                    )})
            except FileNotFoundError:
                if settings.DEBUG:
                    continue
                raise

    @functools.cache
    def translate(
            self,
            key: str,
            user: TelegramUser = None,
            language: Language = None
    ) -> str:

        if not language and user:
            language = user.language

        if not language:
            language = Language.get_default()

        lang_name = language.short_name

        try:
            return self._loaded_packs[lang_name].gettext(key)
        except KeyError:
            return key


@functools.cache
def _(key: str, user: TelegramUser = None, language: Language = None):
    translator = Translator()
    return translator.translate(key, user, language)
