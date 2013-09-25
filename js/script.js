$(window).load(function(){

		for(i=0; i<8; i++){
			$row = $("<div class='board-row'>");
			$("#board").append($row);
			for(j=0; j<8; j++){
				if((i+j)%2 == 0)
					$row.append("<div class='board-box board-box-green' />");
				else{
					$box = $("<div class='board-box board-box-yellow'/>");
					$row.append($box);
					if(i < 3){
						$box.append("<div class='board-coin board-coin-red' />");
					}
					else if(i > 4){
						$box.append("<div class='board-coin board-coin-black' />");
					}
				}
			}
		}
});
