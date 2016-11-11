/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports) {

	'use strict';

	/*
	Argments Format:
	=================

	heads=[{name:'xxx',label:'label1'},
	        {name:'jb',label:'jb'}]
	rows=[{xxx:"jjy",jb:'hahaer'}]

	 */

	Vue.component('sort-table', {
	    props: {
	        value: {},
	        heads: {
	            default: function _default() {
	                return [];
	            }
	        },
	        rows: {
	            default: function _default() {
	                return [];
	            }
	        },
	        sort: {
	            default: function _default() {
	                return [];
	            }
	        },
	        map: {
	            default: function _default() {
	                return function (name, row) {
	                    return row[name];
	                };
	            }
	        }
	    },
	    data: function data() {
	        return {
	            icatch: '',
	            selected: this.value
	        };
	    },
	    methods: {
	        in_sort: function in_sort(name) {
	            return this.sort.indexOf(name) != -1;
	        },
	        get_sort_pos: function get_sort_pos(name) {
	            if (name.startsWith('-')) {
	                name = name.substr(1);
	            }
	            var index = this.sort.indexOf(name);
	            if (index != -1) {
	                return index;
	            } else {
	                return this.sort.indexOf("-" + name);
	            }
	        },
	        sort_col: function sort_col(name) {
	            var pos = this.get_sort_pos(name);
	            if (pos == -1) {
	                this.sort.push(name);
	            } else {
	                this.sort[pos] = name;
	            }
	            this.$dispatch('sort-changed');
	        },
	        rm_sort: function rm_sort(name) {
	            var pos = this.get_sort_pos(name);
	            if (pos != -1) {
	                this.sort.splice(pos, 1);
	            }
	            this.$dispatch('sort-changed');
	        }
	    },
	    watch: {
	        selected: function selected(v) {
	            this.$emit('input', v);
	        }
	    },
	    template: '<table>\n\t\t\t<thead>\n\t\t\t\t<tr>\n\t\t\t\t\t<td style=\'width:50px\' v-if=\'selected\'>\n\t\t\t\t\t\t<input type="checkbox" name="test" value=""/>\n\t\t\t\t\t</td>\n\t\t\t\t\t<td v-for=\'head in heads\' :class=\'"td_"+head.name\'>\n\t\t\t\t\t\t<span v-if=\'head.sortable\' v-text=\'head.label\' class=\'clickable\' @click=\'sort_col(head.name)\'></span>\n\t\t\t\t\t\t<span v-else v-text=\'head.label\'></span>\n\t\t\t\t\t\t<span v-if=\'icatch = get_sort_pos(head.name),icatch!=-1\'>\n\t\t\t\t\t\t\t<span v-text=\'icatch\'></span>\n\t\t\t\t\t\t\t<span class="glyphicon glyphicon-chevron-up clickable" v-if=\'in_sort(head.name)\'\n\t\t\t\t\t\t\t\t @click=\'sort_col("-"+head.name)\'></span>\n\t\t\t\t\t\t\t<span v-if=\'in_sort("-"+head.name)\' class="glyphicon  glyphicon-chevron-down clickable"\n\t\t\t\t\t\t\t\t @click=\'sort_col(head.name)\'></span>\n\t\t\t\t\t\t\t<span v-if=\'in_sort(head.name)||in_sort("-"+head.name)\' class="glyphicon glyphicon-remove clickable"\n\t\t\t\t\t\t\t\t @click=\'rm_sort(head.name)\'></span>\n\t\t\t\t\t\t</span>\n\t\t\t\t\t</td>\n\t\t\t\t</tr>\n\t\t\t</thead>\n\t\t\t<tbody>\n\t\t\t\t<tr v-for=\'row in rows\'>\n\t\t\t\t\t<td v-if=\'selected\'><input type="checkbox" name="test" :value="row.pk" v-model=\'selected\'/></td>\n\t\t\t\t\t<td v-for=\'head in heads\' :class=\'"td_"+head.name\'>\n\t\t\t\t\t\t\n\t\t\t\t\t\t<span v-html=\'map(head.name,row)\'></span>\n\t\t\t\t\t</td>\n\t\t\t\t</tr>\n\t\t\t</tbody>\n\t\t</table>'
	});

	//<component v-if='icatch = map(head.name,row),icatch.com' :is='icatch.com' :kw='icatch.kw'></component>

	/*
	Argments:
	==========

	nums = ['1','...','6_a','7','8','...','999']

	Events:
	=======

	goto_page,num

	*/
	Vue.component('paginator', {
	    props: ['nums'],
	    methods: {
	        goto_page: function goto_page(num) {
	            if (!isNaN(parseInt(num)) && !num.endsWith('a')) {
	                this.$emit('goto_page', num);
	            }
	        }
	    },
	    template: '\n    <ul class="pagination page-num">\n\n    <li v-for=\'num in nums\' track-by="$index" :class=\'{"clickable": !isNaN(parseInt(num))}\' @click=\'goto_page(num)\'>\n    <span v-text=\'!isNaN(parseInt(num))? parseInt(num):num\' :class=\'{"active":num.endsWith("a")}\'></span>\n    </li>\n\n    </ul>\n    '
	});

	var build_table_args = {
	    methods: {
	        get_filter_obj: function get_filter_obj() {
	            //var search_str=''
	            var filter_obj = {};
	            for (var x = 0; x < this.filters.length; x++) {
	                var filter = this.filters[x];
	                if (filter.value) {
	                    filter_obj[filter.name] = filter.value;
	                    //search_str+= filter.name+'='+filter.value+'&'
	                }
	            }
	            if (this.q) {
	                filter_obj['_q'] = this.q;
	                //search_str+='_q='+this.q+'&'
	            }
	            return filter_obj;
	            //return search_str
	        },
	        get_sort_str: function get_sort_str() {
	            var sort_str = '';
	            for (var x = 0; x < this.sort.length; x++) {
	                sort_str += this.sort[x] + ',';
	            }
	            return sort_str;
	        },
	        search: function search() {
	            this.refresh_arg();
	        },
	        refresh_arg: function refresh_arg() {
	            var filter_obj = this.get_filter_obj();
	            var sort_str = this.get_sort_str();
	            var search_obj = { '_sort': sort_str };
	            update(search_obj, filter_obj);
	            location.search = searchfy(search_obj);
	            //location.search='_sort='+sort_str+'&'+search_str
	        },
	        goto_page: function goto_page(num) {
	            var filter_obj = this.get_filter_obj();
	            var sort_str = this.get_sort_str();
	            var search_obj = { '_sort': sort_str, '_page': num };
	            update(search_obj, filter_obj);
	            location.search = searchfy(search_obj);
	            //location.search='_sort='+sort_str+'&'+search_str+'_page='+num
	        }
	    },
	    events: {
	        'sort-changed': function sortChanged() {
	            this.refresh_arg();
	        }

	    }
	};

	document.write('\n<style type="text/css" media="screen" id="test">\nul.pagination li {display: inline;cursor: pointer}\n\nul.pagination li span {\n    color: black;\n    float: left;\n    padding: 4px 10px;\n    text-decoration: none;\n    border: 1px solid #ddd;\n}\n\nul.pagination li span.active {\n    background-color: #4CAF50;\n    color: white;\n}\n\nul.pagination li span:hover:not(.active) {background-color: #ddd;}\n</style>\n');

	window.build_table_args = build_table_args;

/***/ }
/******/ ]);