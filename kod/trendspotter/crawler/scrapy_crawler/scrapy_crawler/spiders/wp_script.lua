function main(splash)
  splash.images_enabled = false
  splash.timeout = 60
  local render_time = 6
  local url = splash.args.url
	assert(splash:go(url))
  assert(splash:wait(render_time))
        
  splash:set_viewport_full()

  local buttons = {'_2eqe0jj', '_1rh9-ML', '_1YnfD5d', 'hPppTzo'};
  local continue = false;

  local href = splash:jsfunc([[
  function() {
    var x = document.getElementsByTagName('a')
    var arr = []
    for(var i = 0; i < x.length; i++) {
      arr.push(x[i].href)
    }
    return arr
  }
  ]])
  
  local click = splash:jsfunc([[
  function(link) {
  	var x = document.getElementsByClassName(link)
    var res = x.length
    for(var i = 0; i < x.length; i++) {
    		x[i].click();
  	}
  	return res
  }]])
  
  local res_link = {}
  for i=1, #buttons do
    local value = click(buttons[i])
    table.insert(res_link, {buttons[i], value})
    splash:wait(render_time)
  end
  
  local com_links = {'_2H53dzb', 'tCAnOuA _2oPK6Em'}
  local get_comments = splash:jsfunc([[
  function(link) {
    var x = document.getElementsByClassName(link);
    var arr = []
    for(var i = 0; i < x.length; i++) {
    	arr.push(x[i].innerHTML);
  	}
    return arr;
  }
  ]])
  
  local comments = {}
  for i=1, #com_links do
  	local elems = get_comments(com_links[i])
    for i=1, #elems do
    	table.insert(comments, elems[i])  
    end
  end
  
	return {
  	num = res_link,
    comments = comments,
    links = href(),
		-- html = splash:html(),
  }
end