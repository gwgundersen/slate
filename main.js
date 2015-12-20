$(function() {
    
    var pw = localStorage.getItem('slate'),
        $form = $('form'),
        $add = $('button#add'),
        $view = $('button#view'),
        $report = $('#report'),
        $pw = $('#pw');

    if (pw) {
        $pw.val(pw);
    }

    $pw.change(function() {
        localStorage.setItem('slate', $pw.val());
    });

    $add.click(function(evt) {
        evt.preventDefault();
        var pw = $pw.val(),
            payload = {
                cost: $('input[name="cost"]').val(),
                category: $('select[name="category"]').val(),
                comment: $('input[name="comment"]').val(),
                pw: $pw.val()
            };
        
        if (isValid(payload)) {
            $.post('/slate/add', payload, function(resp) {
                if (resp === 'success') {
                    $form[0].reset();
                    alert('Success!');
                }
            }).error(function(data) {
                alert(data.responseText);
            });
        }
    });

    $view.click(function(evt) {
        evt.preventDefault();
        $.get('/slate/view', { pw: $pw.val() }, function(data) {
            if (data.indexOf('incorrect password') > 0) {
                alert('Incorrect password');
            } else {
                $report.html(data);
                $form.hide();
                $view.hide();
            }
        });
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
