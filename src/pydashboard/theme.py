from pydantic import BaseModel

from pydashboard.style import Colors, Variant


class Theme(BaseModel):
    colors: Colors = Colors()

    def _get_color(self, name: str) -> str:
        return getattr(self.colors, name)

    def _get_transparent_color(self, name: str) -> str:
        return self._get_color(name).replace("#", "#CC")

    @property
    def style_sheet(self) -> str:
        sheet = f"""
        QPushButton {{
            border-radius: 4px;
            font: 14px;
            padding: 4px 10px 4px 10px;
        }}
        """
        for name in self.colors.model_dump().keys():
            sheet += f"""
            QPushButton[variant="{Variant.FLAT.value}"][color="{name}"],
            QPushButton[variant="{Variant.ELEVATED.value}"][color="{name}"] {{
                background-color: {self._get_color(name)};
                color: white;
            }}
            QPushButton[variant="{Variant.FLAT.value}"][color="{name}"]:hover,
            QPushButton[variant="{Variant.ELEVATED.value}"][color="{name}"]:hover,
            QPushButton[variant="{Variant.OUTLINED.value}"][color="{name}"]:hover,
            QPushButton[variant="{Variant.TEXT.value}"][color="{name}"]:hover {{
                background-color: {self._get_transparent_color(name)};
                color: white;
            }}
            QPushButton[variant="{Variant.OUTLINED.value}"][color="{name}"] {{
                color: {self._get_color(name)};
                border: 1px solid {self._get_color(name)};
            }}
            QPushButton[variant="{Variant.TEXT.value}"][color="{name}"] {{
                color: {self._get_color(name)};
            }}
            QPushButton[variant="{Variant.PLAIN.value}"][color="{name}"] {{
                color: {self._get_color(name)};
            }}
            QPushButton[variant="{Variant.PLAIN.value}"][color="{name}"]:hover {{
                color: {self._get_transparent_color(name)};
            }}
            """
        return sheet
