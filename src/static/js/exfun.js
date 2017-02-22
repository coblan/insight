
ex={
	parseSearch:function (queryString) {
		var queryString = queryString || location.search
		if(queryString.startsWith('?')){
			var queryString=queryString.substring(1)
		}
		var params = {}
	    // Split into key/value pairs
	    var queries = queryString.split("&");
	    // Convert the array of strings into an object
	    for (var i = 0; i < queries.length; i++ ) {
		    var mt = /([^=]+?)=(.+)/.exec(queries[i])
		    if(mt){
			    params[mt[1]] = decodeURI(mt[2]);
		    }
	    }
	    return params;
	},
	searchfy:function (obj,pre) {
		var outstr=pre||''
		for(x in obj){
			if(obj[x]!==''&&obj[x]!=null){
				outstr+=x.toString()+'='+ obj[x].toString()+'&';
			}
		}
		if(outstr.endsWith('&')){
			return outstr.slice(0,-1)
		}else if(outstr==pre){
			return ''
		}else{
			return outstr
		}
	},
	appendSearch:function(obj,url){
		if(url){
			var url_obj = ex.parseURL(url)
			var search = url_obj.params
		}else{
			url=location.href
			var search=ex.parseSearch()
		}
		ex.assign(search,obj)
		return url.replace(/(\?.*)|()$/,ex.searchfy(search,'?'))
	},
	parseURL: function(url) {
		var a = document.createElement('a');
		a.href = url;
		return {
			source: url,
			protocol: a.protocol.replace(':',''),
			host: a.hostname,
			port: a.port,
			search: a.search,
			params: (function(){
				var ret = {},
					seg = a.search.replace(/^\?/,'').split('&'),
					len = seg.length, i = 0, s;
				for (;i<len;i++) {
					if (!seg[i]) { continue; }
					s = seg[i].split('=');
					ret[s[0]] = s[1];
				}
				return ret;
			})(),
			file: (a.pathname.match(/\/([^\/?#]+)$/i) || [,''])[1],
			hash: a.hash.replace('#',''),
			pathname: a.pathname.replace(/^([^\/])/,'/$1'),
			relative: (a.href.match(/tps?:\/\/[^\/]+(.+)/) || [,''])[1],
			segments: a.pathname.replace(/^\//,'').split('/')
		};
	},
/*两种调用方式
 var template1="我是{0}，今年{1}了";
 var template2="我是{name}，今年{age}了";
 var result1=template1.format("loogn",22);
 var result2=template2.format({name:"loogn",age:22});
 两个结果都是"我是loogn，今年22了"
 */
	template:function (string,args) {
		var result = string;
		if(args.length){
			for (var i = 0; i < args.length; i++) {
                if (args[i] != undefined) {
                    //var reg = new RegExp("({[" + i + "]})", "g");//这个在索引大于9时会有问题，谢谢何以笙箫的指出
　　　　　　　　　　　　var reg= new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, args[i]);
                }
            }
		}else{
			 for (var key in args) {
                if(args[key]!=undefined){
                    var reg = new RegExp("({" + key + "})", "g");
                    result = result.replace(reg, args[key]);
                }
	         }
		}
	    return result;
		},
	/*
	ex.merge([{name:'dog',age:'18'}],[{name:'dog',label:'dog_label'}])
	>> [{name:'dog',age:'18',label:'dog_label'}]
	*/
	merge:function (src1,src2) {
		var self=this
		var dst_list=JSON.parse(JSON.stringify(src1))
		this.each(src2,function (src_item) {
			var obj = self.findone(dst_list,{name:src_item.name})
			if(obj){
				self.assign(obj,src_item)
			}else{
				dst_list.push(src_item)
			}
		})
		return dst_list
	},
	product:function (src1,src2) {
		var out=[]
		for(var i=0;i<src1.length;i++){
			for(var j=0;j<src2.length;j++){
				out.push([src1[i],src2[j]])
			}
		}
		return out
	},
	assign:function (dst,src) {
		for(var key in src){
			dst[key]=src[key]
		}
	},
	copy:function (obj) {
		return JSON.parse(JSON.stringify(obj))
	},
	findone:function (collection,obj) {
		for(var i=0;i<collection.length;i++){
			var now_obj=collection[i]
			var match=true
			for(var key in obj){
				if (obj[key] !=now_obj[key]){
					match =false
					break
				}
			}
			if(match){
				return now_obj
			}
		}
		return null
	},
	find:function (collection,obj) {
		out=[]
		for(var i=0;i<collection.length;i++){
			var now_obj=collection[i]
			var match=true
			for(var key in obj){
				if (obj[key] !=now_obj[key]){
					match =false
					break
				}
			}
			if(match){
				out.push(now_obj)
			}
		}
		return out
	},
	each:function (array,func) {
		for(var i=0;i<array.length;i++){
			func(array[i])
		}
	},
	split:function (base_str,sep) {
		if(base_str==''){
			return []
		}else{
			return base_str.split(sep)
		}
	},
	map:function (array,func) {
		var out=[]
		for(var i=0;i<array.length;i++){
			out.push(func(array[i]))
		}
		return out
	},
	isin:function (obj,array,func) {
		if(func){
			for(var i=0;i<array.length;i++){
				if(func(obj,array[i])){
					return true
				}
			}
			return false
		}else{
			return array.indexOf(obj)!=-1
		}
	},
	filter:function (array,func) {
		var out=[]
		for(var x=0;x<array.length;x++){
			if(func(array[x])){
				out.push(array[x])
			}
		}
		return out
	},
	any:function(array,func) {
		for(var x=0;x<array.length;x++){
			if(func(array[x])){
				return true
			}
		}
		return false
	},
	extend:function(array1,array2){
		array1.push.apply(array1,array2)
		return array1
	},
	remove:function (array,func_or_obj) {
		var index_ls=[]
		if (typeof func_or_obj == 'function'){
			var func=func_or_obj
			for(var i=0;i<array.length;i++){
				if(func(array[i])){
					index_ls.push(i)
				}
			}
		}else{
			var obj=func_or_obj
			for(var i=0;i<array.length;i++){
				var match=true
				for(var key in obj){
					if(obj[key]!=array[i][key]){
						match=false
					}
				}
				if(match){
					index_ls.push(i)
				}
				//if(array[i]==obj){
				//	index_ls.push(i)
				//}
			}
		}
		var rm_item=[]
		index_ls.reverse()
		for(var x=0;x<index_ls.length;x++){
			var rm=array.splice(index_ls[x],1)
			rm_item= rm.concat(rm_item)
		}
		return rm_item
	},
	load_js: function(src,success) {
		success = success || function(){};
		var name = src //btoa(src)
		if(!window['__js_hook_'+name]){
			window['__js_hook_'+name]=[]
		}
		window['__js_hook_'+name].push(success)
		var hooks=window['__js_hook_'+name]
		if(window['__js_loaded_'+name]){
			while (hooks.length>0){
				hooks.pop()()
			}
		}
		if(! window['__js_'+name]){
			window['__js_'+name]=true
			var domScript = document.createElement('script');
			  domScript.src = src;
			  domScript.onload = domScript.onreadystatechange = function() {
			    if (!this.readyState || 'loaded' === this.readyState || 'complete' === this.readyState) {
				  window['__js_loaded_'+name]=true
			      while (hooks.length>0){
						hooks.pop()()
					}
			      this.onload = this.onreadystatechange = null;
			      this.parentNode.removeChild(this);
			    }
			  }
			  document.getElementsByTagName('head')[0].appendChild(domScript);
		}
		
		
	},
	load_css:function (src) {
		var name = btoa(src)
		if(window['__src_'+name]){
			return
		}
		window['__src_'+name]=true
		$('head').append('<link rel="stylesheet" href="'+src+'" type="text/css" />')
	},
	is_fun:function (v) {
		return typeof v === "function"
	},
	get:function(url,callback){
		//replace $.get
		var self=this
		var wrap_callback=function (resp) {
			if (resp.msg) {
				self.show_msg(resp.msg)
			}
			if (resp.status && typeof resp.status == 'string' && resp.status != 'success') {
				hide_upload(300)
				return
			} else {
				callback(resp)
			}
		}
		return $.get(url,wrap_callback)
	},
	post:function(url,data,callback){
		var self=this
		var wrap_callback=function (resp) {
			if (resp.msg) {
				self.show_msg(resp.msg)
			}
			if (resp.status && typeof resp.status == 'string' && resp.status != 'success') {
				hide_upload(300) // sometime
				return
			} else {
				callback(resp)
			}
		}
		return $.post(url,data,wrap_callback)
	},
	show_msg:function(msg){
		alert(msg)
	}


}

function parseSearch(queryString) {
	var queryString = queryString || location.search
	if(queryString.startsWith('?')){
		var queryString=queryString.substring(1)
	}
	var params = {}
    // Split into key/value pairs
    var queries = queryString.split("&");
    // Convert the array of strings into an object
    for (var i = 0; i < queries.length; i++ ) {
	    var mt = /([^=]+?)=(.+)/.exec(queries[i])
        params[mt[1]] = mt[2];
    }
    return params;
}
function searchfy(obj,pre){
	var outstr=pre||''
	for(x in obj){
		if(obj[x]){
			outstr+=x.toString()+'='+ obj[x].toString()+'&';
		}
		
	}
	if(outstr.endsWith('&')){
		return outstr.slice(0,-1)
	}else{
		return outstr
	}
	
}
function update(dst_obj,src_obj) {
	for(x in src_obj){
		dst_obj[x]=src_obj[x]
	}
}

//  startsWith
if (!String.prototype.startsWith) {
    String.prototype.startsWith = function(searchString, position){
      position = position || 0;
      return this.substr(position, searchString.length) === searchString;
  };
  String.prototype.endsWith = function(str){
	return (this.match(str+"$")==str)
	};
}

Array.prototype.each = function(fn) 
{ 
return this.length ? [fn(this.slice(0,1))].concat(this.slice(1).each(fn)) : []; 
};


 /*两种调用方式
 var template1="我是{0}，今年{1}了";
 var template2="我是{name}，今年{age}了";
 var result1=template1.format("loogn",22);
 var result2=template2.format({name:"loogn",age:22});
 两个结果都是"我是loogn，今年22了"
 */
String.prototype.format = function(args) {
    var result = this;
    if (arguments.length > 0) {    
        if (arguments.length == 1 && typeof (args) == "object") {
            for (var key in args) {
                if(args[key]!=undefined){
                    var reg = new RegExp("({" + key + "})", "g");
                    result = result.replace(reg, args[key]);
                }
            }
        }
        else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] != undefined) {
                    //var reg = new RegExp("({[" + i + "]})", "g");//这个在索引大于9时会有问题，谢谢何以笙箫的指出
　　　　　　　　　　　　var reg= new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
    }
    return result;
}