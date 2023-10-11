'''多日数据分析可视化模块'''
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Timeline
from pyecharts.globals import ThemeType
import pandas as pd
import pdb

'''globals配置文件'''
toolbox_opts = {
    "is_show": True,  # 控制工具箱是否显示
    "pos_left": "center",  # 将工具栏放在上方中间
    "pos_top": "10%",  # 控制工具栏的垂直位置，这里设置为距离顶部 10%
    "feature": {
        "dataZoom": {"type": "inside", "xAxisIndex": [0], "orient": "horizontal"},  # 缩放工具表示水平缩放
        "dataView": {"readOnly": False},  # 数据视图工具，允许用户查看和到处
        "magicType": {"type": ["line", "bar"]},  # 视图切换工具
        "restore": {},  # 图表初始话
        "saveAsImage": {},  # 图片保存工具
    },
}
'''数据获取配置文件'''
summ_keys = ['曝光UV', 'UV总和', 'CTR', '客户数总和', 'UV客户转化率', '销售额总和', '销售量总和', '平均单价']

'''多日经营数据柱形图可视化'''


def days_pyecharts_bar(data_frame):
    '''

    :param data_frame: 分析完成的dataframe数据集：multi_data_analysis_duori
    :return:
    '''
    # pdb.set_trace()  # 调试模块
    days_pyecharts_dataframe_time = data_frame['日期']
    bar = (
        Bar(
            init_opts=opts.InitOpts(chart_id='oneday_pyecharts_one')
        )
            .add_xaxis([days_pyecharts_dataframe_time[i] for i in range(len(days_pyecharts_dataframe_time))])
    )
    for col in summ_keys:
        bar.add_yaxis(col, data_frame[col].tolist())

    bar.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"{days_pyecharts_dataframe_time[0]}~{days_pyecharts_dataframe_time.iloc[-1]}日经营数据可视化",
            title_textstyle_opts=opts.TextStyleOpts(font_style=25),
            pos_right='30%',
            pos_top='0.1%'
        ),
        xaxis_opts=opts.AxisOpts(type_='category', name='日期'),
        tooltip_opts=opts.TooltipOpts(trigger='axis'),
        legend_opts=opts.LegendOpts(pos_right='0.01%',
                                    pos_top='12%',
                                    orient='vertical',
                                    textstyle_opts=opts.TextStyleOpts(
                                        font_size=7,
                                    ),
                                    ),
        datazoom_opts=opts.DataZoomOpts(is_show=True, pos_right='10%', pos_top='90%'),
        toolbox_opts=toolbox_opts,
    )
    return bar


'''经营数据附图饼数据转换方法'''


def days_pyecharts_data_list(data_frame):
    '''

    :param data_frame: 处理完成得数据[[a,1,2,3],[b,1,2,3],[c,1,2,3]]
    :return:[[[a,1],[b,1],[c,1]],[[a,2],[b,2],[b,3]],[[c,1],[c,2],[c,3]]]
    '''
    columns_name = [col[0] for col in data_frame]  # 获取名字
    values_data = [col[1:] for col in data_frame]  # 获取数据
    transposed_data = list(map(list, zip(*values_data)))
    result = [[list(col) for col in zip(columns_name, row)] for row in transposed_data]
    return result


'''经营数据附图饼形图'''


def days_pyecharts_pie_ctr_business(data_frame):
    '''

    :param data_frame: 分析完成的dataframe数据集：multi_data_analysis_duori
    :return: pie,t
    '''
    # pdb.set_trace()  # 调试模块
    days_pyecharts_dataframe_time = data_frame['日期']
    days_pyecharts_dataframe_zip = [list(i) for i in zip(data_frame.loc[:, summ_keys[0:3]].columns.tolist(),
                                                         *data_frame.loc[:, summ_keys[0:3]].values.tolist())]
    days_pyecharts_dataframe_data = days_pyecharts_data_list(data_frame=days_pyecharts_dataframe_zip)

    tl = (
        Timeline(init_opts=opts.InitOpts(
            theme=ThemeType.DARK
        )
        )
            .add_schema(
            is_auto_play=True,
            play_interval=1500)
    )
    for i in range(len(days_pyecharts_dataframe_time)):
        pie = (
            Pie()
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{days_pyecharts_dataframe_time[0]}~{days_pyecharts_dataframe_time.iloc[-1]}\n转化率",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=12)
                ),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="0.1%", pos_left="70%"),
            )
                .set_series_opts(
                label_opts=opts.LabelOpts(is_show=True),
                minAngle=1,
                radius=["40%", "80%"],
                minRadius=0, maxRadius=None,
                center=["40%", "60%"])

                .add(
                "",
                (days_pyecharts_dataframe_data[i]),
                radius=["40%", "70%"],  # 饼状图内外半径
                label_opts=opts.LabelOpts(
                    position='outside',  # 标签位置

                ),
            )
        )
        tl.add(pie, f"{days_pyecharts_dataframe_time[i]}")
    return tl


