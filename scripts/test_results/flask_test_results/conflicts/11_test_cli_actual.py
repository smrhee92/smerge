# -*- coding: utf-8 -*-
"""
    tests.test_cli
    ~~~~~~~~~~~~~~

    :copyright: (c) 2016 by the Flask Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
#
# This file was part of Flask-CLI and was modified under the terms its license,
# the Revised BSD License.
# Copyright (C) 2015 CERN.
#
from __future__ import absolute_import, print_function
import os
import sys

import click
import pytest
from click.testing import CliRunner
from flask import Flask, current_app

from flask.cli import cli, AppGroup, FlaskGroup, NoAppException, ScriptInfo, \
    find_best_app, locate_app, with_appcontext, prepare_exec_for_file, \
    find_default_import_path, get_version

@pytest.fixture
def runner():
    return CliRunner()



def test_cli_name(test_apps):
    """Make sure the CLI object's name is the app's name and not the app itself"""
    from cliapp.app import testapp
    assert testapp.cli.name == testapp.name


def test_find_best_app(test_apps):
    """Test if `find_best_app` behaves as expected with different combinations of input."""
    class Module:
        app = Flask('appname')
    class Module:
        application = Flask('appname')

    class Module:
        myapp = Flask('appname')
    assert find_best_app(Module) == Module.app
    class Module:
        pass

<<<<<<< REMOTE
    class Module:
        myapp1 = Flask('appname1')
        myapp2 = Flask('appname2')

=======

>>>>>>> LOCAL
    pytest.raises(NoAppException, find_best_app, Module)
    assert find_best_app(Module) == Module.application
    assert find_best_app(Module) == Module.myapp

    pytest.raises(NoAppException, find_best_app, Module)

def test_get_version(test_apps, capsys):
    """Test of get_version."""
    from flask import __version__ as flask_ver
    from sys import version as py_ver
    class MockCtx(object):
        resilient_parsing = False
        color = None
        def exit(self): return
    ctx = MockCtx()
    get_version(ctx, None, "test")
    out, err = capsys.readouterr()
    assert flask_ver in out
    assert py_ver in out


def test_prepare_exec_for_file(test_apps):
    """Expect the correct path to be set and the correct module name to be returned.

    :func:`prepare_exec_for_file` has a side effect, where
    the parent directory of given file is added to `sys.path`.
    """
    realpath = os.path.realpath('/tmp/share/test.py')
    dirname = os.path.dirname(realpath)
    assert prepare_exec_for_file('/tmp/share/test.py') == 'test'
    assert dirname in sys.path

    realpath = os.path.realpath('/tmp/share/__init__.py')
    dirname = os.path.dirname(os.path.dirname(realpath))
    assert prepare_exec_for_file('/tmp/share/__init__.py') == 'share'
    assert dirname in sys.path

    with pytest.raises(NoAppException):
        prepare_exec_for_file('/tmp/share/test.txt')


<<<<<<< REMOTE
def test_flaskgroup():
    """Test FlaskGroup."""
    def create_app(info):
        return Flask("flaskgroup")

    @click.group(cls=FlaskGroup, create_app=create_app)
    def cli(**params):
        pass

    @cli.command()
    def test():
        click.echo(current_app.name)

    runner = CliRunner()
    result = runner.invoke(cli, ['test'])
    assert result.exit_code == 0
    assert result.output == 'flaskgroup\n'



=======
def test_appgroup(runner):
    """Test of with_appcontext."""
    @click.group(cls=AppGroup)
    def cli():
        pass

    @cli.command(with_appcontext=True)
    def test():
        click.echo(current_app.name)

    @cli.group()
    def subgroup():
        pass

    @subgroup.command(with_appcontext=True)
    def test2():
        click.echo(current_app.name)

    obj = ScriptInfo(create_app=lambda info: Flask("testappgroup"))

    result = runner.invoke(cli, ['test'], obj=obj)
    assert result.exit_code == 0
    assert result.output == 'testappgroup\n'

    result = runner.invoke(cli, ['subgroup', 'test2'], obj=obj)
    assert result.exit_code == 0
    assert result.output == 'testappgroup\n'



>>>>>>> LOCAL
<<<<<<< REMOTE
def test_print_exceptions():
    """Print the stacktrace if the CLI."""
    def create_app(info):
        raise Exception("oh no")
        return Flask("flaskgroup")

    @click.group(cls=FlaskGroup, create_app=create_app)
    def cli(**params):
        pass

    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Exception: oh no' in result.output
    assert 'Traceback' in result.output

=======
def test_flaskgroup(runner):
    """Test FlaskGroup."""
    def create_app(info):
        return Flask("flaskgroup")

    @click.group(cls=FlaskGroup, create_app=create_app)
    def cli(**params):
        pass

    @cli.command()
    def test():
        click.echo(current_app.name)

    result = runner.invoke(cli, ['test'])
    assert result.exit_code == 0
    assert result.output == 'flaskgroup\n'



>>>>>>> LOCAL
class TestRoutes:
    def test_no_route(self, runner, monkeypatch):
        monkeypatch.setitem(os.environ, 'FLASK_APP', 'cliapp.routesapp:noroute_app')
        result = runner.invoke(cli, ['routes'], catch_exceptions=False)
        assert result.exit_code == 0
        assert result.output == """\
