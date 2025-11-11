# coding:utf-8
from flask import Flask,render_template
from flask_cors import CORS

def create_app():
    """
    创建flask应用对象
    :param config_name: str 配置模式的名称 ("develop","product")
    :return:
    """

    app = Flask(__name__, template_folder='templates')

    CORS(app, resource={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def index():
        return render_template("index.html")

    # 注册蓝图
    from app import api
    app.register_blueprint(api.api, url_prefix="/api")

    return app