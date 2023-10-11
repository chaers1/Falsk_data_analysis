'''数据分析模块文件'''

import pandas as pd
from core.utility import parse_date_string
from core.models import Table
from sqlalchemy import and_

'''数据读取方法'''


def commerce(data):
    '''

    :param data: 数据分析文件
    :return: 返回数据显示文件
    '''
    commerce_df = pd.read_excel(data)
    return commerce_df


'''单日数据获取查询清洗转换数据库中的数据为pandas数据格式，为接下来的数据分析做准备'''


def get_single_day_data(analysis_route_single):
    '''

    :param analysis_route_single: 转换完成的日期类数据
    :return: 返回一个pandas数据格式
    '''
    # 解析日期字符串为日期对象
    analysis_route_parse = parse_date_string(date_str=analysis_route_single)

    # 查询特定日期的数据
    single_day_data = Table.query.filter_by(sale_data=analysis_route_parse).all()  # 数据库获取指定日期的数据

    # 创建数据字典列表
    data_dict_list = [{'货号': row.produtc_code, '日期': row.sale_data, '客户数': row.customer_counts,
                       '销售额': row.tltal_sales, '销售量（含拒退）': row.total_quantity,
                       '销售额（扣满减含拒退）': row.sales_after_discount, 'UV': row.uv,
                       '转化率': row.conversion_rate, '商品CTR': row.product_ctr,
                       '曝光UV': row.exposure_uv, '款号辅助': row.style_code_auxiliary,
                       '销售区间': row.sales_range, '品类': row.category, '活动': row.activity,
                       '到手价': row.net_price, '到手价区间': row.net_price_range
                       } for row in single_day_data]

    # 转换为Pandas DataFrame
    df = pd.DataFrame(data_dict_list)

    return df


'''单日经营数据分析类型/品类数据销售类型'''


def Get_fenxi_day_data(dataframe):
    '''

    :param Day_input_data: 数据库按照日期抽取的文件
    :return:
    '''
    data_time = dataframe['日期'].iloc[0]
    buv_sum = round(dataframe['曝光UV'].sum(), 2)
    uv_sum = dataframe['UV'].sum()
    ctr_sp = (uv_sum / buv_sum) * 100
    kh_sum = dataframe['客户数'].sum()
    kh_uv = (kh_sum / uv_sum) * 100
    xse_sum = dataframe['销售额'].sum()
    xsl_sum = dataframe['销售量（含拒退）'].sum()
    ping_dan_jian = xse_sum / xsl_sum

    result_dict = {
        '日期': data_time,
        '曝光UV总和': buv_sum,
        'UV总和': uv_sum,
        'CTR': ctr_sp,
        '客户数总和': kh_sum,
        'UV客户转化率': kh_uv,
        '销售额总和': xse_sum,
        '销售量总和': xsl_sum,
        '平均单价': ping_dan_jian,
    }

    '''品类销售代码'''
    commerce_grupds = dataframe.groupby(['品类'])['销售量（含拒退）'].sum().reset_index()  # 统计每个品类的销售量
    commerce_grupds_sum = commerce_grupds.sum()

    # 创建一个包含销售总量的字典
    category_data = {
        '销售总量': commerce_grupds_sum['销售量（含拒退）'],
        **commerce_grupds.set_index('品类').to_dict()['销售量（含拒退）']  # 这里需要重点理解
    }

    # 转换成 DataFrame
    pinlei_df = pd.DataFrame([category_data])
    pinlei_df.insert(0, '日期', data_time)

    result_df = pd.DataFrame.from_dict([result_dict])
    return result_df, pinlei_df


'''多日数据分析数据库获取数据'''


def Multi_data_analysis(start_data, ene_data):
    '''转换时间格式操作'''
    start_route_multi = parse_date_string(date_str=start_data)
    end_route_multi = parse_date_string(date_str=ene_data)
    '''数据库查询操作'''
    filtered_data = Table.query.filter(
        and_(Table.sale_data >= start_route_multi, Table.sale_data <= end_route_multi)).all()
    '''将查询到的数据进行数据匹配'''
    data_dict_list = [{'货号': row.produtc_code, '日期': row.sale_data, '客户数': row.customer_counts,
                       '销售额': row.tltal_sales, '销售量（含拒退）': row.total_quantity,
                       '销售额（扣满减含拒退）': row.sales_after_discount, 'UV': row.uv,
                       '转化率': row.conversion_rate, '商品CTR': row.product_ctr,
                       '曝光UV': row.exposure_uv, '款号辅助': row.style_code_auxiliary,
                       '销售区间': row.sales_range, '品类': row.category, '活动': row.activity,
                       '到手价': row.net_price, '到手价区间': row.net_price_range
                       } for row in filtered_data]
    df = pd.DataFrame(data_dict_list)
    return df


'''获取到的多日数据分析模块'''


def multi_data_analysis_duori(data_frame):
    dataframe = data_frame.groupby('日期')
    result_list = []  # 创建一个实例用于存储迭代的数据
    result_list_pinlei = []

    for date, group in dataframe:
        metrics = {
            '日期': group['日期'].iloc[0],
            '曝光UV': round(group['曝光UV'].sum(), 2),
            'UV总和': group['UV'].sum(),
            'CTR': round(group['UV'].sum() / group['曝光UV'].sum() * 100, 2),
            '客户数总和': group['客户数'].sum(),
            'UV客户转化率': round((group['客户数'].sum() / group['UV'].sum()) * 100, 2),
            '销售额总和': group['销售额'].sum(),
            '销售量总和': group['销售量（含拒退）'].sum(),
            '平均单价': round(group['销售额'].sum() / group['销售量（含拒退）'].sum(), 2),
        }
        result_list.append(metrics)

        data_time = group['日期'].iloc[0]
        commerce_grupds = group.groupby(['品类'])['销售量（含拒退）'].sum().reset_index()  # 统计每个品类的销售量
        commerce_grupds_sum = commerce_grupds.sum()  # 销售总量
        result_dict = {
            '日期': data_time,
            '销售总量': commerce_grupds_sum['销售量（含拒退）'],
        }
        result_dict.update(commerce_grupds.set_index('品类').to_dict()['销售量（含拒退）'])
        result_list_pinlei.append(result_dict)

    df = pd.DataFrame(result_list)
    df1 = pd.DataFrame(result_list_pinlei)

    return df, df1

