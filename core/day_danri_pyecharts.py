'''单日数据可视化分析代码模块'''
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
import pdb

'''pyecharts--toolbox_opts配置参数'''

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
summ_keys = ['曝光UV总和', 'UV总和', 'CTR', '客户数总和', 'UV客户转化率', '销售额总和', '销售量总和', '平均单价']


def pyecharts_one_day(data_frame):
    '''
    单日数据分析可视化--整体数据分析
    :param data_frame: 单日数据分析数据文件
    :return:
    '''

    oneday_time = data_frame['日期'].tolist()
    bar = (
        Bar(
            init_opts=opts.InitOpts(chart_id='oneday_pyecharts_one')
        )
            .add_xaxis(oneday_time)
    )
    for col in summ_keys:
        bar.add_yaxis(col, data_frame[col].tolist())
    bar.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"{oneday_time}日经营数据可视化",
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


''' 经营数据附图（饼图）'''


def pyecharts_one_day_pie(data_frame):
    '''

    :param data_frame: 分析完成的数据进行数据分析
    :return:
    '''
    one_pie_data = data_frame.columns[1:4]  # 获取标签
    one_pie_values = data_frame.iloc[:, 1:4].values.tolist()  # 获取数据
    nestd_list = [list(x) for x in zip(one_pie_data, *one_pie_values)]

    pie = (
        Pie()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="CTR数据"),
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
            (nestd_list),
            radius=["40%", "70%"],  # 饼状图内外半径
            label_opts=opts.LabelOpts(
                position='outside',  # 标签位置

            ),
        )
    )

    return pie


'''转化率函饼形图方法'''


def conversion_pie(data_frame):
    # 获取数据
    ion_list = ['UV总和', '客户数总和', 'UV客户转化率']
    ion_pie_colums = data_frame.columns[data_frame.columns.isin(ion_list)]
    ion_pie_values = data_frame[ion_list].values.tolist()
    # 整理数据
    ion_pie_zip = [list(i) for i in zip(ion_pie_colums, *ion_pie_values)]
    pie = (
        Pie()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="转化率"),
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
            (ion_pie_zip),
            radius=["40%", "70%"],  # 饼状图内外半径
            label_opts=opts.LabelOpts(
                position='outside',  # 标签位置

            ),
        )
    )

    return pie


'''件单价附图'''


def unit_price_of_pieces(data_frame):
    # 获取数据
    unit_list = ['销售额总和', '销售量总和', '平均单价']
    unit_columns = data_frame.columns[data_frame.columns.isin(unit_list)]
    unit_values = data_frame[unit_list].values.tolist()

    # 整理数据
    unit_zip = [list(i) for i in zip(unit_columns, *unit_values)]
    pie = (
        Pie()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="件单价"),
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
            (unit_zip),
            radius=["40%", "70%"],  # 饼状图内外半径
            label_opts=opts.LabelOpts(
                position='outside',  # 标签位置

            ),
        )
    )

    return pie


'''ctr，转化率，件单价'''


def percentage_ctr_conversion_unit(data_frame):
    # 获取数据
    percentage_list = ["CTR", "UV客户转化率", "平均单价"]
    percentage_columns = data_frame.columns[data_frame.columns.isin(percentage_list)]
    percentage_values = data_frame[percentage_list].values.tolist()
    # 处理数据
    percentage_zip = [list(i) for i in zip(percentage_columns, *percentage_values)]
    pie = (
        Pie()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="CTR,转化率，件单价"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="45%", pos_left="70%"),
        )
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True),
            minAngle=1,
            radius=["40%", "80%"],
            minRadius=0, maxRadius=None,
            center=["40%", "60%"])

            .add(
            "",
            (percentage_zip),
            radius=["40%", "70%"],  # 饼状图内外半径
            label_opts=opts.LabelOpts(
                position='outside',  # 标签位置

            ),
        )
    )
    return pie


'''单日数据销售品类可视化函数'''


