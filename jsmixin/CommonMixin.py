import os
import execjs 
import os.path
import logging 

class CommonMixin(object):
    """ Mixin for tornado.web.Application class allow using CommonJS features. """

    def __init__(self, **settings):
        self._requires = []
        self._styles = dict()
        self._scripts = dict()
        bundle_name = settings.get('bundle_name', 'bundle')
        self._debug = settings.get('debug', False)
        self._js_bundle = os.path.join(settings['static_path'], bundle_name) + '.js'
        self._css_bundle = os.path.join(settings['static_path'], bundle_name) + '.css'
        self._rebuild_bundle = settings.get('rebuild_bundle', False)


    def requireLib(self, name):
        """ Prepares CommonJS library with `name` to pack into bundle."""    
        self._requires.append(name)


    def registerFile(self, filename, alias=None):
        """ Prepares CommonJS module to pack into bundle."""
        filename = os.path.abspath(filename)
        if os.path.exists(filename):
            alias = alias or os.path.splitext(os.path.basename(filename))[0]
            if alias in self._scripts:
                if self._scripts[alias]!=filename:
                    logging.warning("Alias '%s' already has registred for '%s',"
                        " but will be overwrited for '%s'.", alias, self._scripts[alias], filename)
            self._scripts[alias] = filename
            style = os.path.splitext(filename)[0]+'.css'
            if os.path.exists(style):
                self._styles[alias] = style
        else:
            raise ValueError("Script: {0} is not found.".format(filename))    


    def buildBundle(self, rebuild=None):
        """ Builds CommonJS bundle """
        rebuild =  self._rebuild_bundle if rebuild is None else rebuild
        if not os.path.exists(os.path.dirname(self._js_bundle)):
            os.makedirs(os.path.dirname(self._js_bundle))
        js_bundle_ts = os.path.getmtime(self._js_bundle) if os.path.exists(self._js_bundle) else 0
        css_bundle_ts = os.path.getmtime(self._css_bundle) if os.path.exists(self._css_bundle) else 0
        js_files_max_ts = max([os.path.getmtime(filename) for filename in self._scripts.values()]) if self._scripts else 0
        css_files_max_ts = max([os.path.getmtime(filename) for filename in self._styles.values()]) if self._styles else 0
        with open(os.path.join(os.path.dirname(__file__), 'CommonMixin.js')) as file:
            ctx = execjs.compile(file.read())
            if self._scripts and (js_files_max_ts>js_bundle_ts or rebuild):
                files = list(self._scripts.items())
                try:
                    ctx.call('bundle_scripts', self._js_bundle, self._requires, files, self._debug)
                except execjs.RuntimeError as exc:
                    raise RuntimeError('execjs.RuntimeError: {0}'.format(exc.args[0].decode('utf8')))
                logging.warning("Rebuilded: '{0}'.".format(self._js_bundle))
            if self._styles and (css_files_max_ts>css_bundle_ts or rebuild):
                files = list(self._styles.values())
                try:
                    ctx.call('bundle_styles', self._css_bundle, files, self._debug)
                except execjs.RuntimeError as exc:
                    raise RuntimeError('execjs.RuntimeError: {0}'.format(exc.args[0].decode('utf8')))
                logging.warning("Rebuilded: '{0}'.".format(self._css_bundle)) 





