generate_question_html = (i, question) => {
	let html_text = `<label for="q-${i}"> ${i}. ${question} </label> <textarea rows=5 cols=100 name="q-${i}"></textarea>`
	return(html_text);
}

$(document).ready(function () {
  // Submitting the resume using AJAX and displaying the questions
  $("#file-upload").submit(function (event) {
   var formURL = $(this).attr("action");
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
				questions_html += generate_question_html(index, data['questions'][index])
			}
			console.log(questions_html);
			// let qa_form = `<form action="http://localhost:5000/submit_answers/${data['id']}" method="post"> ${questions_html} <input type="submit"> Submit Answer </input> </form>`
			let qa_form_content = `${questions_html} <input type="submit"> Submit Answer </input>`
			$("#questions").html(qa_form_content);
		  },
		  error: function(data){
		  	console.log("ERROR");
		  	console.log(data);
		  }
	  });
   $("#resume-upload-div").css("display", "none");
   $("#score-div").css("display", "none");
   $("#questions-div").css("display", "block");
   event.preventDefault();
  });

  // Submitting the answers using AJAX and displaying the score
  $("#questions").submit(function (event){
	
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
		    $("#score-content").html(`Score:${data['score']} <br>Reason:${data['reason']}`)
		},
		error: function(data){
		    console.log("ERROR");
		    console.log(data);
		},
	});
        $("#resume-upload-div").css("display", "none");
        $("#questions-div").css("display", "none");
        $("#score-div").css("display", "block");
	event.preventDefault();
  });
});