Route                    Endpoint  Methods           
-----------------------------------------------------
/static/<path:filename>  static    HEAD, OPTIONS, GET
"""

    def test_simple_route(self, runner, monkeypatch):
        monkeypatch.setitem(os.environ, 'FLASK_APP', 'cliapp.routesapp:simpleroute_app')
        result = runner.invoke(cli, ['routes'], catch_exceptions=False)
        assert result.exit_code == 0
        assert result.output == """\
Route                    Endpoint  Methods           
-----------------------------------------------------
/simpleroute             simple    HEAD, OPTIONS, GET
/static/<path:filename>  static    HEAD, OPTIONS, GET
"""

    def test_only_POST_route(self, runner, monkeypatch):
        monkeypatch.setitem(os.environ, 'FLASK_APP', 'cliapp.routesapp:only_POST_route_app')
        result = runner.invoke(cli, ['routes'], catch_exceptions=False)
        assert result.exit_code == 0
        assert result.output == """\
Route                    Endpoint   Methods           
------------------------------------------------------
/only-post               only_post  POST, OPTIONS     
/static/<path:filename>  static     HEAD, OPTIONS, GET
"""
def test_locate_app(test_apps):
    """Test of locate_app."""
    assert locate_app("cliapp.app").name == "testapp"
    assert locate_app("cliapp.app:testapp").name == "testapp"
    assert locate_app("cliapp.multiapp:app1").name == "app1"
    pytest.raises(NoAppException, locate_app, "notanpp.py")
<<<<<<< REMOTE
pytest.raises(NoAppException, locate_app, "cliapp/app")
=======

>>>>>>> LOCAL

    pytest.raises(NoAppException, locate_app, "cliapp.importerrorapp")
    pytest.raises(RuntimeError, locate_app, "cliapp.app:notanapp")
def test_find_default_import_path(test_apps, monkeypatch, tmpdir):
    """Test of find_default_import_path."""
    monkeypatch.delitem(os.environ, 'FLASK_APP', raising=False)
    assert find_default_import_path() == None
    monkeypatch.setitem(os.environ, 'FLASK_APP', 'notanapp')
    assert find_default_import_path() == 'notanapp'
    tmpfile = tmpdir.join('testapp.py')
    tmpfile.write('')
    monkeypatch.setitem(os.environ, 'FLASK_APP', str(tmpfile))
    expect_rv = prepare_exec_for_file(str(tmpfile))
    assert find_default_import_path() == expect_rv


def test_scriptinfo(test_apps):
    """Test of ScriptInfo."""
    obj = ScriptInfo(app_import_path="cliapp.app:testapp")
    assert obj.load_app().name == "testapp"
    assert obj.load_app().name == "testapp"
    def create_app(info):
        return Flask("createapp")

    obj = ScriptInfo(create_app=create_app)
    app = obj.load_app()
    assert app.name == "createapp"


    assert obj.load_app() == app

def test_with_appcontext(runner):
    """Test of with_appcontext."""
    @click.command()
    @with_appcontext
    def testcmd():
        click.echo(current_app.name)

    obj = ScriptInfo(create_app=lambda info: Flask("testapp"))
    runner = CliRunner()
    result = runner.invoke(testcmd, obj=obj)
    assert result.exit_code == 0


    assert result.output == 'testapp\n'


