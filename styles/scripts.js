

$(document).ready(function() {
  const paths = $('[id^="Plass_id_"]');
  const datoInput = $("input[placeholder='Valgt Dato']");
  const navLinks = $(".nav-item.nav-link");

  paths.click(function(event) {
    event.preventDefault();
    const computedStyle = window.getComputedStyle(this);
    if (computedStyle.getPropertyValue('fill') !== 'red') {
      paths.removeClass('selected');
      $(this).addClass('selected');
      $(this).css('fill', 'red');
    }
  });

  navLinks.on("click", function(event) {
    event.preventDefault();
    const dato = $(this).text().trim().split(" ")[1];
    datoInput.val(dato);
  });

  $(".nav-link").click(function() {
    $(".nav-link").removeClass("active"); // remove active class from all buttons
    $(this).addClass("active"); // add active class to the clicked button
  });
});


//kaller funksjon når man klikker på menyen
$(document).ready(function() {
  $('.nav-link').click(function(event) {
    event.preventDefault();
    var dato = $(this).text().trim().split(" ")[1];
    $.ajax({
      url: '/hent_bookings',
      type: 'POST',
      dataType: 'json',
      data: {'dato': dato},
      success: function(data) {
  console.log(data);


  var oppttate_plasser = data;
const pathsx = document.querySelectorAll("[id^='Plass_id_']");
const textbox = document.querySelector("input[placeholder='Valgt Plass']");

for (let i = 0; i < pathsx.length; i++) {
  pathsx[i].addEventListener("click", function(event) {
    const id = this.getAttribute("id").replace("Plass_id_", "");
    if (this.getAttribute("fill") !== "red" && !oppttate_plasser.some(p => p.plass_id === id)) {
      event.preventDefault();
      textbox.value = "";
      textbox.value += id + " ";
    }
  });
}



  var booketPlasser = data.booket_plasser;

  var styleId = 'plass-styles';
  $('#' + styleId).remove(); // remove the previous style element if it exists
  $('[id^="Plass_id_"] text').remove(); // remove previous text elements

  var style = $('<style></style>');  // create a new style element
  style.attr('id', styleId); // give it an ID
  $('head').append(style);  // append it to the head element

  for (var i = 0; i < data.length; i++) {
    var plassId = data[i].plass_id.trim();
    var pathSelector = '#Plass_id_' + plassId + ' path';
    style.append(pathSelector + ' { fill: red; }');  // add the style rule to the style element

    // add text element for bruker_id
    var bruker_id = data[i]['bruker_id'];
    var bookings_dato = data[i]['bookings_dato'];
    var svg_element = d3.select('#Plass_id_' + plassId);
    var bbox = svg_element.select('path').node().getBBox();
    var centerX = bbox.x + bbox.width / 2;
    var centerY = bbox.y + bbox.height / 2;
    svg_element.append('text')
      .attr('x', centerX)
      .attr('y', centerY)
      .attr('dy', '.35em')
      .attr('text-anchor', 'middle')
      .text(bruker_id)
      .style('fill', 'white')
      .style('font-size', '20px');
  }
},

      error: function(error) {
        console.error(error);
      }
    });
  });
});

function validateForm() {
    var plass = document.getElementById("Plass").value;
    var dato = document.getElementById("Dato").value;
    if (plass == "" || dato == "") {
        alert("Du har ikke valgt dag/plass");
        return false;
    }
    return true;
}
