from typing import List, Mapping

from loguru import logger

from pydashboard.components.button import MButton
from pydashboard.components.button_group import ButtonGroup
from pydashboard.layout.cell import Cell

from pydashboard.theme import Theme
from pydashboard.style import Variant, Colors
from pydashboard import app


class ComponentsDemo(app.MainWindow):
    def __init__(self):
        super().__init__("按钮")
        self.setup_ui()

    def setup_ui(self):
        self.add_label(Variant.FLAT.value, 0, 0)
        self.add_cell(
            Cell([MButton(x, color=x) for x in Colors.model_fields.keys()]),
            0,
            1,
        )
        self.add_label(Variant.ELEVATED.value, 1, 0)
        self.add_cell(
            Cell(
                [
                    MButton(x, color=x, variant=Variant.ELEVATED)
                    for x in Colors.model_fields.keys()
                ]
            ),
            1,
            1,
        )
        self.add_label(Variant.OUTLINED.value, 2)
        self.add_cell(
            Cell(
                [
                    MButton(x, color=x, variant=Variant.OUTLINED)
                    for x in Colors.model_fields.keys()
                ]
                + [
                    MButton("lime", color="lime", variant=Variant.OUTLINED),
                ]
            ),
            2,
            1,
        )
        self.add_label(Variant.TEXT.value, 3)
        self.add_cell(
            Cell(
                [
                    MButton(x, color=x, variant=Variant.TEXT)
                    for x in Colors.model_fields.keys()
                ]
            ),
            3,
            1,
        )
        self.add_label(Variant.PLAIN.value, 4)

        self.add_cell(
            Cell(
                [
                    MButton(x, color=x, variant=Variant.PLAIN)
                    for x in Colors.model_fields.keys()
                ]
            ),
            4,
            1,
        )
        self.add_label("带图标的按钮", 5)
        self.add_cell(
            Cell(
                [
                    MButton("information", color="info", icon="mdi.information"),
                    MButton("bell", color="primary", icon="mdi.bell"),
                    MButton(
                        "首页", color="warning", variant=Variant.TEXT, icon="mdi.home"
                    ),
                    MButton(
                        "alert", color="danger", variant=Variant.PLAIN, icon="mdi.alert"
                    ),
                ]
            ),
            5,
            1,
        )
        self.add_label("禁用按钮", 6)
        self.add_cell(
            Cell(
                [
                    MButton("删除", color="danger").disable(),
                    MButton("删除", color="danger", variant=Variant.ELEVATED).disable(),
                    MButton("删除", color="danger", variant=Variant.OUTLINED).disable(),
                    MButton("删除", color="danger", variant=Variant.TEXT).disable(),
                    MButton("删除", color="danger", variant=Variant.PLAIN).disable(),
                ]
            ),
            6,
            1,
        )
        self.add_label("直角按钮", 7)
        self.add_cell(
            Cell(
                [
                    MButton("hello, world", border_radius="none"),
                    MButton(
                        "hello, world", border_radius="none", variant=Variant.ELEVATED
                    ),
                    MButton(
                        "hello, world", border_radius="none", variant=Variant.OUTLINED
                    ),
                ]
            ),
            7,
            1,
        )
        self.add_label("圆角按钮", 8)
        self.add_cell(
            Cell(
                [
                    MButton("sm radius", border_radius="sm"),
                    MButton("sm radius", border_radius="sm", variant=Variant.ELEVATED),
                    MButton("sm radius", border_radius="sm", variant=Variant.OUTLINED),
                    MButton("md radius", border_radius="md", color="success"),
                    MButton(
                        "md radius",
                        border_radius="md",
                        color="success",
                        variant=Variant.ELEVATED,
                    ),
                    MButton(
                        "md radius",
                        border_radius="md",
                        color="success",
                        variant=Variant.OUTLINED,
                    ),
                    MButton("lg radius", border_radius="lg", color="warning"),
                    MButton(
                        "lg radius",
                        border_radius="lg",
                        color="warning",
                        variant=Variant.ELEVATED,
                    ),
                    MButton(
                        "lg radius",
                        border_radius="lg",
                        color="warning",
                        variant=Variant.OUTLINED,
                    ),
                    MButton(
                        "xl radius",
                        border_radius="xl",
                        color="danger",
                        variant="outlined",
                    ),
                    MButton(
                        "round radius",
                        border_radius="round",
                        color="cyan",
                        variant="outlined",
                    ),
                ]
            ),
            8,
            1,
        )

        # self.add_label("按钮组", 9)
        # self.add_cell(
        #     Cell(
        #         [
        #             ButtonGroup(
        #                 [
        #                     MButton("", icon="mdi.plus"),
        #                     MButton("", icon="mdi.trash-can"),
        #                 ]
        #             ),
        #             ButtonGroup(
        #                 [
        #                     MButton("", icon="mdi.plus"),
        #                     MButton("", icon="mdi.trash-can"),
        #                 ],
        #                 border_radius="xl",
        #             ),
        #             ButtonGroup(
        #                 [
        #                     MButton("", icon="mdi.plus"),
        #                     MButton("", icon="mdi.trash-can"),
        #                     MButton("", icon="mdi.refresh"),
        #                 ]
        #             ),
        #             ButtonGroup(
        #                 [
        #                     MButton("", icon="mdi.plus"),
        #                     MButton("", icon="mdi.trash-can"),
        #                     MButton("", icon="mdi.refresh"),
        #                     MButton("", icon="mdi.home"),
        #                 ],
        #                 color="primary",
        #                 border_radius="round",
        #             ),
        #         ],
        #     ),
        #     9,
        #     1,
        # )


if __name__ == "__main__":
    app.run(
        ComponentsDemo(),
        theme=Theme(colors=Colors.model_validate({"lime": "#CDDC39"})),
    )
