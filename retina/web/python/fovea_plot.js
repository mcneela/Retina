//@sourceURL=test.js

$(document).ready(function() {
	setTimeout(function() {
		$('.ui.accordion').accordion();
		// $('.ui move up reveal').reveal();
		$('#graphLoader').fadeOut(function() {
			$(this).remove();
		});
		$('#graphDiv').unwrap();
		$('#jsonDropdown').dropdown();
	}, 1500);
});

$('#sideMenu #layers').click(function() {
});

$('#linkJSON').click(function(e) {
	var height = $('#graphDiv').css('height');
	var heightPercent = Math.round($('#graphDiv').height() /
		$('#graphDiv').parent().height() * 100);
	if (heightPercent == '100') {
		openJSONEditor();
	}
	else {
		closeJSONEditor();
	}
});

function openJSONEditor() {
	graph = $('#graphDiv');
	graph.animate({
		height: '65%',
	}, 400, 'easeOutQuint');
	graph.find('.scene').css('height', 'auto');
	graph.find('.scene').css('width', 'auto');
}

function closeJSONEditor() {
	graph = $('#graphDiv');
	graph.animate({
		height: '100%',
	}, 400, 'easeOutQuint');
	graph.find('*').scale(135);
}

$(document).on('click', '#layerButton', function() {
	window.open('layerManager.html', 'Layer Manager', 'width=800, height=600');
});
