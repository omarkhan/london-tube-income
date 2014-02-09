# Max income to display on the graph
range = 1700

# Drawing surface width and height
w = 2673.8766
h = 1885.32

# Graph margins
margin = 110

# Plotting functions
x = d3.scale.linear().range([0 + margin, w - margin])
y = d3.scale.linear().domain([0, range]).range([0 + margin, h - margin])

# Line generator for income data
line = d3.svg.line()
  .x((d, i) -> x(i))
  .y((d) -> h - y(d.income))
  .interpolate('cardinal')

# Path tween function from http://bl.ocks.org/mbostock/3916621
pathTween = (path, precision) ->
  return ->
    path0 = this
    path1 = path0.cloneNode()
    path1.setAttribute('d', path)
    len0 = path0.getTotalLength()
    len1 = path1.getTotalLength()

    # Uniform sampling of distance based on specified precision
    dt = precision / Math.max(len0, len1)
    distances = (i for i in [dt..1] by dt)

    # Compute point-interpolators at each distance
    points = distances.map (t) ->
      p0 = path0.getPointAtLength(t * len0)
      p1 = path1.getPointAtLength(t * len1)
      return d3.interpolate([p0.x, p0.y], [p1.x, p1.y])

    return (t) ->
      if t < 1
        return 'M' + points.map((p) -> p(t)).join('L')
      return path

# Select the svg and add a g for the graph
map = d3.select('#map')
mapContent = d3.select('#map-content')
g = map.append('g')
  .attr('class', 'graph')

# Add graph axes
g.append('line')
  .attr('x1', x(0))
  .attr('y1', h - y(0))
  .attr('x2', x(range))
  .attr('y2', h - y(0))

g.append('line')
  .attr('x1', x(0))
  .attr('y1', h - y(0))
  .attr('x2', x(0))
  .attr('y2', h - y(range))

g.selectAll('.y-label')
  .data(y.ticks(4))
  .enter()
  .append('text')
  .attr('class', 'y-label')
  .text((d) -> d.toString())
  .attr('x', x(0) - 30)
  .attr('y', (d) -> h - y(d))
  .attr('dy', 15)

g.selectAll('y-tick')
  .data(y.ticks(4))
  .enter()
  .append('line')
  .attr('class', 'y-tick')
  .attr('x1', x(0))
  .attr('y1', (d) -> h - y(d))
  .attr('x2', x(0) - 12)
  .attr('y2', (d) -> h - y(d))

# Display the graph for the given line id and income data
render = (lineId, stations) ->
  # Fade out and remove the existing graph, if any
  g.select('path')
    .transition()
    .duration(500)
    .style('opacity', 0)
    .transition()
    .remove()

  # Set the x domain to the number of stations
  x.domain([0, stations.length - 1])

  # Add x ticks for each station
  g.selectAll('.x-tick').remove()
  g.selectAll('.x-tick')
    .data(stations)
    .enter()
    .append('line')
    .attr('class', 'x-tick')
    .attr('x1', (d, i) -> x(i))
    .attr('y1', h - y(0))
    .attr('x2', (d, i) -> x(i))
    .attr('y2', h - y(0) + 12)

  # Add x axis labels for each station
  g.selectAll('.x-label').remove()
  g.selectAll('.x-label')
    .data(stations)
    .enter()
    .append('text')
    .attr('class', 'x-label')
    .text((d) -> d.name)
    .attr('x', (d, i) -> x(i))
    .attr('y', h - y(0) + 30)
    .attr('transform', (d, i) -> "rotate(-80, #{x(i) + 12}, #{h - y(0) + 30})")

  # Transition the line on the map to the graph using pathTween
  mapContent.classed('fade', true)
  original = map.select("##{lineId} path.main")
  path = g.append('path').attr({
    d: original.attr('d')
    style: original.attr('style')
  })
  path.transition()
    .duration(1000)
    .attrTween('d', pathTween(line(stations), 10))

# Bind events
lines = d3.select('#lines')
lines.selectAll('.line')
  .data(DATA.lines)
  .each ({name, id, branches}) ->
    d3.select(this)
      .on('click', ->
        branches = d3.select(this).select('.branches')
        hidden = branches.style('display') == 'none'
        d3.selectAll('.branches').style('display', 'none')
        if hidden
          branches.style('display', 'block'))
      .selectAll('.branch')
      .data(branches)
      .on('click', ({stations}) ->
        d3.event.stopPropagation()
        render(id, stations))
