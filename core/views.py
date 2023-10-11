'''web程序flask路由文件'''
from core import app, db
from core.utility import Utility
from core.models import Admin, Table
from flask_login import login_user
from flask import render_template, request, url_for, redirect, flash

from core.data_fenxi import commerce, get_single_day_data, Get_fenxi_day_data, Multi_data_analysis, \
    multi_data_analysis_duori  # 数据分析方法模块

from core.day_danri_pyecharts import pyecharts_one_day, pyecharts_pinlei_oneday, pyecharts_one_day_pie, \
    conversion_pie, unit_price_of_pieces, percentage_ctr_conversion_unit, one_pinlei_pie, tow_pinlei_pie, \
    three_pinlei_pie, four_pinlei_pie  # 单日可视化

from core.many_day_pyecharts import days_pyecharts_bar, days_pyecharts_pie_ctr_business, \
    days_pyecharts_pie_conversion_business, days_pyecharts_pie_upp_business, \
    days_pyecharts_pie_cnu_business  # 多日经营可视化数据主图附图

from core.many_day_pyecharts import days_pyecharts_bar_category, dyas_pyecharts_pie_categouy_onehunderd, \
    dyas_pyecharts_pie_categouy_towhunderd, dyas_pyecharts_pie_categouy_threehunderd, \
    dyas_pyecharts_pie_categouy_fourhunderd

'''登录界面视图函数'''


@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur_users = Admin.query.filter(Admin.name == username).all()
        if cur_users:
            for cur_user in cur_users:
                if cur_user.validate_pwd(password):
                    login_user(cur_user)
                    flash('登入成功')
                    return redirect(url_for('base'))

        flash('账户名或密码不对，请核对账号密码，若未注册请先注册')
        return redirect(url_for('login'))

    return render_template('login.html')


'''注册界面视图函数'''


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['zusername']
        password = request.form['zpassword']

        if not username:
            flash('用户名不能为空')
            return redirect(url_for('register'))
        if not password:
            flash('密码不能为空')
            return redirect(url_for('register'))
        new_user = Admin(name=username, password=password, flasktime=Utility.get_cur_time())
        new_user.set_pwd(password)
        db.session.add(new_user)
        db.session.commit()
        flash_sx = '注册成功，点击返回登录'
        return render_template('index.html', flash_sx=flash_sx)
    return render_template('register.html')


'''主页视图函数'''


@app.route('/base', methods=['POST', 'GET'])
def base():
    return render_template('base.html')


'''数据管理视图函数'''


@app.route('/query', methods=['POST', 'GET'])
def query():
    # 数据获取
    if request.method == 'POST':
        upload_file = request.files['query-input-uploaded_file']
        action = request.form.get('action')

        if not upload_file:
            return "未选择上传文件"
        if not action:
            return "未指定操作"
        '''
        if:显示数据判断逻辑
        elif：数据存储判断逻辑
        '''
        if action == 'display':
            commerce_display = commerce(data=upload_file)
            commerce_biaoge_qiepian = commerce_display.loc[:, '货号':'到手价区间']
            html_table_display = commerce_biaoge_qiepian.to_html(classes='table table-striped')
            return render_template('query.html', html_table_display=html_table_display)

        elif action == 'save':
            commerce_biaoge = commerce(data=upload_file)  # pandas读取表格
            commerce_biaoge_qiepian = commerce_biaoge.loc[:, '货号':'到手价区间']
            commerce_biaoge_qiepian.fillna(value=0, inplace=True)

            selected_columns = {'货号': 'produtc_code',
                                '日期': 'sale_data',
                                '客户数': 'customer_counts',
                                '销售额': 'tltal_sales',
                                '销售量（含拒退）': 'total_quantity',
                                '销售额（扣满减含拒退）': 'sales_after_discount',
                                'UV': 'uv',
                                '转化率': 'conversion_rate',
                                '商品CTR': 'product_ctr',
                                '曝光UV': 'exposure_uv',
                                '款号辅助': 'style_code_auxiliary',
                                '销售区间': 'sales_range',
                                '品类': 'category',
                                '活动': 'activity',
                                '到手价': 'net_price',
                                '到手价区间': 'net_price_range'
                                }  # 映射表格
            commerce_biaoge_qiepian.rename(columns=selected_columns, inplace=True)  # 重命名表格对应数据库表格列
            try:
                num_rows_uploaded = 0
                for index, row in commerce_biaoge_qiepian.iterrows():
                    data_entry = Table(**row)
                    db.session.add(data_entry)
                    num_rows_uploaded += 1  # 每添加一行数据，增加计数器的值
                db.session.commit()
                return f'文件数据上传数据库成功,共上传了{num_rows_uploaded}行数据'
            except Exception as e:
                db.session.rollback()
                return f'错误：{str(e)}'

    return render_template('query.html')


