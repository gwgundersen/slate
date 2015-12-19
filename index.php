<!DOCTYPE HTML PUBLIC=''>
<html>
<head>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
	<meta content='width=device-width, initial-scale=1' name='viewport'/>
	<title>Slate</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
	<script src='http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js'></script>
    <link rel='stylesheet' href='main.css'/>
    <script src='main.js'></script>
</head>
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
        </div>
        <div class='col-sm-3'>
            <button id='view'>View Report</button>
        </div>
    </div>
</div>
</body>
</html>
