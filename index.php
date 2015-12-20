<!DOCTYPE HTML PUBLIC=''>
<html>
<?php include dirname(__FILE__) . '/header.php'; ?>
<body>
<div class='container'>
    <h1>Slate</h1>
    <div class='row'>
        <div class='col-sm-3'>
            <form>
                <div class='form-group'>
                    <input class='form-control' name='cost' type='text' placeholder='Cost ($)' autocomplete='off'/>
                </div>
                <div class='form-group'>
                    <select class='form-control' name='category' autocomplete='off'>
                        <option value='select'>(Category)</option>
                        <option value='food-in'>Food (In)</option>
                        <option value='food-out'>Food (Out)</option>
                        <option value='alcohol'>Alcohol</option>
                        <option value='household'>Household items</option>
                        <option value='clothing'>Clothing</option>
                        <option value='transportation'>Transportation</option>
                        <option value='miscellaneous'>Miscellaneous</option>
                    </select>
                </div>
                <div class='form-group'>
                    <input class='form-control' name='comment' type='text' placeholder='Comment' autocomplete='off'/>
                </div>
                <div class='form-group'>
                    <input class='form-control' id='pw' type='password' placeholder='Password'/>
                </div>
                <div class='form-group'>
                    <button id='add' class='form-control' class='btn btn-default'>Add</button>
                </div>
            </form>
            <button id='view' class='btn btn-default'>View Report</button>
        </div>
    </div>
    <div id='report'></div>
</div>
</body>
</html>
