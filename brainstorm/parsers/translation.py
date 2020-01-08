import json


class TranslationParser:
    tag = 'translation'

    def parse(self, context, snapshot):
        context.save('translation.json', json.dumps({
            'x': snapshot.translation.x,
            'y': snapshot.translation.y,
            'z': snapshot.translation.z,
        }).encode())
