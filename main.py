from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from os.path import split
from math import floor
from PIL import Image
from helpers import *


class Embedder():
    def __init__(
        self,
        embed_path: str,
        embed_position: Tuple[str, str, int],
        embed_scale: float,
        output_dir: str,
    ) -> None:
        self.__embed_path = embed_path
        self.__embed_position = embed_position
        self.__embed_scale = embed_scale
        self.__output_dir = output_dir

    def embed(self, content_paths: List[str]):
        for content_path in content_paths:
            file_name = split(content_path)[1]
            output_path = self.__output_dir + file_name
            (self.__video if file_name.endswith('.mp4') else self.__image)(
                content_path, output_path
            )
        return self.__output_dir

    def __video(self, content_path: str, output_path: str):
        content = VideoFileClip(content_path)
        embed = ImageClip(self.__embed_path)
        embed = embed.resize(self.__embed_scale)  # type: ignore
        embed = embed.set_duration(content.duration)
        position = self.__calculate_position(embed.size, content.size)
        embed = embed.set_position(position)
        CompositeVideoClip([content, embed]).write_videofile(output_path)

    def __image(self, content_path: str, output_path: str):
        content = Image.open(content_path, 'r')
        embed = Image.open(self.__embed_path, 'r')
        new_embed_w = floor(embed.size[0]*self.__embed_scale)
        new_embed_h = floor(embed.size[1]*self.__embed_scale)
        embed = embed.resize((new_embed_w, new_embed_h), Image.ANTIALIAS)
        position = self.__calculate_position(embed.size, content.size)
        content.paste(embed, position)
        content.save(output_path)

    def __calculate_position(self, embed_size: Tuple[int, int], content_size: Tuple[int, int]):
        horizontal_position, vertical_position, margin = self.__embed_position
        embed_w, embed_h = embed_size
        content_w, content_h = content_size
        x = (
            margin if horizontal_position == 'left'
            else content_w - embed_w - margin
        )
        y = (
            margin if vertical_position == 'top'
            else content_h - embed_h - margin
        )
        return (x, y)


def main():
    content_paths = ask(
        'content directory/file: ',
        validators=[is_content_path],
        transformer=text_to_content_paths,
    )

    embed_path = ask(
        'embed file: ',
        validators=[is_embed_path],
        transformer=text_to_file_path,
    )

    output_dir = ask(
        'output directory: ',
        validators=[is_dir],
        transformer=text_to_dir_path,
    )

    embed_horizontal_position = ask(
        'embed horizontal position (left/right): ',
        validators=[is_horizontal_position]
    )

    embed_vertical_position = ask(
        'embed vertical position (top/bottom): ',
        validators=[is_vertical_position]
    )

    embed_margin = ask(
        'embed margin: ',
        validators=[is_numeric],
        transformer=text_to_int
    )

    embed_scale = ask(
        'embed scale: ',
        validators=[is_float, is_greater_than_zero],
        transformer=text_to_float
    )

    embed_position = (
        embed_horizontal_position, embed_vertical_position, embed_margin
    )

    embedder = Embedder(embed_path, embed_position, embed_scale, output_dir)
    return embedder.embed(content_paths)


if __name__ == "__main__":
    try:
        print('output: ', main())
    except Exception as error:
        print('error: ' + str(error))
