function send_ajax(action, method, data) {
	var req = new XMLHttpRequest();
	req.open(method, action, true);
	req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
	req.send(data);
}

function tile_click(idx) {
	send_ajax('/game', 'post', 'tile=' + idx);
}

function reset_board() {
	send_ajax('/game', 'post', 'reset=' + 'true');
}