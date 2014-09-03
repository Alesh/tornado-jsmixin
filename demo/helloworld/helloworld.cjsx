# @cjsx React.DOM

React = require("react")

HelloWorld = React.createClass
	render: ->
        <span>Hello, {@props.name}!</span>

module.exports = HelloWorld