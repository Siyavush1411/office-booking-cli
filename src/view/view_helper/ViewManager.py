from .TextStyle import TextStyle
from .TextLayout import TextMarkupBuilder


class ViewManager:
    def __init__(self):
        pass

    @staticmethod
    def style_text(text: str) -> str:
        text: str = TextStyle(text)
        return text

    @staticmethod
    def align_text(text: str) -> str:
        markup = TextMarkupBuilder(text)
        return markup

    @staticmethod
    def align_massive_center(text: str) -> str:
        str_list = text.splitlines()
        centered_lines = []
        for line in str_list:
            centered_lines.append(ViewManager.align_text(line).center)
        return "\n".join(centered_lines)
    
    @staticmethod
    def pad_ansi(text_obj, width):
        raw_len = len(text_obj.text)
        return f"{text_obj}{' ' * (width - raw_len)}"