from flask import Flask, render_template, request, jsonify
import config
from exts import db, fetch_data, fetch_week, time_desc
from models import OfficeModel, OrderModel
import time
import flask_whooshalchemyplus

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
flask_whooshalchemyplus.init_app(app)

app.jinja_env.variable_start_string = '{{ '
app.jinja_env.variable_end_string = ' }}'


with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():

    weeks = fetch_week()
    # 办公室信息
    get_office = request.args.get('office')
    office = OfficeModel.query.filter(get_office == OfficeModel.name).first()

    all_offices = OfficeModel.query.all()
    offices = [x.desc for x in all_offices]
    if office:
        office_desc = office.desc
    else:
        office_desc = '五味子'

    results = fetch_data()

    return render_template('date_picker.html', time_span=results, weeks=weeks, offices=offices, select_office=office_desc)


@app.route('/canSelect/')
def can_select():

    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    week = int(request.args.get('week'))
    office = request.args.get('office')

    ordered = ordered_time(office, week)

    new_orders = []
    for aOrder in ordered:
        new_orders.extend(range(aOrder.order_from, aOrder.order_to))

    select_range = list(range(start, end))

    inter = set(select_range).intersection(set(new_orders))
    if len(inter) > 0:
        return "false"
    else:
        return "true"


@app.route('/search/')
def search():
    search_text = request.args.get('query')
    orderes = OrderModel.query.whoosh_search(search_text).all()
    ordered = order_convert(orderes)
    return render_template('order_list.html', ordered=ordered)



@app.route('/orderlist/')
def order_list():
    orderes = OrderModel.query.all()
    ordered = order_convert(orderes)
    return render_template('order_list.html', ordered=ordered)


def order_convert(orders):
    ordered = []
    for order in orders:
        ord_convert = order.to_dict()
        ord_convert['time_desc'] = time_desc(order.order_from, order.order_to + 1, order.order_day)
        ordered.append(ord_convert)
    return ordered


# 获取已被选择的内容
@app.route('/getOrdered/')
def get_ordered():
    office = request.args.get('office')
    week = request.args.get('week')
    ordered = ordered_time(office, int(week))
    order_json = jsonify({'data': [x.to_dict() for x in ordered]})
    return order_json


@app.route('/submit/', methods=['POST'])
def submit():
    user_name = request.form.get('user_name')
    user_depart = request.form.get('user_depart')
    reason = request.form.get('reason')
    start_hour = request.form.get('start_hour')
    end_hour = request.form.get('end_hour')
    select_week = request.form.get('select_week', '0')
    office = request.form.get('office').strip()

    office_model = OfficeModel.query.filter(OfficeModel.desc == office).first()
    if not office_model:
        return '未能查到办公室' + '"' + office + '"'

    new_order = OrderModel(user_name=user_name,depart_name=user_depart,reason=reason,order_from=start_hour, order_to=end_hour, office_id=office_model.id)
    new_order.order_day = time_offset(select_week)
    db.session.add(new_order)
    db.session.commit()

    flask_whooshalchemyplus.index_one_model(OrderModel)
    return ''


# 管理页面
@app.route('/manage/')
def manage():
    return render_template('office_manage.html')


@app.route('/addOffice/', methods=['POST'])
def add_office():
    name = request.form.get('name')
    desc = request.form.get('desc')

    same_names = OfficeModel.query.filter(OfficeModel.name == name).all()
    if same_names:
        return '存在同名name:{},放弃添加'.format(name)

    same_descs = OfficeModel.query.filter(OfficeModel.desc == desc).all()
    if same_descs:
        return '存在同名desc:{},放弃添加'.format(name)

    office1 = OfficeModel(name=name, desc=desc)
    db.session.add(office1)
    db.session.commit()
    return ''


# 获取偏移后的时间戳
def time_offset(select):
    offset = int(select) * 86400
    return offset + int(time.time())


# 获取某一天的时间戳差
def time_duration(offset):
    cur_time = time.time()
    start = cur_time - cur_time % 86400 + 86400 * offset
    return [start, start + 86400]


# 获取某天的预订信息
def ordered_time(office, week):

    office_model = OfficeModel.query.filter(OfficeModel.desc == office.strip()).first()
    if not office_model:
        return []

    duration = time_duration(int(week))
    ordered = OrderModel.query.filter((OrderModel.office_id == office_model.id) & (OrderModel.order_day > duration[0]) & (OrderModel.order_day <= duration[1])).all()
    return ordered


if __name__ == '__main__':
    app.run()




