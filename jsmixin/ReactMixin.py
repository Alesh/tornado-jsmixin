import os
import re
import sys
import json
import uuid
import execjs 
import os.path
import importlib
import tornado.web
from jsmixin.CommonMixin import CommonMixin


class ReactUIModule(tornado.web.UIModule):
    """ Tornado UI module for placing JSX component on page template. """

    def render(self, component, tag="div", id=None, class_name=None, no_render=False, **props):
        """ Renders JSX components in initial state. """
        rendered_code = ""
        element_id = id or uuid.uuid1()
        props = self._prepareProps(props, component);
        class_name = component.replace('.', '-') + (' '+class_name if class_name is not None else '')
        if not (self.handler.application.settings.get('no_render', False) or no_render):
            try:
                rendered_code = self.handler.application._ctx.call('render_jsx', component, props)
            except execjs.RuntimeError as exc:
                raise RuntimeError('execjs.RuntimeError: {0}'.format(exc.args[0].decode('utf8')))
        startup_code = ('<script>'
                        'require("react").renderComponent(require("{0}")({1}), document.getElementById("{2}"));'
                        '</script>').format(component, props, element_id)
        return '<{3} id="{0}" class="{1}">{2}</{3}>'.format(element_id, class_name, rendered_code, tag) + startup_code
    
    def _prepareProps(self, props, component_name):
        return json.dumps(props)


class ReactMixin(CommonMixin):
    """ Mixin for tornado.web.Application class allow using React.js features. """
    
    def __init__(self, **settings):
        if not isinstance(self, tornado.web.Application):
            raise TypeError("This mixin must be used with class of 'tornado.web.Application'.")
        self._ctx = None            
        settings = settings or self.settings
        CommonMixin.__init__(self, **settings)
        self.requireLib('react')
        self.ui_modules['jsx'] = ReactUIModule


    _RE = re.compile('{% module jsx\("(.*?)"')

    def buildBundle(self, rebuild=None):
        """ Builds CommonJS bundle and prepare it for server page prerendering. """
        # scans all templates and registers all found components
        template_path = self.settings.get('template_path')
        if os.path.exists(template_path) and os.path.isdir(template_path):
            for dirname, _, filelist in os.walk(template_path):
                for filename in filelist:
                    filename = os.path.join(dirname, filename)
                    with open(filename) as file:
                        for alias in re.findall(self._RE, file.read()):
                            if alias not in self._scripts:
                                try:
                                    name = alias.split('.')[-1]
                                    module = importlib.import_module('.'.join(alias.split('.')[:-1]))
                                    component = getattr(module, name)
                                    if component:
                                        self.registerComponent(component)
                                        if hasattr(component, 'onRegister'):
                                            component.onRegister(self)
                                    else:
                                        raise
                                except:
                                    raise ValueError("Component: {0} is not found.".format(alias))

        CommonMixin.buildBundle(self, rebuild)
        if os.path.exists(self._js_bundle):
            with open(self._js_bundle) as file:
                bundle = file.read()
            with open(os.path.join(os.path.dirname(__file__), 'ReactMixin.js')) as file:
                self._ctx = execjs.compile(bundle+file.read());        


    def registerComponent(self, component, alias=None):
        """ Prepares React.js component to pack into bundle."""
        if isinstance(component, str) and os.path.exists(component):
            self.registerFile(component, alias)
            return
        elif isinstance(component, type) and hasattr(component, '__jsx__'):
            if component.__module__ in sys.modules:
                if hasattr(component, '__required__'):
                    for dependency in component.__required__:
                        self.registerComponent(dependency)
                filename = os.path.join(os.path.dirname(sys.modules[component.__module__].__file__), component.__jsx__)
                alias = component.__module__ + '.' + component.__name__
                self.registerFile(filename, alias)
            return
        else:
            raise ValueError("Component: {0} is not found.".format(component))




