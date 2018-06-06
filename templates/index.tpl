<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Daily Bread</title>
  <meta name="description" content="Scripture reading of the day.">
  <meta name="keywords" content="bible, scripture, daily, bread">
  <meta name="robots" content="all">
  <link rel="stylesheet" type="text/css" href="/static/css/main.css">
</head>
<body>
  <div id="wrapper">
    <header>
      <h1>Daily Bread</h1>
    </header>

    <main>
      <!-- cache daily book and chapter here -->
      <h1>{{ title }}</h1>
      {{! text }}
    </main>

    <footer>
      <p>
        &copy; 2018 <a href="http://ndrwkim.com" target="_blank">ndrwkim</a>.
      </p>
      {{! copyright }}
    </footer>
  </div>
</body>
</html>