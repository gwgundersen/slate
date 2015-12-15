<!DOCTYPE HTML PUBLIC=''>
<html>
<head>
	<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>
	<meta content='width=device-width, initial-scale=1' name='viewport'/>
	<title>Slate</title>
    <link rel='stylesheet' href='main.css'/>
	<script src='http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js'></script>
    <script src='main.js'></script>
</head>
<body>
<div class='page'>
    <h1>Slate</h1>
    <form>
        <div>
            <input name='cost' type='text' placeholder='Cost ($)' autocomplete='off'/>
        </div>
        <div>
            <select name='category' autocomplete='off'>
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
        <div>
            <input name='comment' type='text' placeholder='Comment' autocomplete='off'/>
        </div>
        <div>
            <input id='pw' type='text' placeholder='Password'/>
        </div>
        <div>
            <button>Add</button>
        </div>
    </form>
</div>
</body>
</html>
