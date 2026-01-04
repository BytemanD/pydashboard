from typing import List, Mapping

from loguru import logger

from pydashboard.components.chip import MChip
from pydashboard.layout.cell import Cell

from pydashboard.theme import Theme
from pydashboard.style import Variant, Colors
from pydashboard import app


class ComponentsDemo(app.MainWindow):
    def __init__(self):
        super().__init__("纸片")
        self.setup_ui()

    def setup_ui(self):
        self.add_label(Variant.FLAT.value, 0, 0)
        self.add_cell(
            Cell([MChip(f"{x}", color=x) for x in Colors.model_fields]),
            0,
            1,
        )
        self.add_label(Variant.ELEVATED.value, 1, 0)
        self.add_cell(
            Cell([MChip(f"{x}", color=x, variant=Variant.ELEVATED) for x in Colors.model_fields]),
            1,
            1,
        )
        self.add_label(Variant.OUTLINED.value, 2, 0)
        self.add_cell(
            Cell(
                [
                    MChip(f"{x}", color=x, variant="outlined")
                    for x in Colors.model_fields
                ]
            ),
            2,
            1,
        )
        self.add_label(Variant.TEXT, 3, 0)
        self.add_cell(
            Cell([MChip(f"{x}", variant=Variant.TEXT) for x in Colors.model_fields]),
            3,
            1,
        )
        self.add_label("标签属性", 4, 0)
        self.add_cell(
            Cell(
                [
                    MChip(f"{x.value} 标签", label=True, variant=x)
                    for x in [
                        Variant.FLAT,
                        Variant.ELEVATED,
                        Variant.OUTLINED,
                        Variant.TEXT,
                        Variant.PLAIN,
                    ]
                ]
            ),
            4,
            1,
        )
        self.add_label("图标", 5, 0)
        self.add_cell(
            Cell(
                [
                    MChip(f"首页", prepend_icon='mdi.home'),
                    MChip(f"首页", prepend_icon='mdi.plus', append_icon='mdi.trash-can'),
                ]
            ),
            5,
            1,
        )

        # self.add_label("可关闭", 6, 0)
        # self.add_cell(
        #     Cell(
        #         [
        #             MChip(f"首页", prepend_icon='mdi.home', closable=True),
        #         ]
        #     ),
        #     6,
        #     1,
        # )


if __name__ == "__main__":
    app.run(
        ComponentsDemo(),
        theme=Theme(colors=Colors.model_validate({"lime": "#CDDC39"})),
    )
