    $(function () {
   $("#filter__range").slider({
  	min: 0,
  	max: 20000,
  	values: [5000,15000],
  	range: true,
  	stop: function(event, ui) {
      $("input#priceMin").val($("#filter__range").slider("values",0));
      $("input#priceMax").val($("#filter__range").slider("values",1));

      $('.price-range-min.value').html($("#filter__range").slider("values",0));
      $('.price-range-max.value').html($("#filter__range").slider("values",1));
    },
    slide: function(event, ui){
      $("input#priceMin").val($("#filter__range").slider("values",0));
      $("input#priceMax").val($("#filter__range").slider("values",1));

      $('.price-range-min.value').html($("#filter__range").slider("values",0));
      $('.price-range-max.value').html($("#filter__range").slider("values",1));
    }
  });

  $("input#priceMin").on('change', function(){
  	var value1=$("input#priceMin").val();
  	var value2=$("input#priceMax").val();
    if(parseInt(value1) > parseInt(value2)){
  		value1 = value2;
  		$("input#priceMin").val(value1);
      $('.price-range-min.value').html(value1);
  	}
  	$("#filter__range").slider("values", 0, value1);
    $('.price-range-min.value').html(value1);
  });

  $("input#priceMax").on('change', function(){
  	var value1=$("input#priceMin").val();
  	var value2=$("input#priceMax").val();
  	if (value2 > 20000) { value2 = 20000; $("input#priceMax").val(35000)}
  	if(parseInt(value1) > parseInt(value2)){
  		value2 = value1;
  		$("input#priceMax").val(value2);
      $('.price-range-max.value').html(value2);
  	}
  	$("#filter__range").slider("values",1,value2);
    $('.price-range-max.value').html(value2);
  });

  $('.ui-slider-handle:eq(0)').append('<span class="price-range-min value">' + $('#filter__range').slider('values', 0 ) + '</span>');
  $('.ui-slider-handle:eq(1)').append('<span class="price-range-max value">' + $('#filter__range').slider('values', 1 ) + '</span>');
});
      function submitForm() {
    document.getElementById("priceForm").submit();
  }