$(function() {
  $('input[type=checkbox]').on('change', function() {
    var $input = $(this);
    var isChecked = $input.prop('checked');
    var $removeBtn = $input.closest('.form-check').find('.remove-tag');
    if (isChecked) {
      $removeBtn.show();
      $input.closest('.form-check').addClass('border border-info p-2');
    } else {
      $removeBtn.hide();
      $input.closest('.form-check').removeClass('border border-info p-2');
    }
  });
  $('.remove-tag').click(function(e) {
    e.preventDefault();
    var $removeBtn = $(this);
    var $input = $removeBtn.closest('.form-check').find('input[type=checkbox]');
    var tagId = $input.val();
    $input.prop('checked', false);
    $removeBtn.closest('.form-check').removeClass('border border-info p-2').remove();
  });
});