def pyecharts_pinlei_oneday(dataframe):
    '''

    :param dataframe: 单日销售品类数据集
    :return:
    '''
    oneday_pinlei = list(dataframe.iloc[:, 1:].columns)
    oneday_time = dataframe['日期'].tolist()
    bar_pinlei = (
        Bar(
            init_opts=opts.InitOpts(chart_id='oneday_pyecharts_one')
        )
            .add_xaxis(oneday_time)
    )
    for col in oneday_pinlei:
        bar_pinlei.add_yaxis(col, dataframe[col].tolist())
    bar_pinlei.set_global_opts(
        title_opts=opts.TitleOpts(
            title=f"{oneday_time}日经品类销售数据可视化",
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
    return bar_pinlei


'''单日销售品类可视化附图-pie'''


def one_pinlei_pie(data_frame):
    # pdb.set_trace()#调试模块

    pinlei_df_data = data_frame[list(data_frame.iloc[:, 1:].columns)].stack().reset_index(level=0, drop=True)[
        lambda x: x > 100]
    pinlei_df_indes = pinlei_df_data.index.tolist()
    pinlei_df_values = pinlei_df_data.values.tolist()
    pinlei_df_zip = [list(i) for i in zip(pinlei_df_indes, pinlei_df_values)]
    pie = (
        Pie()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="高于100件"),
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
            (pinlei_df_zip),
            radius=["40%", "70%"],  # 饼状图内外半径
            label_opts=opts.LabelOpts(
                position='outside',  # 标签位置

            ),
        )
    )
    return pie


def tow_pinlei_pie(data_frame):
    # pdb.set_trace()  # 调试模块

    pinlei_df_data = data_frame[list(data_frame.iloc[:, 1:].columns)].stack().reset_index(level=0, drop=True)[
        lambda x: (x >= 50) & (x <= 100)]
    pinlei_df_index = pinlei_df_data.index.tolist()
    pinlei_df_values = pinlei_df_data.values.tolist()
    pinlei_df_zip = [list(i) for i in zip(pinlei_df_index, pinlei_df_values)]

    pie = (
        Pie()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="销售低于100件"),
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
            (pinlei_df_zip),
            radius=["40%", "70%"],  # 饼状图内外半径
            label_opts=opts.LabelOpts(
                position='outside',  # 标签位置

            ),
        )
    )
    return pie


def three_pinlei_pie(data_frame):
    pinlei_df_data = data_frame[list(data_frame.iloc[:, 1:].columns)].stack().reset_index(level=0, drop=True)[
        lambda x: x < 50]
    pinlei_df_index = pinlei_df_data.index.tolist()
    pinlei_df_values = pinlei_df_data.values.tolist()
    pinlei_df_zip_therr = [list(i) for i in zip(pinlei_df_index, pinlei_df_values)]

    pie = (
        Pie()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="销售低于50件"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="0.1%", pos_left="80%"),
        )
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True),
            minAngle=1,
            radius=["40%", "80%"],
            minRadius=0, maxRadius=None,
            center=["40%", "60%"])

            .add(
            "",
            (pinlei_df_zip_therr),
            radius=["40%", "70%"],  # 饼状图内外半径
            label_opts=opts.LabelOpts(
                position='outside',  # 标签位置

            ),
        )
    )
    return pie


def four_pinlei_pie(data_frame):
    # pdb.set_trace()  # 调试模块

    data_frame_columns = data_frame.iloc[:, 2:].columns.tolist()  # 获取索引
    data_frame_amount_to = data_frame.iloc[0, 1]  # 获取销售总量
    data_frame_values = data_frame[data_frame_columns].values.tolist()  # 获取索引值
    data_frame_percentage = [(round((value / data_frame_amount_to) * 100, 2)) for value in data_frame_values[0]]
    data_frame_four_zip = [list(i) for i in zip(data_frame_columns,data_frame_percentage)]

    pie = (
        Pie()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="销售量百分比"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="0.1%", pos_left="80%"),
        )
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True),
            minAngle=1,
            radius=["40%", "80%"],
            minRadius=0, maxRadius=None,
            center=["40%", "60%"])

            .add(
            "",
            (data_frame_four_zip),
            radius=["40%", "70%"],  # 饼状图内外半径
            label_opts=opts.LabelOpts(
                position='outside',  # 标签位置

            ),
        )
    )
    return pie