def days_pyecharts_pie_conversion_business(data_frame):
    # pdb.set_trace()  # 调试模块

    days_conversion_time = data_frame['日期']
    selected_keys = ['UV总和', '客户数总和', 'UV客户转化率']
    days_conversion_zip = [list(i) for i in zip(data_frame.loc[:, selected_keys].columns.tolist(),
                                                *data_frame.loc[:, selected_keys].values.tolist())]
    days_pyecharts_dataframe_data = days_pyecharts_data_list(data_frame=days_conversion_zip)

    tl = (
        Timeline(init_opts=opts.InitOpts(
            theme=ThemeType.DARK
        )
        )
            .add_schema(
            is_auto_play=True,
            play_interval=1500)
    )
    for i in range(len(days_conversion_time)):
        pie = (
            Pie()
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{days_conversion_time[0]}~{days_conversion_time.iloc[-1]}\n转化率",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=12)
                ),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="0.1%", pos_left="70%"),
            )
                .set_series_opts(
                label_opts=opts.LabelOpts(is_show=True),
                minAngle=1,
                radius=["40%", "80%"],
                minRadius=0, maxRadius=None,
                center=["40%", "60%"])

                .add(
                "",
                (days_pyecharts_dataframe_data[i]),
                radius=["40%", "70%"],  # 饼状图内外半径
                label_opts=opts.LabelOpts(
                    position='outside',  # 标签位置

                ),
            )
        )
        tl.add(pie, f"{days_conversion_time[i]}")
    return tl


def days_pyecharts_pie_upp_business(data_frame):
    days_pyecharts_time = data_frame['日期']
    days_pyecharts_bussiness_zip = [list(i) for i in zip(data_frame.loc[:, summ_keys[5:]].columns.tolist(),
                                                         *data_frame.loc[:, summ_keys[5:]].values.tolist()
                                                         )]
    days_pyecharts_dataframe_data = days_pyecharts_data_list(data_frame=days_pyecharts_bussiness_zip)

    tl = (
        Timeline(init_opts=opts.InitOpts(
            theme=ThemeType.DARK
        )
        )
            .add_schema(
            is_auto_play=True,
            play_interval=1500)
    )
    for i in range(len(days_pyecharts_time)):
        pie = (
            Pie()
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{days_pyecharts_time[0]}~{days_pyecharts_time.iloc[-1]}\n转化率",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=12)
                ),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="0.1%", pos_left="70%"),
            )
                .set_series_opts(
                label_opts=opts.LabelOpts(is_show=True),
                minAngle=1,
                radius=["40%", "80%"],
                minRadius=0, maxRadius=None,
                center=["40%", "60%"])

                .add(
                "",
                (days_pyecharts_dataframe_data[i]),
                radius=["40%", "70%"],  # 饼状图内外半径
                label_opts=opts.LabelOpts(
                    position='outside',  # 标签位置

                ),
            )
        )
        tl.add(pie, f"{days_pyecharts_time[i]}")
    return tl


