# -*- coding: utf-8 -*-
import os
import random
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp

from kivymd.uix.label import MDLabel

import copy
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path
from kivymd.font_definitions import theme_font_styles
from pydantic import BaseModel

from pydashboard.models import TableHeader
from pydashboard.table import Table

# 添加字体路径
resource_add_path(os.path.abspath("fonts"))
# 注册新的字体
LabelBase.register("Roboto", fn_regular="msyh.ttf")
# theme_font_styles.append('Roboto')

KV = """
BoxLayout:
    orientation: 'vertical'
    
    MDTopAppBar:
        id: top_app_bar
        title: "可编辑数据表"
        elevation: 1
        left_action_items: [['plus', lambda x: app.add_row()]]

    MDBoxLayout:
        size_hint_y: None
        height: dp(50)
        padding: "10dp"
        spacing: "10dp"
        
        MDRaisedButton:
            text: "添加行"
            on_release: app.add_row()
        
        MDRaisedButton:
            text: "删除选中"
            on_release: app.delete_selected()
    MDScreen:
        id: container
    
"""


class EditableDataTableApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.editing_row = None
        self.data = []
        self.theme_cls.font_styles["Roboto"] = [
            "Roboto",
            16,
            False,
            0.15,
        ]
        self.theme_cls.font_styles.update(
            {
                "H1": ["Roboto", 96, False, -1.5],
                "H2": ["Roboto", 60, False, -0.5],
                "H3": ["Roboto", 48, False, 0],
                "H4": ["Roboto", 34, False, 0.25],
                "H5": ["Roboto", 24, False, 0],
                "H6": ["Roboto", 20, False, 0.15],
                "Subtitle1": ["Roboto", 16, False, 0.15],
                "Subtitle2": ["Roboto", 14, False, 0.1],
                "Body1": ["Roboto", 16, False, 0.5],
                "Body2": ["Roboto", 14, False, 0.25],
                "Button": ["Roboto", 14, True, 1.25],
                "Caption": ["Roboto", 12, False, 0.4],
                "Overline": ["Roboto", 10, True, 1.5],
            }
        )
        self.table = Table(
            [
                TableHeader(label="ID", name="id"),
                TableHeader(label="名称", name="name"),
                TableHeader(label="描述", name="description"),
            ]
        )

    def build(self):
        # return MDLabel(text="Hello, World,开心快乐每一天", halign="center",font_style='Roboto')

        layout = Builder.load_string(KV)

        # 初始化数据
        self.data = [
            ["John", "Doe", "30", "Developer"],
            ["Jane", "Smith", "25", "Designer"],
            ["Bob", "Johnson", "35", "Manager"],
        ]

        # 绑定行点击事件
        self.table.bind(
            on_row_press=self.on_row_press, on_check_press=self.on_check_press
        )
        layout.ids.container.add_widget(self.table)
        layout.ids.top_app_bar.font_name = "Roboto"

        return layout

    def get_row_data(self):
        row_data = []
        for i, row in enumerate(self.data):
            row_with_actions = row + [["pencil", "delete"], "操作"]
            print(row_with_actions)
            row_data.append(row_with_actions)
        return row_data

    def on_row_press(self, instance_table, instance_row):
        """处理行点击事件"""
        row_index = instance_row.index // len(instance_table.column_data)

        # 检查是否点击了操作列
        if instance_row.index % len(instance_table.column_data) == 4:  # 操作列是第5列
            # 获取点击的图标
            col = instance_row.index % len(instance_table.column_data)
            if col == 4:
                # 显示操作菜单
                self.show_action_dialog(row_index)

    def on_row_press(self, instance_table, instance_row):
        """Called when a table row is clicked."""

        print(1111, instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        """Called when the check box in the table row is checked."""

        print(2222, instance_table, current_row)

    def sort_on_signal(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][2]))

    def sort_on_schedule(self, data):
        return zip(
            *sorted(
                enumerate(data),
                key=lambda l: sum(
                    [
                        int(l[1][-2].split(":")[0]) * 60,
                        int(l[1][-2].split(":")[1]),
                    ]
                ),
            )
        )

    def sort_on_team(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][-1]))

    def show_action_dialog(self, row_index):
        """显示操作对话框"""
        self.editing_row = row_index

        # 创建编辑对话框
        self.dialog = MDDialog(
            title="编辑",
            type="custom",
            content_cls=Builder.load_string(
                """
MDBoxLayout:
    orientation: 'vertical'
    spacing: "12dp"
    size_hint_y: None
    height: "300dp"
    
    MDTextField:
        id: name
        hint_text: "姓名"
        text: ""
    
    MDTextField:
        id: last_name
        hint_text: "姓氏"
        text: ""
    
    MDTextField:
        id: age
        hint_text: "年龄"
        text: ""
    
    MDTextField:
        id: position
        hint_text: "职位"
        text: ""
"""
            ),
            buttons=[
                MDFlatButton(
                    text="取消",
                    theme_text_color="Custom",
                    on_release=lambda x: self.dialog.dismiss(),
                ),
                MDFlatButton(
                    text="保存", theme_text_color="Custom", on_release=self.save_row
                ),
                MDFlatButton(
                    text="删除",
                    theme_text_color="Custom",
                    text_color=(1, 0, 0, 1),
                    on_release=self.delete_row,
                ),
            ],
        )

        # 填充当前数据
        if row_index < len(self.data):
            row_data = self.data[row_index]
            self.dialog.content_cls.ids.name.text = row_data[0]
            self.dialog.content_cls.ids.last_name.text = row_data[1]
            self.dialog.content_cls.ids.age.text = row_data[2]
            self.dialog.content_cls.ids.position.text = row_data[3]

        self.dialog.open()

    def save_row(self, instance):
        """保存行数据"""
        if self.editing_row is not None:
            name = self.dialog.content_cls.ids.name.text
            last_name = self.dialog.content_cls.ids.last_name.text
            age = self.dialog.content_cls.ids.age.text
            position = self.dialog.content_cls.ids.position.text

            if self.editing_row < len(self.data):
                # 更新现有行
                self.data[self.editing_row] = [name, last_name, age, position]
            else:
                # 添加新行
                self.data.append([name, last_name, age, position])

            # 更新表格
            self.table.row_data = self.get_row_data()
            self.dialog.dismiss()

    def delete_row(self, instance):
        """删除行"""
        if self.editing_row is not None and self.editing_row < len(self.data):
            del self.data[self.editing_row]
            self.table.row_data = self.get_row_data()
            self.dialog.dismiss()

    def add_row(self):
        """添加新行"""
        import string

        data = Data(
            id=len(self.table.data) + 1,
            name="".join(random.choices(string.ascii_letters, k=4)),
            description="",
        )
        self.table.add_data(data)

    def delete_selected(self):
        """删除选中的行"""
        self.table.row_data.pop(-1)
        if self.table.row_data:
            # 这里可以实现删除逻辑
            # 注意：MDDataTable没有内置的多选功能
            pass


class Data(BaseModel):
    id: int
    name: str
    description: str


if __name__ == "__main__":
    EditableDataTableApp().run()
