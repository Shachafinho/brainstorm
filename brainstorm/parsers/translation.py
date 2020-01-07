class TranslationParser:
    tag = 'translation'

    def parse(self, context, snapshot):
        print(f'Translation={snapshot.translation}')
