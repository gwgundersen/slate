$(function() {
    
    var pw = localStorage.getItem('slate'),
        $add = $('button'),
        $pw = $('#pw');

    if (pw) {
        $pw.val(pw);
    }

    $add.click(function(evt) {
        evt.preventDefault();
        var pw = $('#pw').val(),
            payload = {
                cost: $('input[name="cost"]').val(),
                category: $('select[name="category"]').val(),
                comment: $('input[name="comment"]').val()
            };
        
        if (isValid(payload)) {
            localStorage.setItem('slate', $pw.val());
            $.post('/save.php', payload, function(resp) {
                console.log(resp);
            });
        }
    });

    function isValid(data) {
        if (typeof data.cost === 'undefined' || isNaN(parseFloat(data.cost))) {
            alert('Cost must be a float');
            return false;
        }
        if (typeof data.category === 'undefined' || data.category === 'select') {
            alert('Select a category');
            return false;
        }
        return true;
    };
});
