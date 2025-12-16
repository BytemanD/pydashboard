# -*- coding: utf-8 -*-

from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from pydantic import BaseModel

from pydashboard.models import TableHeader


class Table(MDDataTable):
    def __init__(
        self, headers: list[TableHeader], use_pagination=True, rows_num=10, check=True
    ):
        self.headers = headers
        super().__init__(
            use_pagination=use_pagination,
            rows_num=rows_num,
            check=check,
            column_data=[(x.label or x.name, dp(30)) for x in headers],
            row_data=[],
            elevation=2,
        )

    @property
    def columns(self):
        return [x[0] for x in self.column_data]

    @property
    def data(self):
        return self.row_data

    # def on_row_press(self, instance_row):
    #     """处理行点击事件"""
    #     row_index = instance_row.index // len(self.column_data)

    #     # 检查是否点击了操作列
    #     if instance_row.index % len(instance_table.column_data) == 4:  # 操作列是第5列
    #         # 获取点击的图标
    #         col = instance_row.index % len(instance_table.column_data)
    #         if col == 4:
    #             # 显示操作菜单
    #             self.show_action_dialog(row_index)
    def on_check_press(self, row_data: list):
        """Called when the check box in the table row is checked."""
        print(2222, self, row_data)

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

    def delete_selected(self):
        """删除选中的行"""
        self.row_data.pop(-1)

    def add_data(self, data: BaseModel):
        data_dict = data.model_dump()
        self.row_data.append([data_dict.get(k.name, '') for k in self.headers])