'''数据分析视图函数'''


@app.route('/analysis', methods=['POST', 'GET'])
def analysis():
    html_table_display = None  # 用于单日数据分析表格的HTML
    html_table_display_pinlei = None
    html_table_display_duori = None  # 用于多日数据分析表格的HTML
    html_table_display_duori_pinlei = None
    if request.method == 'POST':
        analysis_route = request.form['analysis_type']
        # 单日数据分析
        if analysis_route == 'single_day':
            analysis_route_single = request.form.get('single_date')
            df_single_day_data = get_single_day_data(analysis_route_single)  # 数据清洗
            result_df, result_df_pinlei = Get_fenxi_day_data(dataframe=df_single_day_data)  # 数据分析

            html_table_display = result_df.to_html(classes='table table-striped')
            html_table_display_pinlei = result_df_pinlei.to_html(classes='table table-striped')


        # 多日数据分析
        elif analysis_route == 'multi_day':
            analysis_route_multi_start = request.form.get('start_date')
            analysis_route_multi_end = request.form.get('end_date')
            data_shili = Multi_data_analysis(start_data=analysis_route_multi_start,
                                             ene_data=analysis_route_multi_end)
            muler_duori, muler_duori_pinlei = multi_data_analysis_duori(data_frame=data_shili)
            html_table_display_duori = muler_duori.to_html(classes='table table-striped2')
            html_table_display_duori_pinlei = muler_duori_pinlei.to_html(classes='table table-striped2')

    return render_template('analysis.html',
                           html_table_display=html_table_display,
                           html_table_display_pinlei=html_table_display_pinlei,
                           html_table_display_duori=html_table_display_duori,
                           html_table_display_duori_pinlei=html_table_display_duori_pinlei)


'''数据可视化视图函数'''


