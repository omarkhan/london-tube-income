range = 1500
w = 960
h = 400
margin = 45

x = d3.scale.linear().range([0 + margin, w - margin])
y = d3.scale.linear().domain([0, range]).range([0 + margin, h - margin])

graph = d3.select('#graph')
g = graph.append('g')
  .attr('transform', 'translate(0, 400)')

line = d3.svg.line()
  .x((d, i) -> x(i))
  .y((d) -> -y(d.income))
  .interpolate('cardinal')

g.append('line')
  .attr('x1', x(0))
  .attr('y1', -y(0))
  .attr('x2', x(range))
  .attr('y2', -y(0))

g.append('line')
  .attr('x1', x(0))
  .attr('y1', -y(0))
  .attr('x2', x(0))
  .attr('y2', -y(range))

g.selectAll('.y-label')
  .data(y.ticks(4))
  .enter()
  .append('text')
  .attr('class', 'y-label')
  .text((d) -> d.toString())
  .attr('x', x(0) - 10)
  .attr('y', (d) -> -y(d))
  .attr('dy', 5)

g.selectAll('y-tick')
  .data(y.ticks(4))
  .enter()
  .append('line')
  .attr('class', 'y-tick')
  .attr('x1', x(0))
  .attr('y1', (d) -> -y(d))
  .attr('x2', x(0) - 4)
  .attr('y2', (d) -> -y(d))

path = g.append('path')
render = (lineIdx) ->
  [lineName, branches] = DATA.lines[lineIdx]
  return (branchIdx) ->
    [branchName, stations] = branches[branchIdx]
    x.domain([0, stations.length])

    g.selectAll('x-tick')
      .data(stations)
      .enter()
      .append('line')
      .attr('class', 'x-tick')
      .attr('x1', (d, i) -> x(i))
      .attr('y1', -y(0))
      .attr('x2', (d, i) -> x(i))
      .attr('y2', -y(0) + 4)

    g.selectAll('.x-label')
      .data(stations)
      .enter()
      .append('text')
      .attr('class', 'x-label')
      .text((d) -> d.name)
      .attr('x', (d, i) -> x(i))
      .attr('y', -y(0) + 10)
      .attr('transform', (d, i) -> "rotate(-80, #{x(i) + 4}, #{-y(0) + 10})")

    path.transition().attr('d', line(stations))
