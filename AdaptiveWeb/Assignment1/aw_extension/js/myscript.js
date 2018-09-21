function getUrlid() {
    var urlid = new URL(window.location.href);
    console.log(urlid);
    usern=urlid.searchParams.get("user");
    console.log(usern);
  

// attaching  the user to all links on the page
$('a').each(function() {
	console.log('Adding');
  this.href +='?&user='+usern;
});
    return usern;
}


var user;
user=getUrlid();

$('.vote').click(function(){

	chrome.extension.sendMessage({
		activity:'voted',
		usern:usern

	});

});

$('.user-action-time').click(function(){

	chrome.extension.sendMessage({
		activity:'checking edits',
		usern:usern
	});

});

$('.spacer').click(function(){

	chrome.extension.sendMessage({
		activity:'checking similar questions',
		usern:usern
	});

});

$('.short-link').click(function(){

	chrome.extension.sendMessage({
		activity:'sharing answer',
		usern:usern
	});

});

$('.pl8.aside-cta.grid--cell').click(function(){

	chrome.extension.sendMessage({
		activity:'asks question',
		usern:usern
	});

});
