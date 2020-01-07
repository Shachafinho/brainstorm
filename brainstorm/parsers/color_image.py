class ColorImageParser:
    tag = 'color_image'

    def parse(self, context, snapshot):
        print(f'ColorImage={snapshot.color_image}')
