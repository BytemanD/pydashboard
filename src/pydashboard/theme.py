from pydantic import BaseModel

from pydashboard.style import Colors, Variant


class Theme(BaseModel):
    colors: Colors = Colors()
    default_border_raidus: str = '3px'

    def _get_color(self, name: str) -> str:
        return getattr(self.colors, name)

    def get_color(self, name: str):
        return self.colors.translate(name) or self.colors.primary

    def _get_transparent_color(self, name: str) -> str:
        return self._get_color(name).replace("#", "#CC")

    @property
    def style_sheet(self) -> str:
        sheet = """
        QFrame {
            border: 1px soild #2196F3;
            border-radius: 3px;
        }
        QFrame[variant="text"] {
            border: none;
        }
        QPushButton {
            border-radius: 3px;
            font: 14px;
            padding: 4px 10px 4px 10px;
        }
        QPushButton[rounded="0"] {
            border-radius: 0px;
        }
        QPushButton[rounded="md"] {
            border-radius: 6px;
        }
        QPushButton[rounded="lg"] {
            border-radius: 9px;
        }
        QPushButton[rounded="xl"] {
            border-radius: 13px;
        }
        QPushButton[rounded-left="0"] {
            border-top-left-radius: 0px;
            border-bottom-left-radius: 0px;
        }
        QPushButton[rounded-left="md"] {
            border-top-left-radius: 6px;
            border-bottom-left-radius: 6px;
        }
        QPushButton[rounded-left="lg"] {
            border-top-left-radius: 9px;
            border-bottom-left-radius: 9px;
        }
        QPushButton[rounded-left="xl"] {
            border-top-left-radius: 12px;
            border-bottom-left-radius: 12px;
        }
        QPushButton[rounded-left="0"] {
            border-top-left-radius: 0px;
            border-bottom-left-radius: 0px;
        }
        QPushButton[rounded-right="0"] {
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
        }
        QPushButton[roundrounded-right="md"] {
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
        }
        QPushButton[rounded-right="lg"] {
            border-top-right-radius: 9px;
            border-bottom-right-radius: 9px;
        }
        QPushButton[rounded-right="xl"] {
            border-top-right-radius: 12px;
            border-bottom-right-radius: 12px;
        }

        QPushButton[border-left-color="grey"] {
            border-left: 1px solid grey;
        }
        QPushButton[border-right-color="grey"] {
            border-right: 1px solid grey;
        }

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
            QPushButton[variant="{Variant.FLAT.value}"][color="{name}"]:disabled,
            QPushButton[variant="{Variant.ELEVATED.value}"][color="{name}"]:disabled {{
                background-color:  {self._get_transparent_color(name)};
            }}
            QPushButton[variant="{Variant.OUTLINED.value}"][color="{name}"]:disabled {{
                color: {self._get_transparent_color(name)};
                border: 1px solid {self._get_transparent_color(name)};
            }}
            QPushButton[variant="{Variant.TEXT.value}"][color="{name}"]:disabled {{
                color: {self._get_transparent_color(name)};
            }}
            QPushButton[variant="{Variant.PLAIN.value}"][color="{name}"]:disabled {{
                color: {self._get_transparent_color(name)};
            }}
            """
        return sheet