def days_pyecharts_pie_cnu_business(data_frame):
    days_pyecharts_time = data_frame['日期']
    sum_keys = ['客户数总和', 'UV客户转化率', '平均单价']
    days_pyecharts_bussiness_zip = [list(i) for i in zip(data_frame.loc[:, sum_keys].columns.tolist(),
                                                         *data_frame.loc[:, sum_keys].values.tolist()
                                                         )]
    days_pyecharts_dataframe_data = days_pyecharts_data_list(data_frame=days_pyecharts_bussiness_zip)

    tl = (
        Timeline(init_opts=opts.InitOpts(
            theme=ThemeType.DARK
        )
        )
            .add_schema(
            is_auto_play=True,
            play_interval=1500)
    )
    for i in range(len(days_pyecharts_time)):
        pie = (
            Pie()
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{days_pyecharts_time[0]}~{days_pyecharts_time.iloc[-1]}\n转化率",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=12)
                ),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="0.1%", pos_left="70%"),
            )
                .set_series_opts(
                label_opts=opts.LabelOpts(is_show=True),
                minAngle=1,
                radius=["40%", "80%"],
                minRadius=0, maxRadius=None,
                center=["40%", "60%"])

                .add(
                "",
                (days_pyecharts_dataframe_data[i]),
                radius=["40%", "70%"],  # 饼状图内外半径
                label_opts=opts.LabelOpts(
                    position='outside',  # 标签位置

                ),
            )
        )
        tl.add(pie, f"{days_pyecharts_time[i]}")
    return tl


'''销售品类柱形图可视化方法'''


def days_pyecharts_bar_category(data_frame):
    # pdb.set_trace()  # 调试模块
    days_columns = list(data_frame.iloc[:, 1:].columns)
    days_times = data_frame['日期']

    bar = (
        Bar(
            init_opts=opts.InitOpts(chart_id='oneday_pyecharts_one')
        )
            .add_xaxis([days_times[i] for i in range(len(days_times))])
    )
    for col in days_columns:
        bar.add_yaxis(col, data_frame[col].tolist())

    bar.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"{days_times[0]}~{days_times.iloc[-1]}日经品类销售可视化",
            title_textstyle_opts=opts.TextStyleOpts(font_style=25),
            pos_right='30%',
            pos_top='0.1%'
        ),
        xaxis_opts=opts.AxisOpts(type_='category', name='日期'),
        tooltip_opts=opts.TooltipOpts(trigger='axis'),
        legend_opts=opts.LegendOpts(pos_right='0.01%',
                                    pos_top='12%',
                                    orient='vertical',
                                    textstyle_opts=opts.TextStyleOpts(
                                        font_size=7,
                                    ),
                                    ),
        datazoom_opts=opts.DataZoomOpts(is_show=True, pos_right='10%', pos_top='90%'),
        toolbox_opts=toolbox_opts,
    )
    return bar


'''销售品类可视化附图饼形图'''


def dyas_pyecharts_pie_categouy_onehunderd(data_frame):
    # pdb.set_trace()  # 调试模块
    days_times = data_frame['日期']
    categouy_df_data = data_frame.iloc[:, 1:].stack()[lambda x: x > 100].reset_index()
    result = categouy_df_data.groupby('level_0').apply(lambda x: x[['level_1', 0]].values.tolist()).tolist()

    tl = (
        Timeline(init_opts=opts.InitOpts(
            theme=ThemeType.DARK
        )
        )
            .add_schema(
            is_auto_play=True,
            play_interval=1500)
    )
    for i in range(len(days_times)):
        pie = (
            Pie()
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{days_times[0]}~{days_times.iloc[-1]}\n大于100件",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=12)
                ),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="0.1%", pos_left="70%"),
            )
                .set_series_opts(
                label_opts=opts.LabelOpts(is_show=True),
                minAngle=1,
                radius=["40%", "80%"],
                minRadius=0, maxRadius=None,
                center=["40%", "60%"])

                .add(
                "",
                (result[i]),
                radius=["40%", "70%"],  # 饼状图内外半径
                label_opts=opts.LabelOpts(
                    position='outside',  # 标签位置

                ),
            )
        )
        tl.add(pie, f"{days_times[i]}")
    return tl


