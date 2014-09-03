var browserify = require('browserify'),
    uglifycss = require('uglifycss'),
    uglifyify = require('uglifyify'),
    coffeeify, reactify, coffee_reactify,
    fs = require('fs');


try {
    coffeeify  = require('coffeeify');
} catch(e) {}

try {
    coffee_reactify = require('coffee-reactify');
} catch(e) {}

try {
    reactify = require('reactify');
} catch(e) {}



function bundle_scripts(bundle_file, requires, files, debug) 
{
    var b = browserify({debug: debug, global: true})
    if (typeof coffeeify !== 'undefined') 
        b.transform({global: true}, coffeeify);
    if (typeof reactify !== 'undefined') 
        b.transform({global: true}, reactify);
    if (typeof coffee_reactify !== 'undefined') 
        b.transform({global: true}, coffee_reactify);
    if (!debug)
        b.transform({global: true}, uglifyify);
    requires.forEach(function(element) {
        b.require(element);
    });
    files.forEach(function(element) {
        b.require(element[1], {expose: element[0]});
    });
    b.bundle().pipe(fs.createWriteStream(bundle_file));
}

function bundle_styles(bundle_file, files, debug)
{
    var result,
        outStream = fs.createWriteStream(bundle_file);
    if (debug) {
        result = '';
        files.forEach(function(file) {
            result += '/**\n * file: '+file+'\n */\n';
            result += fs.readFileSync(file);
            result += '\n\n';
        });
    } else {
        result = uglifycss.processFiles(files, {expandVars: true});
    }
    outStream.write(result);
    outStream.end();
}