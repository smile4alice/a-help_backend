from ahelp.admin.common import AdminModelView


class FeedbackAdminModelView(AdminModelView):
    column_list = [
        "name",
        "number",
        "mail",
        "message",
        "date",
    ]
    column_labels = {
        "name": "Ім'я",
        "number": "Мобільний",
        "mail": "e-mail",
        "message": "Повідомлення",
        "date": "Дата отримання",
    }
    column_descriptions = dict(
        name="Ім'я користувача, вказане у формі зворотного зв'язку.",
        number="Номер користувача для зворотнього зв'язку",
        mail="Пошта для зворотнього звязку. Буде вказана в полі'Отримувач' при відправці зворотнього листа з Вашої пошти.",
        message="Повідомлення від відвідувача.",
        date="Дата і час отримання повідомлення",
    )
    column_searchable_list = [
        "name",
        "number",
        "mail",
    ]
    column_export_exclude_list = ["date"]
    column_default_sort = [("date", True)]
    can_set_page_size = True
    can_view_details = True
    details_modal = True
    can_export = True
    export_types = [
        "csv",
        "xls",
        "xlsx",
        "json",
        "yaml",
        "html",
    ]
    can_edit = False
    list_template = "admin/details_button.html"
    column_formatters = {"date": lambda view, context, model, name: model.date.strftime("%d %B %Y %H:%M:%S")}

    def render(self, template, **kwargs):
        kwargs[
            "description"
        ] = """<ul><li>Ви не можете редагувати повідомлення, проте можете
                                   їх переглядати, натиснувши відповідну кнопку зліва,
                                   напроти відповідного запису.</li> <li>У вас є можливість
                                   завантажити всі данні з цієї таблиці, натиснувши
                                   кнопку "Зберегти" та обравши потрібний формат файлу.
                                   Файл з данними буде збережено у відповідному форматі
                                   на вашому комп'ютері.</li></ul>"""
        return super(FeedbackAdminModelView, self).render(template, **kwargs)