def dyas_pyecharts_pie_categouy_towhunderd(data_frame):
    # pdb.set_trace()  # 调试模块
    days_times = data_frame['日期']
    categouy_df_data = data_frame.iloc[:, 1:].stack()[lambda x: (x >= 50) & (x <= 100)].reset_index()
    result = categouy_df_data.groupby('level_0').apply(lambda x: x[['level_1', 0]].values.tolist()).tolist()
    tl = (
        Timeline(init_opts=opts.InitOpts(
            theme=ThemeType.DARK
        )
        )
            .add_schema(
            is_auto_play=True,
            play_interval=1500)
    )
    for i in range(len(days_times)):
        pie = (
            Pie()
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{days_times[0]}~{days_times.iloc[-1]}\n小于100大于50",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=12)
                ),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="0.1%", pos_left="70%"),
            )
                .set_series_opts(
                label_opts=opts.LabelOpts(is_show=True),
                minAngle=1,
                radius=["40%", "80%"],
                minRadius=0, maxRadius=None,
                center=["40%", "60%"])

                .add(
                "",
                (result[i]),
                radius=["40%", "70%"],  # 饼状图内外半径
                label_opts=opts.LabelOpts(
                    position='outside',  # 标签位置

                ),
            )
        )
        tl.add(pie, f"{days_times[i]}")
    return tl


def dyas_pyecharts_pie_categouy_threehunderd(data_frame):
    # pdb.set_trace()  # 调试模块
    days_times = data_frame['日期']
    categouy_df_data = data_frame.iloc[:, 1:].stack()[lambda x: x < 50].reset_index()
    result = categouy_df_data.groupby('level_0').apply(lambda x: x[['level_1', 0]].values.tolist()).tolist()

    tl = (
        Timeline(init_opts=opts.InitOpts(
            theme=ThemeType.DARK
        )
        )
            .add_schema(
            is_auto_play=True,
            play_interval=1500)
    )
    for i in range(len(days_times)):
        pie = (
            Pie()
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{days_times[0]}~{days_times.iloc[-1]}\n小于50",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=12)
                ),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="0.1%", pos_left="70%"),
            )
                .set_series_opts(
                label_opts=opts.LabelOpts(is_show=True),
                minAngle=1,
                radius=["40%", "80%"],
                minRadius=0, maxRadius=None,
                center=["40%", "60%"])

                .add(
                "",
                (result[i]),
                radius=["40%", "70%"],  # 饼状图内外半径
                label_opts=opts.LabelOpts(
                    position='outside',  # 标签位置

                ),
            )
        )
        tl.add(pie, f"{days_times[i]}")
    return tl


def dyas_pyecharts_pie_categouy_fourhunderd(data_frame):
    # pdb.set_trace()  # 调试模块
    days_times = data_frame['日期']
    categouy_df_data = data_frame.columns[1:]  # 除去日期列
    data_frame[categouy_df_data] = (data_frame[categouy_df_data].div(data_frame['销售总量'], axis=0) * 100).round(
        2)  # 计算百分比
    data_frame_zip = data_frame.iloc[:, 2:].stack().reset_index()  # 对数据进行打标为数据分组做数据准备

    data_frame_list = data_frame_zip.groupby('level_0').apply(
        lambda x: x[['level_1', 0]].values.tolist()).tolist()  # 完成数据是一个嵌套列表类数据

    tl = (
        Timeline(init_opts=opts.InitOpts(
            theme=ThemeType.DARK
        )
        )
            .add_schema(
            is_auto_play=True,
            play_interval=1500)
    )
    for i in range(len(days_times)):
        pie = (
            Pie()
                .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=f"{days_times[0]}~{days_times.iloc[-1]}\n销售量百分比",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=12)
                ),
                legend_opts=opts.LegendOpts(orient="vertical", pos_top="0.1%", pos_left="80%",
                                            textstyle_opts=opts.TextStyleOpts(font_size=12))
            )
                .set_series_opts(
                label_opts=opts.LabelOpts(is_show=True),
                minAngle=1,
                radius=["40%", "80%"],
                minRadius=0, maxRadius=None,
                center=["40%", "60%"])

                .add(
                "",
                (data_frame_list[i]),
                radius=["40%", "70%"],  # 饼状图内外半径
                label_opts=opts.LabelOpts(
                    position='outside',  # 标签位置

                ),
            )
        )
        tl.add(pie, f"{days_times[i]}")
    return tl
