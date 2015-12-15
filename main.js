$(function() {
    
    var pw = localStorage.getItem('slate'),
        $form = $('form'),
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
                comment: $('input[name="comment"]').val(),
                pw: $pw.val()
            };
        
        console.log(payload);
        if (isValid(payload)) {
            localStorage.setItem('slate', $pw.val());
            $.post('/slate/save.php', payload, function(resp) {
                if (resp === 'success') {
                    $form[0].reset();
                    alert('Success!');
                }
            }).error(function(data) {
                alert(data.responseText);
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
        if (typeof data.comment === 'undefined' || data.comment === '') {
            alert('Input a comment');
            return false;
        }
        return true;
    };
});
