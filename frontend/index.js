generate_question_html = (i, question) => {
	let html_text = `<div class="form-group m-3"><label for="${i}"> ${i}. ${question} </label><br> <textarea class="form-control" rows=5 name="${i}" required></textarea></div>`
	return(html_text);
}

raise_error = (message) => {
	alert_html = `<div class="alert alert-danger" role="alert">
	${message}	
	</div>`;
	$("#alert-placeholder").html(alert_html);
}

$(document).ready(function () {
  // Submitting the resume using AJAX and displaying the questions
  $("#file-upload").submit(function (event) {
   var formURL = $(this).attr("action");
   $("#resume-upload-div").css("display", "none");
   $("#score-div").css("display", "none");
   $("#questions-div").css("display", "block");
   $("#spinner").css("display", "block");
   console.log("Submitting");
	  $.ajax({
		  type: "POST",
		  url: formURL,
		  data: new FormData(this),
		  processData: false,
		  contentType: false,
		  success: function(data){
		  	console.log("SUCCESS");
		  	console.log(data);
			$("#questions").attr('action', `http://localhost:5000/submit_answers/${data['id']}`);
			let questions_html = "";
			for (let index in data['questions']){
				console.log(data['questions'][index]);
				// questions_html += "<div>" + data['questions'][index] + "</div>";
				questions_html += generate_question_html(parseInt(index)+1, data['questions'][index])
			}
			console.log(questions_html);
			let qa_form_content = `${questions_html} <button class="btn btn-primary" type="submit"> Submit Answers </input>`
			$("#questions").html(qa_form_content);
			$("#spinner").css("display", "none");
		  },
		  error: function(data){
		  	console.log("ERROR");
		  	console.log(data);
			$("#spinner").css("display", "none");
			raise_error("Could not submit resume to server. Try again later");

		  }
	  });
   event.preventDefault();
  });

  // Submitting the answers using AJAX and displaying the score
  $("#questions").submit(function (event){
        $("#resume-upload-div").css("display", "none");
        $("#questions-div").css("display", "none");
        $("#score-div").css("display", "block");
	$("#spinner").css("display", "block");
	var formURL = $(this).attr("action");
	console.log("Submitting answers");
	console.log(this);
	$.ajax({
		type:"POST",
		url: formURL,
		data: new FormData(this),
		processData: false,
		contentType: false,
		success: function(data){
		    console.log("SUCCESS");
		    console.log(data);
		    $("#score-content").html(`<h5>Score: ${data['score']}</h5><br><h5>Reason: ${data['reason']}</h5>`)
		$("#spinner").css("display", "none");
		},
		error: function(data){
		    console.log("ERROR");
		    console.log(data);
		    $("#spinner").css("display", "none");
		    raise_error("Could not submit answers to the server. Try again later");
		},
	});
	event.preventDefault();
  });
});
