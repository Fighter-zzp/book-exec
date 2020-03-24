# 简单的flask书本案例
1. 配置数据库
    * 导入SQLAlchemy扩展
    * 创建db对象, 并配置参数
    * 终端创建数据库
2. 添加书和作者模型
    * 模型继承db.Model
    * __tablename__:表名
    * db.Column:字段
    * db.relationship: 关系引用
3. 添加数据
4. 使用模板显示数据库查询的数据
    * 查询所有的作者信息, 让信息传递给模板
    * 模板中按照格式, 依次for循环作者和书籍即可 (作者获取书籍, 用的是关系引用)
5. 使用WTF显示表单
    * 自定义表单类
    * 模板中显示
    * secret_key / 编码 / csrf_token
6. 实现相关的增删逻辑
    * 增加数据
    * 删除书籍  url_for的使用 /  for else的使用 / redirect的使用
    * 删除作者 
