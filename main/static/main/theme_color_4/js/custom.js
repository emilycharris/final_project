// Horizontal scroll slider
//-----------------------------------------------------------------------------
//	Fuild layout, centering the items
$(function() {
$('#foo5').carouFredSel({
	width: '100%',
	scroll: 1,
	prev: '#prev2',
	next: '#next2',
	pagination: "#pager2",
	visible: {
		min: 1,
		max: 4,
	},
	auto: {
		pauseOnHover: 'resume',
	}
});
$('#foo4').carouFredSel({
	width: '100%',
	responsive: true,
	scroll: 1,
	prev: '#prev3',
	next: '#next3',
	pagination: "#pager3",
	visible: {
		min: 1,
		max: 1,
	},
	auto: {
		pauseOnHover: 'resume',
	}
});
});



// Pretty photo 
//-----------------------------------------------------------------------------
$(document).ready(function(){
	$("area[rel^='prettyPhoto']").prettyPhoto();
	
	$(".gallery:first a[rel^='prettyPhoto']").prettyPhoto({animation_speed:'normal',theme:'dark_square',slideshow:3000, autoplay_slideshow: false});
		
	$(".gallery:gt(0) a[rel^='prettyPhoto']").prettyPhoto({animation_speed:'fast',slideshow:10000, hideflash: true});
	
	$("#custom_content a[rel^='prettyPhoto']:first").prettyPhoto({
	custom_markup: '<div id="map_canvas" style="width:260px; height:265px"></div>',
	changepicturecallback: function(){ initialize(); }
	});
	
	$("#custom_content a[rel^='prettyPhoto']:last").prettyPhoto({
	custom_markup: '<div id="bsap_1259344" class="bsarocks bsap_d49a0984d0f377271ccbf01a33f2b6d6"></div><div id="bsap_1237859" class="bsarocks bsap_d49a0984d0f377271ccbf01a33f2b6d6" style="height:260px"></div><div id="bsap_1251710" class="bsarocks bsap_d49a0984d0f377271ccbf01a33f2b6d6"></div>',
	changepicturecallback: function(){ _bsap.exec(); }
	});
});



// Hover effect
//-----------------------------------------------------------------------------
jQuery(function($){
	$('.bar, .bar2').mosaic({
		animation:'slide'
	});
});



// Twitter plugin
//-----------------------------------------------------------------------------
jQuery(function($){
	$(".tweet").tweet({
	username: "wrapbootstrap",
	avatar_size: 30, //If you remove the comment from this line will display the avatar of twitter username and you must remove the default twitter icon from css/jquery.tweet.css
	count: 2,
	loading_text: "loading tweets..."
	});
});




// Flickr plugin
//-----------------------------------------------------------------------------
$('.basicuse').jflickrfeed({
	limit: 6,
	qstrings: {
	id: '37304598@N02' //Here your Flickr Id
	},
	itemTemplate: '<li><a href="{{image_b}}"><img src="{{image_s}}" alt="{{title}}" /></a></li>'
});




// Go to top
//-----------------------------------------------------------------------------
$(document).ready(function() {
	$().UItoTop({ easingType: 'easeOutQuart' });
});



// TOOLTIP
//-----------------------------------------------------------------------------
$('li').tooltip('hide');




// Toggle
//-----------------------------------------------------------------------------
$(function(){
	$('.myToggler').click(function(e){
		$(this).next().slideToggle();
		var sign=$(this).children(':first');
		sign.text(sign.text() == '\uff0b'?'\uff0d':'\uff0b');
		e.preventDefault;
	});
});