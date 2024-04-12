import flask_login as login
from ahelp.admin.common import AdminModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.base import expose
from flask import redirect, abort
from flask_admin._compat import urljoin, quote


class CustomFileAdmin(FileAdmin):
    """File System admin."""

    def is_accessible(self):
        self.extra_css = AdminModelView.extra_css
        return login.current_user.is_authenticated

    @expose("/download/<path:path>")
    def download(self, path=None):
        """
        Download view method.

        :param path:
            File path.
        """
        if not self.can_download:
            abort(404)

        base_path, directory, path = self._normalize_path(path)

        # backward compatibility with base_url
        base_url = self.get_base_url()
        if base_url:
            base_url = urljoin(self.get_url(".index_view"), base_url)
            return redirect(urljoin(quote(base_url), quote(path).replace("%5C", "/")))
        return self.storage.send_file(directory)