@app.route('/visualization', methods=['POST', 'GET'])
def visualization():
    # 单日可视化图表变量
    pyecharts_bar_chart_html = None
    pyecharts_bar_chart_pinlei_html = None
    pyecharts_bar_chart_pie_html = None
    pyecharts_pie_conversion = None
    pyecharts_pie_unti = None
    html_table_display_percentage = None
    '''销售品类附图'''
    pyecharts_one_pinlei_pie = None
    pyecharts_tow_pinlei_pie = None
    pyecharts_three_pinlei_pie = None
    pyecharts_four_pinlei_pie = None
    '''多日经营数据可视化全局变量'''
    pyecharts_days_bar_business = None
    pyecharts_days_pie_business_one = None
    pyecharts_days_pie_business_tow = None
    pyecharts_days_pie_business_three = None
    pyecharts_days_pie_business_four = None
    '''多日品类销售可视化数据变量'''
    pyecharts_days_bar_category = None
    pyecharts_days_pie_category_one = None
    pyecharts_days_pie_category_tow = None
    pyecharts_days_pie_category_three = None
    pyecharts_days_pie_category_four = None
    '''单日期变量'''
    analysis_route_single = None
    '''多日日期变量'''
    analysis_route_multi_start = None
    analysis_route_multi_end = None

    if request.method == 'POST':
        analysis_route = request.form['analysis_type']
        # 单日可视化分析
        if analysis_route == 'single_day':
            analysis_route_single = request.form.get('single_date')
            df_single_duori_data = get_single_day_data(analysis_route_single)  # 数据清洗
            result_df = Get_fenxi_day_data(dataframe=df_single_duori_data)[0]
            pinlei_df = Get_fenxi_day_data(dataframe=df_single_duori_data)[1]  # 数据分析

            '''柱形图主图可视化'''
            pyecharts_bar_chart_html_oneday = pyecharts_one_day(data_frame=result_df)
            pyecharts_bar_chart_pinlei = pyecharts_pinlei_oneday(dataframe=pinlei_df)

            '''经营数据附图饼图'''
            pyecharts_bar_chart_pie = pyecharts_one_day_pie(data_frame=result_df)  # 经营数据饼图--附图
            pyecharts_pie_conversions = conversion_pie(data_frame=result_df)
            pyecharts_pie_untis = unit_price_of_pieces(data_frame=result_df)
            html_table_display_percentages = percentage_ctr_conversion_unit(data_frame=result_df)

            '''经营数据dunp生成'''
            pyecharts_bar_chart_html = pyecharts_bar_chart_html_oneday.dump_options()  # 经营数据主图
            pyecharts_bar_chart_pie_html = pyecharts_bar_chart_pie.dump_options()
            pyecharts_pie_conversion = pyecharts_pie_conversions.dump_options()
            pyecharts_pie_unti = pyecharts_pie_untis.dump_options()
            html_table_display_percentage = html_table_display_percentages.dump_options()

            '''销售品类附图饼图'''
            # pdb.set_trace()#调试模块
            pyecharts_one_pinlei_pies = one_pinlei_pie(data_frame=pinlei_df)
            pyecharts_tow_pinlei_pies = tow_pinlei_pie(data_frame=pinlei_df)
            pyecharts_three_pinlei_pies = three_pinlei_pie(data_frame=pinlei_df)
            pyecharts_four_pinlei_pies = four_pinlei_pie(data_frame=pinlei_df)

            '''销售品类dump生成'''
            pyecharts_bar_chart_pinlei_html = pyecharts_bar_chart_pinlei.dump_options()  # 销售数据饼图
            pyecharts_one_pinlei_pie = pyecharts_one_pinlei_pies.dump_options()
            pyecharts_tow_pinlei_pie = pyecharts_tow_pinlei_pies.dump_options()
            pyecharts_three_pinlei_pie = pyecharts_three_pinlei_pies.dump_options()
            pyecharts_four_pinlei_pie = pyecharts_four_pinlei_pies.dump_options()

            '''多日可视化分析'''
        elif analysis_route == 'multi_day':

            '''数据获取'''
            analysis_route_multi_start = request.form.get('start_date')
            analysis_route_multi_end = request.form.get('end_date')

            '''多日数据分析'''
            data_pyecharts_analysis = Multi_data_analysis(start_data=analysis_route_multi_start,
                                                          ene_data=analysis_route_multi_end)
            # pdb.set_trace()  # 调试模块
            muler_duori = multi_data_analysis_duori(data_frame=data_pyecharts_analysis)[0]
            muler_duori_pinlei = multi_data_analysis_duori(data_frame=data_pyecharts_analysis)[1]

            '''多日经营数据可视化柱形图'''
            days_pyecharts_bar_categoryhtml = days_pyecharts_bar(data_frame=muler_duori)
            days_pyecharts_pie_business_one_html = days_pyecharts_pie_ctr_business(data_frame=muler_duori)
            days_pyecharts_pie_business_tow_html = days_pyecharts_pie_conversion_business(data_frame=muler_duori)
            days_pyecharts_pie_business_three_html = days_pyecharts_pie_upp_business(data_frame=muler_duori)
            days_pyecharts_pie_business_four_html = days_pyecharts_pie_cnu_business(data_frame=muler_duori)

            '''经营数据dunp生成'''
            pyecharts_days_bar_business = days_pyecharts_bar_categoryhtml.dump_options()
            pyecharts_days_pie_business_one = days_pyecharts_pie_business_one_html.dump_options()
            pyecharts_days_pie_business_tow = days_pyecharts_pie_business_tow_html.dump_options()
            pyecharts_days_pie_business_three = days_pyecharts_pie_business_three_html.dump_options()
            pyecharts_days_pie_business_four = days_pyecharts_pie_business_four_html.dump_options()

            '''多日销售品类可视化柱形图'''
            pyecharts_days_bar_category_html = days_pyecharts_bar_category(data_frame=muler_duori_pinlei)

            '''多日品类销售可视化附图饼形图'''
            pyecharts_days_pie_category_one_html = dyas_pyecharts_pie_categouy_onehunderd(data_frame=muler_duori_pinlei)
            pyecharts_days_pie_category_tow_html = dyas_pyecharts_pie_categouy_towhunderd(data_frame=muler_duori_pinlei)
            pyecharts_days_pie_category_three_html = dyas_pyecharts_pie_categouy_threehunderd(
                data_frame=muler_duori_pinlei)
            pyecharts_days_pie_category_four_html = dyas_pyecharts_pie_categouy_fourhunderd(
                data_frame=muler_duori_pinlei)

            '''销售品类数据dunp生成'''
            pyecharts_days_bar_category = pyecharts_days_bar_category_html.dump_options()
            pyecharts_days_pie_category_one = pyecharts_days_pie_category_one_html.dump_options()
            pyecharts_days_pie_category_tow = pyecharts_days_pie_category_tow_html.dump_options()
            pyecharts_days_pie_category_three = pyecharts_days_pie_category_three_html.dump_options()
            pyecharts_days_pie_category_four = pyecharts_days_pie_category_four_html.dump_options()
    return render_template('visualization.html',
                           # 单日可视化
                           pyecharts_bar_chart_html=pyecharts_bar_chart_html,
                           pyecharts_bar_chart_pinlei_html=pyecharts_bar_chart_pinlei_html,
                           pyecharts_bar_chart_pie_html=pyecharts_bar_chart_pie_html,
                           pyecharts_pie_conversion=pyecharts_pie_conversion,
                           pyecharts_pie_unti=pyecharts_pie_unti,
                           html_table_display_percentage=html_table_display_percentage,
                           pyecharts_one_pinlei_pie=pyecharts_one_pinlei_pie,
                           pyecharts_tow_pinlei_pie=pyecharts_tow_pinlei_pie,
                           pyecharts_three_pinlei_pie=pyecharts_three_pinlei_pie,
                           pyecharts_four_pinlei_pie=pyecharts_four_pinlei_pie,
                           # 单日日期传入
                           analysis_route_single=analysis_route_single,
                           # 多日可视化
                           pyecharts_days_bar_business=pyecharts_days_bar_business,
                           pyecharts_days_pie_business_one=pyecharts_days_pie_business_one,
                           pyecharts_days_pie_business_tow=pyecharts_days_pie_business_tow,
                           pyecharts_days_pie_business_three=pyecharts_days_pie_business_three,
                           pyecharts_days_pie_business_four=pyecharts_days_pie_business_four,
                           pyecharts_days_bar_category=pyecharts_days_bar_category,
                           pyecharts_days_pie_category_one=pyecharts_days_pie_category_one,
                           pyecharts_days_pie_category_tow=pyecharts_days_pie_category_tow,
                           pyecharts_days_pie_category_three=pyecharts_days_pie_category_three,
                           pyecharts_days_pie_category_four=pyecharts_days_pie_category_four,

                           # 多日日期传递
                           analysis_route_multi_start=analysis_route_multi_start,
                           analysis_route_multi_end=analysis_route_multi_end
                           )


'''退出登录视图函数'''


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if request.method == 'POST':
        return render_template('login.html')


'''本项目与2023年9月27好完成'''
